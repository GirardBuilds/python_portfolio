'''
M2P1 - Deck Validator.
Before a CSV goes into the loader, check it:
no blank questions or answers, no duplicate questions, flag questions over ~200 characters (too long for a phone notification).
Prints a report of
what's wrong and on which line. Skills: CSV (Ch. 18), string methods, list/dict logic. You'll run this on every deck you build for testers.
'''
import csv, os, sys
from pathlib import Path


data_dir = Path.home() / 'projects' / 'FD'
file = data_dir / 'QNAtestDeck1.csv'
#file = sys.argv[1]
data_dir.mkdir(parents=True, exist_ok=True)
os.chdir(data_dir)
current_deck = []
full_report = []
seen_questions = {}

def deck_validator(Qattempt,Aattempt,Lnum):
    if not Qattempt:
        MTQ = f"Error on Line {Lnum}     -Can't leave a Question empty. "
        full_report.append(MTQ)
        seen_questions[Qattempt] = Lnum
        return
    if not Aattempt:
        full_report.append(f"Warning you left an Answer empty on Line {Lnum}")
    if len(Qattempt) > 200:
        lenmsg = f"Error on Line {Lnum}     -Question length exceeds 200 chracters, please shorten it to continue"
        full_report.append(lenmsg)
        seen_questions[Qattempt] = Lnum
        return
    if Qattempt in seen_questions.keys():
        line_num = seen_questions[Qattempt]
        full_report.append(f"Error on Line {line_num} & {Lnum} -Duplicate question found ")
        return
    seen_questions[Qattempt] = Lnum

with open(file, 'r', newline='') as f:
    reader = csv.reader(f)
    for row in reader:
        Lnum= reader.line_num
        if reader.line_num == 1:
            continue
        try:
            deck_validator(row[0],row[1],Lnum)
        except IndexError:
            full_report.append(f"Error on Line {Lnum}     -Missing Question or Answer, please check your CSV")
            continue
        

if not full_report:
    print("passed")
    with open(file, 'r', newline='') as f:
        reader = csv.reader(f)
        next(reader)
        current_deck = list(reader)
else:
    print(f"""{Path(file).name} Failed
there are {len(full_report)} issues to be resolved""")
    for i in full_report:
        print(i)


#print("full report= ",full_report)
#print("seen questions= ",seen_questions)
#for q,a in current_deck:
    #print(q)
    #print(a)
#print(current_deck)














