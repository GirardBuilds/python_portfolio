"""
M2P5 - Ping Timing Analyzer. 
From the reviews log, figure out when answers happen: 
which hours of day get responses, how long after a ping people answer 
(compare reviewed_at timestamps against expected ping windows). 
Skills: datetime math, dictionaries as counters. 
Directly feeds the "pacing is a core design decision" warning from your research doc.
"""
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
ISO = "%Y-%m-%d %H:%M:%S"
print('testing printed os path= ',os.path.abspath(DB_PATH))#for testing, purposes only, not needed in final version

SCHEMA = """
CREATE TABLE IF NOT EXISTS ping_sent (
    ping_id     INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id     INTEGER NOT NULL REFERENCES users(user_id),
    card_id     INTEGER NOT NULL REFERENCES cards(card_id),
    sent_at     TEXT NOT NULL
);
"""
def log_ping_sent(user_id: int, card_id: int):
    with conn() as c:
        c.execute(
            "INSERT INTO ping_sent (user_id, card_id, sent_at) VALUES (?, ?, ?)",
            (user_id, card_id, datetime.now().strftime(ISO)),
        )


def analyze_ping_response_times():
    with conn() as c:
        # This query pairs each ping_sent with the first review that matches the same user_id and card_id, 
        # where the review's reviewed_at is after the ping's sent_at.
        results = c.execute("""
            SELECT p.ping_id, p.user_id, p.card_id, p.sent_at, r.reviewed_at
            FROM ping_sent p
            LEFT JOIN reviews r ON p.user_id = r.user_id AND p.card_id = r.card_id AND r.reviewed_at > p.sent_at AND r.reviewed_at = (
                SELECT MIN(r2.reviewed_at)
                FROM reviews r2
                WHERE r2.user_id = p.user_id AND r2.card_id = p.card_id AND r2.reviewed_at > p.sent_at
            )
            ORDER BY p.sent_at;
        """).fetchall()

    response_times = []
    for ping_id, user_id, card_id, sent_at, reviewed_at in results:
        if reviewed_at:
            sent_time = datetime.strptime(sent_at, ISO)
            review_time = datetime.strptime(reviewed_at, ISO)
            response_gap = (review_time - sent_time).total_seconds() / 60  # Convert to minutes
            response_times.append(response_gap)
        else:
            response_times.append(None)  # No response

    return response_times

def generate_ping_response_report():
    response_times = analyze_ping_response_times()
    report_file = data_dir / 'ping_response_report.txt'
    
    within_5_min = sum(1 for gap in response_times if gap is not None and gap < 5)
    within_15_min = sum(1 for gap in response_times if gap is not None and gap >= 5 and gap < 15)
    within_30_min = sum(1 for gap in response_times if gap is not None and gap >= 15 and gap < 30)
    within_60_min = sum(1 for gap in response_times if gap is not None and gap >= 30 and gap < 60)
    over_60_min = sum(1 for gap in response_times if gap is not None and gap >= 60)
    no_response = sum(1 for gap in response_times if gap is None)
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write("Ping Response Times Report\n")
        f.write("="*40 + "\n\n")
        f.write(f"Total\n")
        f.write(f"Total pings sent: {len(response_times)}\n")
        f.write(f"Within 5 minutes: {within_5_min}\n")
        f.write(f"Within 15 minutes: {within_15_min}\n")
        f.write(f"Within 30 minutes: {within_30_min}\n")
        f.write(f"Within 60 minutes: {within_60_min}\n")
        f.write(f"Over 60 minutes: {over_60_min}\n")
        f.write(f"No response: {no_response}\n")
    print(f"Ping response report generated at: {report_file}")







