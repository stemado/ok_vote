class VoteRollCall:
    """
    A class representing individual roll call entries for votes in a legislative process.
    """

    def __init__(self, unique_index, votes_detail_index, bill_number, member, vote, vote_type, location, date, time):
        """
        Initialize the VoteRollCall class with given properties.

        :param unique_index: A unique index that may be used as a database key.
        :param votes_detail_index: The same value as the VoteDetail unique index.
        :param bill_number: Bill number (e.g., HB 4837, HB3XX, HJR1011, SCR2).
        :param member: Name of the member or 'Mr. Speaker' or 'House District XX' for vacant seats.
        :param vote: Type of vote cast by the member (Yea, Nay, CP, Excused).
        :param vote_type: Type of vote (e.g., Third Reading, Emergency, Do Pass, etc.).
        :param location: Location of the vote (House Floor, Senate Floor, Committee Name).
        :param date: Date of action (date format).
        :param time: Time of action (time format).
        """
        self.unique_index = unique_index
        self.votes_detail_index = votes_detail_index
        self.bill_number = bill_number
        self.member = member
        self.vote = vote
        self.vote_type = vote_type
        self.location = location
        self.date = date
        self.time = time

    def __str__(self):
        return f"VoteRollCall({self.unique_index}, {self.votes_detail_index}, {self.bill_number}, {self.member}, {self.vote}, {self.vote_type}, {self.location}, {self.date}, {self.time})"


# https://chat.openai.com/share/e/e4a20aca-b855-427a-a794-364291643351
def create_vote_roll_call(name, unique_index, votes_detail_index, bill_number, vote, vote_type, location, date, time):
    """
    Create a VoteRollCall instance with the given parameters.

    :param name: Name of the member.
    :param unique_index, votes_detail_index, bill_number, vote, vote_type, location, date, time: Other properties of VoteRollCall.
    :return: A VoteRollCall instance.
    """
    return VoteRollCall(unique_index, votes_detail_index, bill_number, name, vote, vote_type, location, date, time)

# Example usage
# names = ["John Doe", "Jane Smith", "Alex Johnson"]
# vote_roll_calls = []
# for name in names:
#     # Assuming other properties are provided here in some way
#     vote_roll_call = create_vote_roll_call(name, ...)
#     vote_roll_calls.append(vote_roll_call)
