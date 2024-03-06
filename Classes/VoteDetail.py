import datetime
import re
from enum import Enum
import sqlite3
from Classes.Member import Member
from ok_legislature_config import ok_file_sections


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
        :param date: Date of action (date format).
        :param time: Time of action (time format).
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
        self.date = datetime.datetime
        self.time = datetime.time

    def __str__(self):
        return f"VoteDetail({self.unique_index}, {self.bill_number}, {self.vote_type}, {self.yea}, {self.nay}, {self.cp}, {self.excused}, {self.vacant}, {self.result}, {self.location}, {self.date}, {self.time})"

    @classmethod
    def parse(cls, text: [str]):
        previous_line = None
        all_members = list[Member]
        for line in text:
            if line == "GENERAL ORDER" or line == '':
                continue

            bill_detail = line.lstrip()

            # set bill number
            cls.bill_number = cls.find_hb_pattern(bill_detail)

            # set vote type
            if bill_detail.isupper():
                cls.vote_type = bill_detail.upper()

            # set result (pass,fail)
            if previous_line.startswith('Vacancy'):
                cls.result = cls.extract_pass_fail(line)

            # sending entire text body since we now have this split
            # and should be faster to parse now
            aye_members, cls.yea = cls.extract_votes(text, Vote.AYE)
            nay_members, cls.nay = cls.extract_votes(text, Vote.NAY)

            for member in aye_members:
                print('AYE: ' + member)

            for member in nay_members:
                print('NAY: ' + member)

            # store previous line for referencing
            previous_line = line

    @classmethod
    def extract_votes(cls, lines, vote_type: Vote):
        aye_votes = []
        count = None

        for line in lines:
            if line.startswith(vote_type):
                # Remove "Aye:" and split the line into names
                names = line[4:].split(',')
                # Remove spaces and empty strings
                names = [name.strip() for name in names if name.strip()]
                aye_votes.extend(names)

            # Check for the pattern .--#
            match = re.search(r'\.--(\d+)', line)
            if match:
                count = match.group(1)
                break  # Exit the loop after finding the count

        return aye_votes, count

    @classmethod
    def extract_pass_fail(cls, text):
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

    @classmethod
    def find_hb_pattern(cls, text):
        pattern = r"[A-Z]{2} \d+"
        match = re.search(pattern, text)
        if match:
            return match.group()
        else:
            return "No match found"

    @classmethod
    def in_current_section(cls, text: str) -> bool:
        return not text.isupper()

    @classmethod
    def is_empty(cls, text: str) -> bool:
        return not bool(text.strip())

    # Function to insert a new VoteDetail
    def insert_vote_detail(vote_detail):
        cursor.execute('''
        INSERT INTO votes (unique_index, bill_number, vote_type, yea, nay, cp, excused, vacant, result, location, date, time)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (vote_detail.unique_index, vote_detail.bill_number, vote_detail.vote_type, vote_detail.yea,
              vote_detail.nay, vote_detail.cp, vote_detail.excused, vote_detail.vacant, vote_detail.result,
              vote_detail.location, vote_detail.date, vote_detail.time))
        conn.commit()
