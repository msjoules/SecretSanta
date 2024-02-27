'''
This program is used to randomize players for Secret Santas.

There are two ways you can get player names:
    1) Generate names from an Excel document where each player has his/her own
        sheet
    2) Manually entering each player's name
'''

import os
import players
import pandas as pd
from santa import SecretSanta 

os.system('clear')

print('🎄WELCOME TO THE SECRET SANTA PROGRAM!🎄'
      '\n\nThis program randomizes players for Secret Santa. '
      'Would you like to proceed?')

start_program = True

while start_program:
    proceed = input("\nType 'no' or 'yes':  ").strip()

    if proceed.lower() == 'no':
        print('\nOk. Bye!')
        break
    elif proceed.lower() == 'yes':
        print('''\n\nThere are three ways you can get player names:
        1) Generate names from an Excel document where each player has his/her own sheet
        2) Generate names from a json file
        3) Manually entering each player's name\n\n''')
        
        # Import player names or manually enter them
        while True:
            player_entry = input("\nEnter '1' for Excel Spreadsheet\n"
                                "Enter '2' for json file\n"
                                "Enter '3' to enter names manually\n"
                                "Enter '4' to exit the program\n"
                                "What is your choice?  ").strip()
            
            if player_entry == '4':
                print('\nUser request to EXIT.')
                # names = ''
                start_program = False
                break

            # Option 1: Import names from Excel spreadsheet
            elif player_entry == '1':
                names = players.excel_import()
                break

            # Option 2: Import names from a json file
            elif player_entry == '2':             
                names = players.json_import()
                break

            # Option 3: Manually enter names        
            elif player_entry == '3':
                names = players.manual_entry()
                break

            # Handle invalid entries
            else:
               print('\nInvalid Entry.')
           
        if not start_program:
            break

        players.print_names(names)

        # Instantiate Santa Class
        santa = SecretSanta(names)

        # Allow changes if necessary
        while True:
            make_changes = input("\nWould you like to make any changes?\n"
                                "Enter 'no' or 'yes':  ").strip()
        
            if make_changes.lower() == 'no':
                print('\n*------------------*'
                    '\n* Names Finalized! *'
                    '\n*------------------*')
                break
            elif make_changes.lower() == 'yes':
                # santa = SecretSanta(names)
                names = santa.edit_names()
                break
            # Handle invalid entries
            else:
                print('\nInvalid Entry.')

        if not names:
            print('\nNo names in list.')
            start_program = False
            break

        # Option to save list as json file
        players.save_players(names)

        # Secret Santa randomized assignments
        print("\n\nNow we are going to randomly assign Santas to Players. "
            "To keep the list a secret, the results will not be printed.\n")
        input("Hit the 'Enter' key when you're ready: ")

        santas = santa.pair_players()

        print('\n\nYou can now print out the Santa-Player pairs.\n'
            'If you are also participating, you may want to ask someone else '
            'to take a look at the list.\n'
            'You can also go ahead and attempt to automate the emailing '
            'process without looking at the list.\n'
            "Let's address the Santa-Player list first.")
        pair_peek = input('\nWould you like to print the Santa-Player pairs? '
                        "\nType 'no' or 'yes':  ").strip()
        
        if pair_peek.lower() == 'no':
            print('\nOk. Santa-Player pairs hidden.')
        elif pair_peek.lower() == 'yes':
            print('\n')
            santas_players = {'SANTA':santas, 'RECIPIENT':names}
            santas_players_df = pd.DataFrame(santas_players)
            print(santas_players_df)
        # Handle invalid entry on printing Santa-Recipient list
        else:
            print('\nNo choice, means no peek 👀... moving on.\n')

        setup_emails = True

        while setup_emails:
            # Set up email option
            auto_email = input('\nWould you like to attempt to email the '
                            "participants? \nEnter 'no' or 'yes':  ").strip()
            
            if auto_email.lower() == 'no':
                print('\nOk, bye!')
                start_program = False
                break
            elif auto_email.lower() == 'yes':
                print("\nYou will now be prompted to enter the email address "
                    "of the players.\nDon't worry if you make a mistake, you'll "
                    "have a chance to fix it later.\n")
                santa = SecretSanta(names, santas)
                emails = santa.get_email_addresses()
                se_data = {'Santa':santas, 'Email Address':emails}
                se_df = pd.DataFrame(se_data)

                os.system('clear')

                # Allow changes if necessary
                print("\nThis is one final check prior to initiating the auto email "
                    f"function of this program:\n{se_df}"            
                    "\n\nMake sure you have set up the Gmail account that is being "
                    "used to send the emails correctly.\nThis means:\n"
                    "1) Having 2-factor authentication set up\n"
                    "2) Obtaining an APP password\n"
                    "3) Once successful, deleting your APP password for security")
                
                while True:
                    proceed_to_email = input(
                        "\nWould you like to proceed with the auto-email portion of "
                        "this program?\nEnter 'no' or 'yes':  "
                        ).strip()
                    
                    if proceed_to_email.lower() == 'no':
                        print('\nOk')
                        start_program = False
                        break
                    elif proceed_to_email.lower() == 'yes':
                        santa = SecretSanta(names, santas, emails)
                        santa.email_players()
                        print("\nCongratulations!  You're done with your Secret "
                            "Santa duties!\n\n"
                            "DON'T FORGET TO DELETE YOUR APP PASSWORD!!!!")
                        start_program = False
                        break
                    # Handle invalid entries to proceed with auto-emailing
                    else:
                        print('\nInvalid Entry.')
                setup_emails = False
            # Handle invalid entries for player entry option
            else:
                print('\nInvalid Entry.')
    # Handle invalid entries for main program
    else:
        print('\nInvalid entry. Try again.')

print('\nProgram exit.')
