import time
import os
import pickle

class AdminHome():
    def __init__(self):
        self.accounts = self.load_accounts()
        self.list_commands()
        self.handle_command()

    # Fancy home formatting
    def home_info(self):
        print('''
█ █ █ █▀▀ █   █▀▀ █▀█ █▀▄▀█ █▀▀   ▄▀█ █▀▄ █▀▄▀█ █ █▄ █
▀▄▀▄▀ ██▄ █▄▄ █▄▄ █▄█ █ ▀ █ ██▄   █▀█ █▄▀ █ ▀ █ █ █ ▀█
        ''')
        print('*'*9)
        print(' WARNING')
        print('*'*9)
        print('The ADMIN page is powerful--Do not abuse this.')
        print('With great POWER comes great RESPONSIBILITY!')

    # Lists possible commands
    def list_commands(self):
        self.home_info()
        print('\nType the number that corresponds to the action you want to take:')
        print('---------------------------------')
        print('( 1 ) -- View Commands')
        print('( 2 ) -- View Created Accounts')
        print('( 3 ) -- View Account Info')
        print('( 4 ) -- Remove an Account')
        print('( 0 ) -- Log out')
        print('---------------------------------')

    # Handles what to do based on a user inputted command
    def handle_command(self):
        while True:
            command = input('<ADMIN> Type your command: ')
            print()
            if command == '0':
                print(f'Exiting ADMIN Account!')
                time.sleep(1.5)
                os.system('cls' if os.name == 'nt' else 'clear')
                os.system('python main.py')
                break
            elif command == '1':
                self.clear('')
            elif command == '2':
                self.clear(command)
                self.view_accounts()
                break
            elif command == '3':
                self.clear(command)
                self.view_account_info()
                break
            elif command == '4':
                self.clear(command)
                self.remove_account()
                break
            else:
                print('Invalid command, try again\n')

    # Clears the screen and sets up GUI
    def clear(self, command):
        os.system('cls' if os.name == 'nt' else 'clear')
        self.list_commands()
        if command == '':
            self.handle_command()
        else:  
            print(f'<ADMIN> Type your command: {command}\n')

    # Pauses program until user presses ENTER key
    def enter(self):
        print('\nPress ENTER to Continue')
        if input('') == '':
            self.clear('')

    # Saves self.accounts to accounts.txt
    def save_accounts(self):
        with open('accounts.txt', 'wb') as accounts_file:
            pickle.dump(self.accounts, accounts_file)

    # Loads account from accounts.txt
    def load_accounts(self):
        with open('accounts.txt', 'rb') as accounts_file:
            try:
                accounts = pickle.load(accounts_file)
            except EOFError:
                return []
            return accounts

    # Displays limited info on each account created
    def view_accounts(self):
        for account in self.accounts:
            print(account.get_name().upper())
            print(account.get_email())
            print(account.get_account_num())
            print('*'*14)
        self.enter()

    # Check to see if an account exists based on Acc #
    def account_exists(self):
        self.account_num = input('Account Number: ')
        exists = False
        for account in self.accounts:
            if self.account_num == str(account.get_account_num()):
                exists = True
                break
        return exists, account

    # View the account info of a single account
    def view_account_info(self):
        acc_exists = self.account_exists()
        if acc_exists[0] == True:
            print()
            acc_exists[1].display_all_info()
        else:
            print('No Account Exists')
        self.enter()

    # 108156156729
    # Remove an account from a list of accounts
    def remove_account(self):
        acc_exists = self.account_exists()
        if acc_exists[0] == True:
            print(f'Delete {acc_exists[1].get_name().upper()}\'s Account?')
            confirm = input('Confirm [y/n]: ').lower()
            if confirm == 'y':
                for account in self.accounts:
                    if self.account_num == str(account.get_account_num()):
                        self.accounts.remove(account)
                        self.save_accounts()
                        print(f'{acc_exists[1].get_name().upper()}\'s Account Removed')
                        break
        else:
            print('No Account Exists')
        self.enter()
        