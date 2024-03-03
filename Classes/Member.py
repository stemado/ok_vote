class Member:
    """
    A class representing a member of a legislative body, either the House or the Senate.
    """

    def __init__(self, unique_index, chamber, district, member_name, title):
        """
        Initialize the Member class with given properties.

        :param unique_index: A unique index that may be used as a database key.
        :param chamber: Chamber of the legislative body (House or Senate).
        :param district: District number of the member.
        :param member_name: Name of the member.
        :param title: The title of the member
        """
        self.unique_index = unique_index
        self.chamber = chamber
        self.district = district
        self.member_name = member_name
        self.title = member_name

    def __str__(self):
        return f"Member({self.unique_index}, {self.chamber}, {self.district}, {self.member_name}, {self.title})"

