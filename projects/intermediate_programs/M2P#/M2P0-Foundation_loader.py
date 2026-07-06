#print('printed os path= ',os.path.abspath(>verify data here<))
'''
M2P0 Foundation -The deck-loader script 
When testers join, you'll want to pre-load a deck into their account (removing deck-creation friction, per the plan).
The script: read a CSV of question,answer rows,
and insert them via the functions already in db.py (create_deck, add_card).
That's file handling + CSV (your Chapter 18 material)
+ calling functions from an imported module
'''

import csv, os
from pathlib import Path
import sys
from db_Copy import create_deck, add_card,init_db, upsert_user, DB_PATH

data_dir = Path.home() / 'projects' / 'FD'#for testing, purposes only, not needed in final version
os.chdir(data_dir)#for testing, purposes only, not needed in final version
sys.path.append(str(data_dir))#for testing, purposes only, not needed in final version
print('testing printed data dir= ',data_dir)#for testing, purposes only, not needed in final version
print('testing printed os path= ',os.path.abspath(DB_PATH))#for testing, purposes only, not needed in final version

try:
    user_number = int(sys.argv[1])
except ValueError:
    print("Invalid user number. Please provide a valid integer.")
    sys.exit(0)
file_name = sys.argv[2]

init_db()
if not (Path(file_name).exists() and Path(file_name).is_file()):
    print(f"File '{file_name}' does not exist. Please provide a valid CSV file.")
    sys.exit(0)

upsert_user(user_id=user_number, chat_id=user_number, username= None )
deck_id = create_deck(user_number,Path(file_name).stem)
current_deck = []
with open(file_name, 'r', newline='') as f:
    reader = csv.reader(f)
    next(reader)
    current_deck = list(reader)
card_codes = []
for q ,a in current_deck:
    card_id = add_card(deck_id,q,a)
    card_codes.append(card_id)
print(len(card_codes),'Cards added from ', Path(file_name).stem)




































