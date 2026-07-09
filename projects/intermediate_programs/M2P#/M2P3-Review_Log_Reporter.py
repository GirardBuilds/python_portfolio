'''
M2P3 - Review Log Reporter.
Reads the reviews table and prints per-user, per-day answer counts plus each user's last-seen date - your ghosting detector.
This is the script that answers your kill/continue question. Skills: the sqlite3 module.

The SQL queries are already written in the README; your job is wrapping them in Python.

The kill/continue metrics live in the reviews table. Useful queries:
'''

from pathlib import Path
import sqlite3,os,sys
from datetime import datetime, date, timedelta
from contextlib import contextmanager

data_dir = Path.home() / 'projects' / 'FD'#for testing, purposes only, not needed in final version
os.chdir(data_dir)#for testing, purposes only, not needed in final version
sys.path.append(str(data_dir))#for testing, purposes only, not needed in final version
print('testing printed data dir= ',data_dir)#for testing, purposes only, not needed in final version
#
from db_Copy import  DB_PATH, init_db,conn

init_db()

print('testing printed os path= ',os.path.abspath(DB_PATH))#for testing, purposes only, not needed in final version

SCHEMA = """
CREATE TABLE IF NOT EXISTS reviews (
    review_id  INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id    INTEGER NOT NULL,
    card_id    INTEGER NOT NULL,
    result     TEXT NOT NULL,          -- got_it | missed | skip
    reviewed_at TEXT NOT NULL
);
"""


def answers_per_user_per_day(): #added to db_Copy
    with conn() as c:
        return c.execute("""
            SELECT user_id, DATE(reviewed_at) d, COUNT(*) answered
            FROM reviews GROUP BY user_id, d ORDER BY d;
        """).fetchall()

def last_seen_per_user(): #added to db_Copy
    with conn() as c:
        return c.execute("""
            SELECT users.user_id, MAX(reviewed_at) last_seen
            FROM users LEFT JOIN reviews ON users.user_id = reviews.user_id
            GROUP BY users.user_id ORDER BY last_seen DESC;
        """).fetchall()



def print_kill_continue_report():
    print(f"from {DB_PATH} - kill/continue report")
    print("Answers per user per day:")
    for user_id, d, answered in answers_per_user_per_day():
        print(f"User {user_id} on {d}: {answered} answers")

    print("\nLast seen per user:")
    for user_id, last_seen in last_seen_per_user():
        if not last_seen:
            print(f"User {user_id} has never answered any questions.")
            continue
        last_seen_date = datetime.strptime(last_seen, "%Y-%m-%d %H:%M:%S")
        days_ago = (datetime.now() - last_seen_date).days
        print(f"User {user_id} last seen: {last_seen} ({days_ago} days ago)")


print_kill_continue_report()











