import sqlite3

ok_db = 'identifier.sqlite'

class DbContext:
    def __init__(self):
        self.conn = sqlite3.connect(ok_db)

    def insert_vote_detail(self, vote_detail_dict):
        try:
            with self.conn:  # Using context manager for automatic commit/rollback
                self.conn.execute('''
                   INSERT INTO vote_details (unique_index, bill_number, vote_type, yea, nay, cp, excused, vacant, result, location, date, time)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                   ''', (
                    None,  # SQLite auto-generates the unique index
                    vote_detail_dict['bill_number'],
                    vote_detail_dict['vote_type'],
                    vote_detail_dict['yea'],
                    vote_detail_dict['nay'],
                    vote_detail_dict['cp'],
                    vote_detail_dict['excused'],
                    vote_detail_dict['vacant'],
                    vote_detail_dict['result'],
                    vote_detail_dict['location'],
                    vote_detail_dict['date'],
                    vote_detail_dict['time']
                ))
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")


