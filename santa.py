class SecretSanta:
    # Initialize
    def __init__(self, names=None, santas=None, emails=None):
        self.names = names
        self.santas = santas
        self.emails = emails
    
    # Function allows user to edit player names
    def edit_names(self):
        import os
        # Keep the original list intact for comparison when editing
        original_list = list(self.names)

        # Menu of user options
        while True:
            make_changes = input(
                "\nEnter '1' to EDIT a player\n"
                "Enter '2' to DELETE a player\n"
                "Enter '3' to ADD a player\n"
                "Enter '4' to PRINT ORIGINAL LIST of players\n"
                "Enter '5' to PRINT UPDATED LIST of players -- you might want " 
                "to do this prior to exiting\n"
                "Enter '6' to make NO CHANGES\n"
                "What is your choice?  "
                ).strip()
            
            if make_changes == '6':
                break                   
            elif make_changes == '1':
                try:
                    edit_player = input('\nEnter the NUMBER corresponding to ' 
                                        'the player you would like to CHANGE:  '
                                        ).strip()
                    new_player = input(f'\nWhat NAME would you like to change '
                                        f'player number {edit_player} to? '
                                        ).strip()
                    # Handle blank entries
                    if new_player == '':
                        print('\nThe name cannot be blank.')
                    else:
                        self.names[int(edit_player)] = new_player.capitalize()
                        print(f'\nPlayer number {edit_player} is now '
                              f'{new_player.capitalize()}.')
                # Handle exception
                except:
                    print('\nInvalid Entry for option 1')
            elif make_changes == '2':
                try:
                    del_player = input('\nEnter the NUMBER corresponding to ' 
                                        'the player you would like to DELETE:  '
                                        ).strip()
                    del_player_name = self.names[int(del_player)]
                    self.names.remove(self.names[int(del_player)])
                    print(f'\n{del_player_name} DELETED.')
                # Handle exception
                except:
                    print('\nInvalid Entry for option 2')
            elif make_changes == '3':
                try:
                    add_player = input('\nEnter the player NAME you would like '
                                    'to ADD:  ').strip()
                    # Handle blank entries
                    if add_player == '':
                        print('\nThe name cannot be blank.')
                    else:
                        self.names.append(add_player.capitalize())
                        print(f'\n{add_player.capitalize()} has been ADDED to the list.')
                # Handle exception        
                except:
                    print('\nInvalid Entry for option 3')
            elif make_changes == '4':
                os.system('clear')
                print(f'\nThere are a total {len(original_list)} people playing '
                      'in the ORIGINAL LIST:')
                for i, v in enumerate(original_list):
                    print(f'{i}: {v}')
            elif make_changes == '5':
                os.system('clear')
                print(f'\nThere are a total {len(self.names)} people playing '
                      'in the UPDATED LIST:')
                for i, v in enumerate(self.names):
                    print(f'{i}: {v}')

        return self.names

    # Function pairs players - one as Santa & other as recipient
    def pair_players(self):
        import random

        # Make a copy of players
        santas = list(self.names)

        # Create the pairs
        while True:
            # Randomize the lists
            print('\nShuffling names and attempting to pair...')
            random.shuffle(self.names)
            random.shuffle(santas)

            # Set restart to false, assuming the randomization is correct to 
            # begin with
            restart = False

            # Check if the randomization is correct; if not, need to restart to 
            # re-randomize
            for i, v in enumerate(self.names):
                if santas[i] == self.names[i]:
                    print(f"\nRESTARTING: santas and names can't be the same...")
                    restart = True
                    break
            if restart == False:
                print('\n*---------------------*'
                      '\n* Pairing Successful! *'
                      '\n*---------------------*')
                break

        return santas
    
    # Function used to get player email addresses
    def get_email_addresses(self):
        import pandas as pd
        import os

        emails = []

        for i in range(len(self.santas)):
            email = input(f"Please enter the email address for "
                            f"{self.santas[i]}:  ").strip()
            emails.append(email)

        se_data = {'Santa':self.santas, 'Email Address':emails}
        se_df = pd.DataFrame(se_data)
        print("\nHere is the complete list of santa names and email addresses:\n"
              f"{se_df}\n\nWould you like to make any changes? ")
        
        while True:
            make_changes = input(
                "\nEnter '1' to EDIT a player's email address\n"
                "Enter '2' to PRINT UPDATED LIST of santas and their email "
                "adresses\n"
                "Enter '3' to make NO CHANGES\n"
                "\nWhat is your choice?  "
                ).strip()
            
            if make_changes == '3':
                print('\nOk.')
                break
            elif make_changes == '1':
                change_email = input(
                    '\nEnter the NUMBER corresponding to the '
                    'Santa-Email Address pair:  '
                ).strip()
                try:
                    new_email = input(
                        "Enter the NEW EMAIL address for "
                        f"{self.santas[int(change_email)]}:  ")
                    emails[int(change_email)] = new_email
                # Handle exception
                except:
                    print('\nInvalid entry.')
            elif make_changes == '2':
                os.system('clear')
                se_data = {'Santa':self.santas, 'Email Address':emails}
                se_df = pd.DataFrame(se_data)
                print("\nHere is the complete list of santa names and email "
                      f"addresses:\n{se_df}")
            else:
                print('\nInvalid entry.')

        return emails     
    
    # Function auto mass email using 1 main user account
    # Main user email account must have APP permissions set up
    def email_players(self):
        import os
        import getpass
        import smtplib
        from email.mime.multipart import MIMEMultipart
        from email.mime.text import MIMEText

        while True:
            email_user = getpass.getpass(
                prompt='Please enter your email (text hidden) or CTRL+C to abort: '
                )
            email_password = getpass.getpass(
                prompt='Please enter your password (text hidden) or CTRL+C to abort: '
                )

            # Set the email and password as environment variables
            os.environ['EMAIL_USER'] = email_user
            os.environ['EMAIL_PASSWORD'] = email_password

            # Ensure the server is closed after we're done
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                try:
                    server.login(os.getenv('EMAIL_USER'), os.getenv('EMAIL_PASSWORD'))

                    for email, santa, name in zip(self.emails, self.santas, self.names):
                        msg = MIMEMultipart()
                        msg['From'] = os.getenv('EMAIL_USER')
                        msg['To'] = email
                        msg['Subject'] = 'Secret Santa'
                        body = f'Hello {santa}!  You are the Secret Santa for {name}.'
                        msg.attach(MIMEText(body, 'plain'))
                        text = msg.as_string()
                        try:
                            server.sendmail(os.getenv('EMAIL_USER'), email, text)
                        # Handle exception
                        except:
                            print(f"\nFailed to send email to {email}.")
                    break
                # Handle exception
                except:
                    print('\nIncorrect user credentials.')
            

        # Delete the environment variables
        del os.environ['EMAIL_USER']
        del os.environ['EMAIL_PASSWORD']
