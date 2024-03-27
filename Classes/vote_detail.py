import csv
import datetime
import os
import re
from enum import Enum
from Classes.member import Member, create_member
from Classes.vote_roll_call import create_vote_roll_call


class Vote(Enum):
    AYE = "Aye:"
    NAY = "Nay:"
    CP = "Constitutional Priv:"
    EXCUSED = "Excused:"
    VACANCY = "Vacancy:"


class VoteDetail:
    """
    A class representing the details of a vote in a legislative process.
    """

    def __init__(self, unique_index, bill_number, vote_type, yea, nay, cp, excused, vacant, result, location):
        """
        Initialize the VoteDetail class with given properties.

        :param unique_index: A unique index that may be used as a database key.
        :param bill_number: Bill number (e.g., HB 4837, HB3XX, HJR1011, SCR2).
        :param vote_type: Type of vote (e.g., Third Reading, Emergency, Do Pass, etc.).
        :param yea: Votes for (integer).
        :param nay: Votes against (integer).
        :param cp: Constitutional Privilege (integer).
        :param excused: Members not present (integer).
        :param vacant: Seats without an elected member (integer).
        :param result: Outcome of the vote (Pass or Fail).
        :param location: Location of the vote (House Floor, Senate Floor, Committee Name).
        """
        self.unique_index = unique_index
        self.bill_number = bill_number
        self.vote_type = vote_type
        self.yea = yea
        self.nay = nay
        self.cp = cp
        self.excused = excused
        self.vacant = vacant
        self.result = result
        self.location = location
        self.date = datetime.date.today()
        self.time = datetime.datetime.now().time()

    def __str__(self):
        return f"VoteDetail({self.unique_index}, {self.bill_number}, {self.vote_type}, {self.yea}, {self.nay}, {self.cp}, {self.excused}, {self.vacant}, {self.result}, {self.location}, {self.date}, {self.time})"

    def parse(self, text: [str]):
        previous_line = None
        for line in text:
            if line == "GENERAL ORDER" or line == '':
                continue

            bill_detail = line.lstrip()

            # set bill number
            if self.bill_number is None:
                self.bill_number = self.find_hb_pattern(bill_detail)

            # set vote type
            if bill_detail.isupper() and self.bill_number is not None:
                self.vote_type = bill_detail.upper()

            if previous_line is not None and previous_line.startswith('Vacancy'):
                self.result = self.extract_pass_fail(line)

            if self.excused is None:
                excused_members = self.extract_votes(text, Vote.EXCUSED)
                self.excused = len(excused_members)
                self.to_vote_roll_call(excused_members, Vote.EXCUSED)

            if self.vacant is None:
                vacant_members = self.extract_votes(text, Vote.VACANCY)
                self.vacant = len(vacant_members)
                self.to_vote_roll_call(vacant_members, Vote.VACANCY)

            if self.cp is None:
                cp_members = self.extract_votes(text, Vote.CP)
                self.cp = len(cp_members)
                self.to_vote_roll_call(cp_members, Vote.CP)

            if self.yea is None:
                aye_members = self.extract_votes(text, Vote.AYE)
                self.yea = len(aye_members)
                self.to_vote_roll_call(aye_members, Vote.AYE)

            if self.nay is None:
                nay_members = self.extract_votes(text, Vote.NAY)
                self.nay = len(nay_members)

                self.to_vote_roll_call(nay_members, Vote.NAY)

            # store previous line for referencing
            previous_line = line

    def to_member(self, names):
        members = []
        for name in names:
            member = create_member(0, self.location, )

    def set_chamber(self, location):
        if 'House' in location:
            return 'House'
        if 'Senate' in location:
            return 'Senate'

    def to_vote_roll_call(self, names, vote: Vote):
        downloads_folder = os.path.join(os.path.expanduser('~'), 'Downloads')
        vote_roll_call_csv_path = os.path.join(downloads_folder, "vote_roll_call.csv")
        vote_roll_calls = []
        id = 1
        for name in names:
            # Assuming other properties are provided here in some way
            vote_roll_call = create_vote_roll_call(name, self.unique_index, id, self.bill_number,
                                                   vote.value.replace(':', ''), self.vote_type, self.date, self.time,
                                                   self.result)
            vote_roll_calls.append(vote_roll_call)
            id = id + 1

        self.write_votes_to_csv(vote_roll_calls, vote_roll_call_csv_path)

    def extract_votes(self, lines, vote_type: Vote):
        votes = []

        for line in lines:
            line = line.strip()
            if line.startswith(vote_type.value):
                # Remove "Aye:" and split the line into names
                names = line[4:].split(',')
                # Remove spaces and empty strings
                names = [name.strip() for name in names if name.strip()]
                votes.extend(names)

        return votes

    def extract_pass_fail(self, text):
        """
        Extracts 'Pass' or 'Fail' from a given text string.
        """
        # Regular expression to find 'Pass' or 'Fail'
        pattern = r'\b(Pass|Fail)\b'
        match = re.search(pattern, text, re.IGNORECASE)

        if match:
            return match.group()
        else:
            return None

    def find_hb_pattern(self, text):
        pattern = r"[A-Z]{2} \d+"
        match = re.search(pattern, text)
        if match:
            return match.group()
        else:
            return f"[[{text}]]"

    def in_current_section(self, text: str) -> bool:
        return not text.isupper()

    def is_empty(self, text: str) -> bool:
        return not bool(text.strip())

    def to_dict(self):
        return {
            "unique_index": self.unique_index,
            "bill_number": self.bill_number,
            "vote_type": self.vote_type,
            "yea": self.yea,
            "nay": self.nay,
            "cp": self.cp,
            "excused": self.excused,
            "vacant": self.vacant,
            "result": self.result,
            "location": self.location,
            # Convert datetime objects to string if not None, else use an empty string or None
            "date": self.date.isoformat() if self.date is not None else '',
            "time": self.time.isoformat() if self.time is not None else ''
        }


    @staticmethod
    def write_votes_to_csv(vote_roll_calls, filename):
        """
        Append vote roll call data to a CSV file. If the file doesn't exist, it creates it.

        :param vote_roll_calls: List of VoteRollCall objects.
        :param filename: Name of the CSV file.
        """
        try:
            # Check if the file already exists to determine if we need to write headers
            file_exists = os.path.isfile(filename)

            with open(filename, mode='a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)

                # Write the header only if the file didn't exist
                if not file_exists:
                    writer.writerow(
                        ['Unique Index', 'Votes Detail Index', 'Bill Number', 'Member', 'Vote', 'Vote Type', 'Location',
                         'Date', 'Time'])

                # Append vote roll call data
                for vote in vote_roll_calls:
                    writer.writerow(
                        [vote.unique_index, vote.votes_detail_index, vote.bill_number, vote.member, vote.vote,
                         vote.vote_type, vote.location, vote.date, vote.time])

            print(f"Vote roll call data successfully appended to {filename}")
        except Exception as e:
            print(f"An error occurred while writing to CSV: {e}")
