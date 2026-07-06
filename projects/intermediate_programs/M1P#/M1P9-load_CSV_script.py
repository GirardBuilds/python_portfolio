'''
M1P9 Exam The deck-loader script —
When testers join, you'll want to pre-load a deck into their account (removing deck-creation friction, per the plan).
The script: read a CSV of question,answer rows,
and insert them via the functions already in db.py (create_deck, add_card).
That's file handling + CSV (your Chapter 18 material)
+ calling functions from an imported module
+ a taste of reading someone else's code to figure out an interface.
'''

#decks:  deck_id (auto-number) | owner_id (telegram user id) | name | created_at
#cards:  card_id (auto-number) | deck_id | front | back | created_at

import csv, os
from pathlib import Path
from datetime import datetime, date, timedelta
import sys
import sqlite3

data_dir = Path.home() / 'projects' / 'FD'
file = data_dir / 'QNAtestDeck1.csv'
data_dir.mkdir(parents=True, exist_ok=True)
os.chdir(data_dir)
sys.path.append(str(data_dir))
from db_Copy import create_deck, add_card,init_db, upsert_user, list_decks, delete_deck,get_cards_in_deck,delete_card, DB_PATH

#os.path.abspath("quizchime_copy.db")
print('printed os path= ',os.path.abspath(DB_PATH))

init_db()  # Initialize the database if it doesn't exist
ISO = "%Y-%m-%d %H:%M:%S"
upsert_user(user_id=1234, chat_id=1234, username="test_user")
'user_id       INTEGER PRIMARY KEY,        -- telegram user id'
'owner_id   INTEGER NOT NULL REFERENCES users(user_id)'

owner_id = 1234
picked_deck = Path(file).stem
all_decks = list_decks(owner_id)
deck_id = None

def dupelicate_deck_cleanup():
    global all_decks
    amount = 0
    print("Checking for duplicate decks...")
    quick_return = [deck['name'] for deck in all_decks]
    if list(quick_return) == list(set(quick_return)):
        print("No duplicate decks found.")
        return
    choice2 = input("""Duplicate decks found. Do you want to 
                   [1] save the oldest version 
                   [2] save the newest version (the one most recently created):\n """).strip().lower()
    if choice2 not in ['1', '2']:
        print("Invalid choice. Exiting.")
        sys.exit(0)
    if choice2 == '1':
        seen_namesOld = []
        for deck in all_decks:
            if deck['name'] not in seen_namesOld:
                seen_namesOld.append(deck['name'])
            else:
                print(f"Deck '{deck['name']}' already exists deleting the duplicate deck: ")
                all_cards = get_cards_in_deck(deck['deck_id'])
                for card in all_cards:
                    print(f"Deleting card with ID: {card['card_id']} from deck '{deck['name']}'")
                    delete_card(card['card_id'])
                delete_deck(deck['deck_id'])
                amount += 1
    if choice2 == '2':
        print("Keeping the newest version of each deck.")
        seen_names = {}
        for deck in all_decks:
            seen_names[deck['name']] = deck['deck_id']  # Store the deck_id of the first occurrence
        #print(seen_names)
        for deck in all_decks:
            if deck['name'] in seen_names and seen_names[deck['name']] != deck['deck_id']:
                all_cards = get_cards_in_deck(deck['deck_id'])
                for card in all_cards:
                    print(f"Deleting card with ID: {card['card_id']} from deck '{deck['name']}'")
                    delete_card(card['card_id'])
                print(f"Deck '{deck['name']}' already exists. Deleting the duplicate deck with ID: {deck['deck_id']}")
                delete_deck(deck['deck_id'])
                amount += 1
    print(f"Deleted {amount} duplicate decks.")
    all_decks = list_decks(owner_id)  # Refresh the list of decks after cleanup

dupelicate_deck_cleanup()  # Call the function to clean up duplicate decks

while True:
    for deck in all_decks:
        #print(f"Deck: {deck['name']}")
        if  deck['name'] == picked_deck:
            print(f"Deck '{picked_deck}' already exists for user {owner_id}.")
            choice = input("Do you want to \n[1] load the existing deck?\n[2] replace the existing deck with the new one?:\n ").strip().lower()
            if choice not in ['1', '2']:
                print("Invalid choice. try again.")
                continue
            if choice == '1':
                deck_id = deck['deck_id']#)get_deck(owner_id, 
                print(f"Deck ID: {deck_id}")
                print(f"deck named {deck['name']} already exists loading it...")  
                break 
            if choice == '2':
                print(f"Replacing the existing deck '{picked_deck}' for user {owner_id}.")
                all_cards = get_cards_in_deck(deck['deck_id'])
                for card in all_cards:
                    print(f"Deleting card with ID: {card['card_id']} from deck '{deck['name']}'")
                    delete_card(card['card_id'])
                delete_deck(deck['deck_id'])
                deck_id = None
    break
                
if not deck_id:
    print(f"Creating deck '{picked_deck}' for user {owner_id}.")
    deck_id = create_deck(owner_id, picked_deck)
    current_deck = []
    with open(file, 'r', newline='') as f:
        reader = csv.reader(f)
        next(reader)
        current_deck = list(reader)
    card_codes = []
    for q ,a in current_deck:
        card_id = add_card(deck_id,q,a)
        card_codes.append(card_id)
        print(card_codes)
#csv i was working with
'''
Question,Answer
Q1,A1
Q2,A2
Q3,A3
Q4,A4
Q5,A5
'''







