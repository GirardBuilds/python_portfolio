'''
M2P4 - Stats Digest Generator. 
Builds on M2P3: writes a weekly summary to a text file - total answers, accuracy trend, streaks, most-missed cards. 
Skills: file writing, string formatting, basic aggregation. 
This becomes the thing you glance at every Monday instead of squinting at raw tables.
'''
from pathlib import Path
import os,sys
from datetime import datetime
#from contextlib import contextmanagersqlite3, date, timedelta

data_dir = Path.home() / 'projects' / 'FD'#for testing, purposes only, not needed in final version
os.chdir(data_dir)#for testing, purposes only, not needed in final version
sys.path.append(str(data_dir))#for testing, purposes only, not needed in final version
print('testing printed data dir= ',data_dir)#for testing, purposes only, not needed in final version
#
from db_Copy import  DB_PATH, init_db, last_seen_per_user, stats

init_db()

print('testing printed os path= ',os.path.abspath(DB_PATH))#for testing, purposes only, not needed in final version


now =datetime.now()
time_date = now.strftime("%Y-%m-%d")
file_report = data_dir / 'weekly_reports'  #f"weekly_digest_{time_date}.txt"      Path(__file__).parent
file_report.mkdir(parents=True, exist_ok=True)  # Ensure the directory exists


file_name = file_report / f"weekly_digest_{time_date}.txt"  # Full path to the report file
#file_path.write_text(f"Weekly Digest Report - {time_date}\n")

def generate_weekly_digest():
    with open(file_name, 'w',encoding='utf-8') as f:
        f.write(f"Weekly Digest Report - {time_date}\n")
        f.write("="*40 + "\n\n")
        for user_id, last_seen in last_seen_per_user():
            if not last_seen:
                f.write("*"*40 + "\n\n")
                f.write(f"User {user_id} has never answered any questions.\n\n")
                f.write("*"*40 + "\n\n")
                continue
            user_stats = stats(user_id)
            f.write(f"User {user_id}: | Last Seen: {last_seen} | Total Answers: {user_stats['total']}\n")
            f.write(f"Due Now: {user_stats['due_now']} | Streak: {user_stats['streak']} | Accuracy: {user_stats['accuracy']}\n")
            f.write("-"*40 + "\n\n")
    print(f"Weekly digest report generated at: {file_name}")

generate_weekly_digest()






















