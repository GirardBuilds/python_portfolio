"""
M2P6 - Tester Onboarding Kit. 
Ties it together: 
given a tester's name and a deck CSV, it validates the deck (M2P1's logic), loads it (M2P0's logic), and prints a personalized welcome message you can paste into Telegram.
Skills: importing and reusing your own modules - your LEGO-brick philosophy applied to your own projects for the first time.
"""
import csv, os
from pathlib import Path
import sys

data_dir = Path.home() / 'projects' / 'FD'#for testing, purposes only, not needed in final version
os.chdir(data_dir)#for testing, purposes only, not needed in final version
sys.path.append(str(data_dir))#for testing, purposes only, not needed in final version
print('testing printed data dir= ',data_dir)#for testing, purposes only, not needed in final version

from db_Copy import create_deck, add_card,init_db, upsert_user, DB_PATH
from QC_valid_csv import validate_deck
from QC_loader import load_deck
print('testing printed os path= ',os.path.abspath(DB_PATH))#for testing, purposes only, not needed in final version



batch_file = Path.home() / 'projects' / 'FD' / 'test_group1.csv'
decks_folder = Path.home() / 'projects' / 'FD' / 'test_decks'
if not (batch_file.exists() and batch_file.is_file()):
    print(f"File '{batch_file}' does not exist. Please provide a valid CSV file.")
    sys.exit(0)

errors = []

with open(batch_file, mode='r', newline='', encoding='utf-8') as file:
    reader = csv.reader(file)
    for row in reader:
        Lnum= reader.line_num
        if reader.line_num == 1:
            continue
        is_valid_number = True
        name = row[0].strip()
        try:
            user_number = int(row[1].strip())
        except ValueError:
            is_valid_number = False
            errors.append(f"Invalid user number in row {Lnum}: {row[1]}")

        deck_filename = row[2].strip()
        deck_path = decks_folder / deck_filename
        is_valid_deck, deck_issues = validate_deck(deck_path)
        if not is_valid_deck:
                errors.append(f"Deck validation failed for row {Lnum}: {deck_filename}")
                errors.extend(deck_issues)
        if is_valid_deck and is_valid_number:
            checker = load_deck(deck_path, user_number,name)
            if not checker:
                errors.append(f"Deck loading failed for row {Lnum}: {deck_filename}")
        else:
            errors.append(f"Skipping loading for row {Lnum} due to validation errors.")
        #print(f"Name: {name}, User Number: {user_number}, Deck Filename: {deck_filename}")
if not errors:
    print("All rows processed successfully.")
else:
    with open('onboarding_errors.txt', 'w') as error_file:
        for error in errors:
            error_file.write(error + '\n')










