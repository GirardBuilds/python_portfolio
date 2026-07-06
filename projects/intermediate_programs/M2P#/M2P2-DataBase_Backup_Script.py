'''
M2P2 — Database Backup Script. 
Copies quizchime_copy.db to a backups/ folder with a timestamped filename (quizchime_2026-07-08_0900.db), 
deletes all but the newest 10. 
Skills: shutil, os.path, datetime (Ch. 10–11, 19). 
The day a tester's three weeks of review data exists, 
you'll want this running before anything else touches the DB.'''

from pathlib import Path
import shutil, os, sys
from datetime import datetime

data_dir = Path.home() / 'projects' / 'FD'#for testing, purposes only, not needed in final version
os.chdir(data_dir)#for testing, purposes only, not needed in final version
sys.path.append(str(data_dir))#for testing, purposes only, not needed in final version

from db_Copy import  DB_PATH
#print('testing printed data dir= ',data_dir)#for testing, purposes only, not needed in final version
#print('testing printed os path= ',os.path.abspath(DB_PATH))#for testing, purposes only, not needed in final version


now = datetime.now()
timestamp = now.strftime("%Y-%m-%d_%H%M")

backup_dir = Path("backups")
backup_dir.mkdir(parents=True, exist_ok=True)

source_db = DB_PATH#("quizchime_copy.db")os.path.abspath(
backup_filename = f"quizchime_{timestamp}.db"
backup_path = backup_dir / backup_filename

shutil.copy(source_db, backup_path)

backup_files = list(backup_dir.glob("quizchime_*.db"))

all_files=[]

for file in backup_files:
    all_files.append(Path(file).stem)

all_files.sort(reverse=True)#sorted to garantee the most recent files are at the beginning of the list
to_be_deleted = all_files[10:] #tested if theres not enough files, it returns an empty list
#print('\n\n\nall files found',all_files) #remainder of the list after the 10 most recent files

if to_be_deleted:
    for file in to_be_deleted:
        file_path = backup_dir / f"{file}.db"
        if file_path.exists():# might need a try/except block to catch any errors if the file is in use or locked
            print(f"Deleting old backup file: {file_path}")
            file_path.unlink()
else:
    print("No old backup files to delete. Only the 10 most recent backups are kept.")
























