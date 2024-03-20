import csv
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


    def export_vote_details_to_csv(self, csv_file_path):
        try:
            with self.conn:
                cursor = self.conn.cursor()
                cursor.execute("SELECT * FROM vote_details")
                rows = cursor.fetchall()

                with open(csv_file_path, 'w', newline='') as file:
                    csv_writer = csv.writer(file)
                    # Write the headers
                    csv_writer.writerow([i[0] for i in cursor.description])
                    # Write the data
                    csv_writer.writerows(rows)
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")

    def export_vote_roll_call_to_csv(self, csv_file_path):
        try:
            with self.conn:
                cursor = self.conn.cursor()
                cursor.execute("SELECT * FROM vote_roll_call")
                rows = cursor.fetchall()

                with open(csv_file_path, 'w', newline='') as file:
                    csv_writer = csv.writer(file)
                    # Write the headers
                    csv_writer.writerow([i[0] for i in cursor.description])
                    # Write the data
                    csv_writer.writerows(rows)
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")

    def insert_vote_roll_call(self, vote_roll_call_dict):
        try:
            with self.conn:  # Using context manager for automatic commit/rollback
                self.conn.execute('''
                   INSERT INTO vote_roll_call (UniqueIndex, VotesDetailIndex, BillNumber, Member, Vote, Type, Location, Date, Time)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                   ''', (
                    None,  # SQLite auto-generates the unique index
                    vote_roll_call_dict['VotesDetailIndex'],
                    vote_roll_call_dict['BillNumber'],
                    vote_roll_call_dict['Member'],
                    vote_roll_call_dict['Vote'],
                    vote_roll_call_dict['Type'],
                    vote_roll_call_dict['Location'],
                    vote_roll_call_dict['Date'],
                    vote_roll_call_dict['Time']
                ))
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
