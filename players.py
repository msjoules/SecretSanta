import pandas as pd
import json
import os
import platform
from datetime import datetime
from pathlib import Path

def print_names(names):
    print(f'\nThere are a total {len(names)} people playing.\n')
    for i, v in enumerate(names):
        print(f'{i}: {v}')

def excel_import():
    while True:
        filepath = input('\nEnter the complete path to the spreadsheet '
        '(e.g., /home/user/secretsanta.xlsx or '
        'C:\\Documents\\secretsanta.xlsx)\n'
        'Path:  ').strip()

        os.system('clear')
        print(f'\nUser entered path to Excel document: {filepath}\n')
        
        if (filepath.startswith('"') and filepath.endswith('"')) or \
            (filepath.startswith("'") and filepath.endswith("'")):
            
            filepath = filepath[1:-1]
            
        try:
            db = pd.ExcelFile(filepath)
        # Handle exception
        except:
            print('You must have entered something incorrectly.  '
                    'Please verify the path and try again.')
        else:
            names = db.sheet_names
            names = [names[i].capitalize() for i in range(len(names))]
            return names
            break

def json_import():
    while True:
        filepath = input('\nEnter the complete path to the json file '
                    '(e.g., /home/user/secretsanta.json or '
                    'C:\\Documents\\secretsanta.json)\n'
                    'Path:  ').strip()
        
        os.system('clear')
        print(f'\nUser entered path to json file: {filepath}\n')
        
        if (filepath.startswith('"') and filepath.endswith('"')) or \
            (filepath.startswith("'") and filepath.endswith("'")):
            
            filepath = filepath[1:-1]
            
        try:
            db = Path(filepath).read_text()
        # Handle exception
        except:
            print('You must have entered something incorrectly.  '
                    'Please verify the path and try again.')
        else:
            names = json.loads(db)
            names = [names[i].capitalize() for i in range(len(names))]
            return names

def manual_entry():
    os.system('clear')
    print("\nYou chose to enter the player names individually.\n"
          "Don't worry if you mess up. Just keep going. You will be "
          "able to edit it later.\n")
    names = []

    while True:
        name = input("Please enter the player's name (Enter 'STOP' when"
                    " done):  ").strip()
        
        if name.upper() == 'STOP':
            break
        # Handle blank entries
        elif name == '':
            print('The name cannot be blank.')
            continue
        else:
            names.append(name.capitalize())
        
    return names

def save_players(names):
    saveornot = input("\n\nWould you like to save the Secret Santa list?\n"
                          "Enter 'no' or 'yes':  ").strip()
        
    if saveornot == 'no':
        print('\nOk!')
    else:
        cwd = os.getcwd()

        # Account for Windows using differnt slashes
        platos = platform.system()
        if platos == 'Windows':
            slash = '\\'
        else:
            slash = '/'
        
        year = str(datetime.now().year)
        filename = cwd + slash + 'secretsanta-' + year +'.json'
        path = Path(filename)
        names_json = json.dumps(names)
        path.write_text(names_json)

        print(f'\n\nSecret Santa list saved to:  {filename}')

