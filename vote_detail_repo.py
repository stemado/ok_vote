import sqlite3



# Assuming conn is a global variable or passed as a parameter
conn = sqlite3.connect('vote_detail.db')

def insert_vote_detail(vote_detail):
    try:
        with conn:  # Using context manager for automatic commit/rollback
            conn.execute('''
            INSERT INTO votes (unique_index, bill_number, vote_type, yea, nay, cp, excused, vacant, result, location, date, time)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (vote_detail.unique_index, vote_detail.bill_number, vote_detail.vote_type, vote_detail.yea,
                  vote_detail.nay, vote_detail.cp, vote_detail.excused, vote_detail.vacant, vote_detail.result,
                  vote_detail.location, vote_detail.date, vote_detail.time))
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
