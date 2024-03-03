import re
from ok_legislature_config import ok_file_sections


class VoteDetail:
    """
    A class representing the details of a vote in a legislative process.
    """

    def __init__(self, unique_index, bill_number, vote_type, yea, nay, cp, excused, vacant, result, location, date,
                 time):
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
        self.date = date
        self.time = time

    def __str__(self):
        return f"VoteDetail({self.unique_index}, {self.bill_number}, {self.vote_type}, {self.yea}, {self.nay}, {self.cp}, {self.excused}, {self.vacant}, {self.result}, {self.location}, {self.date}, {self.time})"


# Updated extract_vote_details function to handle multiple bills based on "GENERAL ORDER" sections


def extract_section_by_keyword(text, keyword):
    """
    Extracts a section from the text starting with the given keyword until it reaches text with all capital letters.

    :param text: The input text from which sections are extracted.
    :param keyword: The keyword to search for in the text.
    :return: Extracted section of the text.
    """
    # Define a regex pattern to find the section
    # The pattern looks for the keyword, then captures everything until it finds a line with all capital letters
    pattern = rf"{keyword}(.*?)(?=\n[A-Z\s]+$)"

    # Use regex to find all matches
    matches = re.findall(pattern, text, re.DOTALL)

    # Join all matches to get the full section
    section = "\n".join(matches)

    return section

    # Example usage (commented out to prevent execution)
    # text = "Your input text here"
    # keyword = "HOUSE JOURNAL"
    # extracted_section = extract_section_by_keyword(text, keyword)
    # print(extracted_section)


def in_current_section(text: str) -> bool:
    return not text.isupper()


def is_empty(text: str) -> bool:
    return not bool(text.strip())

# Test the function with the provided sample text
# Uncomment the below lines to test
# vote_details = extract_vote_details(sample_text)
# print(vote_details)

