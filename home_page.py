import time
import os
import pickle

# Root: 232502654266
# Toor: 894016400758
class Home:
    def __init__(self, logged_in_account):
        self.account = logged_in_account
        self.accounts = self.load_accounts()
        
        self.home_info()
        time.sleep(1)

        self.view_acc_num()
        self.view_balances()

        self.transfer_info()
        
        self.list_commands()
        self.handle_command()


    def home_info(self):
        print(f'Welcome {self.account.get_name().title()},')
        print('This is your HOME PAGE. Here you can CONTROL your ACCOUNT BALANCES')
        print('as well as TRANSFER MONEY between your accounts and even to other people\'s!')
        print('When prompted, please input the number that corressponds with what you')
        print('would like to do. If at any time you are unsure of what to do simply type')
        print('"1" into the command prompt, this will display a list of accepted commands.')

        
    # Loads list of accounts from accounts.txt but gets rid of account the current
    #  account, in order to allow the updating of the account if a deposit, withdraw, etc.
    #  is made. If we did not remove the account, trying to add it would result in an
    #  error as there would be two accounts with the same information.
    def load_accounts(self):
        with open('accounts.txt', 'rb') as accounts_file:
            accounts = pickle.load(accounts_file)
            for account in accounts:
                if account.get_email() == self.account.get_email():
                    accounts.remove(account)
                    break
            return accounts


    # Saves the new state of the accounts list with the updated account data
    # to accounts.txt
    def save_accounts(self):
        with open('accounts.txt', 'wb') as accounts_file:
            pickle.dump(self.accounts, accounts_file)


    # Saves changes caused by the various functions of the account class
    # Completely different from save_accounts()
    def save_changes(self):
        self.accounts.append(self.account)
        self.save_accounts()
        time.sleep(1.5)
        self.clear('')
            

    # Prints acceptable commands, simple as that
    def list_commands(self):
        print('\nType the number that corresponds to the action you want to take:')
        print('----------------------------------------------')
        print('( 1 ) -- Get a list of accepted commands')
        print('( 2 ) -- View your ledger')
        print('( 3 ) -- Deposit money')
        print('( 4 ) -- Withdraw money')
        print('( 5 ) -- Transfer money')
        print('( 0 ) -- Log out')
        print('----------------------------------------------')


    # Gets command from user and runs other functions based on which command is inputted
    def handle_command(self):
        while True:
            command = input('<HOME> Type your command: ')
            print()
            if command == '0':
                print(f'See you later, {self.account.f_name.title()}!')
                time.sleep(1.5)
                os.system('cls' if os.name == 'nt' else 'clear')
                os.system('python main.py')
                break
            elif command == '1':
                self.clear('')
            elif command == '2':
                self.clear(command)
                self.view_ledger()
                break
            elif command == '3':
                self.clear(command)
                self.deposit()
                break
            elif command == '4':
                self.clear(command)
                self.withdraw()
                break
            elif command == '5':
                self.clear(command)
                self.transfer()
                break
            else:
                print('Invalid command, try again\n')


    # Clears the terminal but puts back home info, balances and command list
    # Prints out fake command prompt wih previous command
    def clear(self, command):
        os.system('cls' if os.name == 'nt' else 'clear')
        self.home_info()
        self.view_acc_num()
        self.view_balances()
        self.list_commands()
        if command == '':
            self.handle_command()
        else:  
            print(f'<HOME> Type your command: {command}\n')
                

    # Prints the checking and savings balances of an account
    # After, sends user back to command prompt
    def view_balances(self):
        print('\nYOUR CURRENT BALANCES:')
        print(f'Checking - ${self.account.get_checking_balance()}')
        print(f'Savings  - ${self.account.get_savings_balance()}')


    # Loops through dep_with_history dictionary and prints out each time money was depositted or
    # withdrawn from the account
    def view_ledger(self):
        print('LEDGER:')
        print('  DEPOSITS/WITHDRAWALS')
        if len(self.account.get_dep_with_history()) == 0:
            print('    No deposits/withdrawals have been made to or from this account')
        for key, value in self.account.get_dep_with_history().items():
            if key[:-1] == 'deposit':
                sign = '+'
            else:
                sign = '-'
            if value[1] == 'savings':
                buffer = ' '
            else:
                buffer = ''
            print(f'    *  {value[1].upper()}{buffer} : {sign}{value[0]}$')

        print('  TRANSFERS')
        if len(self.account.get_transfer_history()) == 0:
            print('    No transfered have been made to or from this account')
        
        for key, value in self.account.get_transfer_history().items():
            if len(value) == 4:
                print(f'    *  P2P TRANSFER: -{value[0]}$ ({value[1].upper()} --> {value[2].upper()})')
            elif len(value) == 5:
                print(f'    *  P2P TRANSFER: +{value[0]}$ ({value[2].upper()} --> {value[1].upper()})')
            else:
                print(f'    *  TRANSFER: ${value[0]} ({value[1].upper()} --> {value[2].upper()})')

        print()
        time.sleep(2)
        self.handle_command()
                    
    # Confirms money amount is an integer
    def check_money_int(self):
            while True:
                amount = input('Enter amount: $')
                try:
                    amount = int(amount)
                    return amount
                except ValueError:
                    print('Your input was invalid, try again\n')
        
        
    # Gets which account the user wants to deposit into and how much money to deposit
    # Makes sure an integer is given when inputting money amount
    # Runs deposit_money(), prints confirmation, appends new account to accounts list and save it
    def deposit(self):
        self.accounts = self.load_accounts()
        print('DEPOSIT')
        print('Make deposit into which account?')
        print('( 1 ) - Checking')
        print('( 2 ) - Savings\n')

        while True:
            command = input('Enter: ')
            if command == '1':
                account_type = 'checking'
                
                break
            elif command == '2':
                account_type = 'savings'
                break
            else:
                print('Your input was invalid, try again\n')

        print('\nHow large of a deposit would you like to make?')
        amount = self.check_money_int()

        self.account.deposit_money(account_type, amount)
        print(f'\n${amount} WAS DEPOSITED INTO YOUR {account_type.upper()} ACCOUNT!')
        
        self.save_changes()


    # Allows user to withdraw money from their account granted that they have the available funds
    # Similar to deposit() but runs withdraw_money() instead
    def withdraw(self):
        self.accounts = self.load_accounts()
        print('WITHDRAW')
        print('Make withdrawal from which account?')
        print('( 1 ) - Checking')
        print('( 2 ) - Savings\n')

        while True:
            command = input('Enter command: ')
            if command == '1':
                account_type = 'checking'
                break
            elif command == '2':
                account_type = 'savings'
                break
            else:
                print('Your input was invalid, try again\n')

        print('\nHow large of a withdrawal would you like to make?')
        amount = self.check_money_int()

        if self.account.withdraw_money(account_type, amount):
            print(f'\n${amount} WAS WITHDRAWN FROM YOUR {account_type.upper()} ACCOUNT!')
        else:
            print('Insufficient funds. No money was withdrawn')
        
        self.save_changes()


    # Allows user to view their account number and routing number
    # Important info if they want to recieve money from another user
    def view_acc_num(self):
        print()
        print(f'YOUR ACCOUNT #: {self.account.get_account_num()}')
    

    # Notifies user that they received a transfer and asks them which account
    # they want to send it to
    def transfer_info(self):
        if self.account.get_transfer_balance() == 0:
            pass
        else:
            while True:
                print(f'\nATTENTION: You have been transfered ${self.account.get_transfer_balance()}!')
                print('Where would you like to send the money:')
                print('( 1 ) - Checking')
                print('( 2 )- Savings')
                print()
                send_to = input('Enter: ')
                if self.handle_transfer(send_to) == False:
                    print('Your input was invalid, try again')
                else:
                    self.save_changes()

                    
    # Handles sending transfer money to appropriate account
    def handle_transfer(self, send_to):
        values = list(self.account.transfer_history.values())
        if send_to == '1':
            values[len(self.account.get_transfer_history())-1][1] = 'checking'
            amount = self.account.get_checking_balance() + self.account.get_transfer_balance()
            self.account.set_checking_bal(amount)
            self.account.set_transfer_bal(0)
        elif send_to == '2':
            values[len(self.account.get_transfer_history())-1][1] = 'savings'
            amount = self.account.get_savings_balance() + self.account.get_transfer_balance()
            self.account.set_savings_bal(amount)
            self.account.set_transfer_bal(0)
        else:
            return False

        
    # Allows user to not only transfer money from their checking account to their savings account
    # but also transfer money from their account to another person's account
    def transfer(self):
        self.accounts = self.load_accounts()
        print('TRANSFER')
        print('Where are you planning to transfer your money?')
        print('( 1 ) - Savings <--> Checking')
        print('( 2 ) - To another user\n')  # WIP

        while True:
            command = input('Enter command: ')

            # User chooses 'Savings <--> Checking'
            if command == '1':
                print('\nHow do you want to transfer your money?')
                print('( 1 ) - Checking to Savings')
                print('( 2 ) - Savings to Checking')
                path = input('\nEnter command: ')

                # User choose Checking --> Savings
                if path == '1':
                    print('\nCHECKING --> SAVINGS')
                    print('How much money from your checking would you like to transfer to your savings?')
                    amount = self.check_money_int()
                    if self.account.transfer_money('checking', amount) == True:
                        print(f'\n${amount} FROM YOUR CHECKING WAS TRANSFERED TO YOUR SAVINGS ACCOUNT')
                    else:
                        print('\nInsufficient funds. No money was transfered')
                    
                    self.save_changes()
                    break
                
                # User chooses Savings --> Checking 
                elif path == '2':
                    print('\nSAVINGS --> CHECKING')
                    print('How much money from your savings would you like to transfer to your checking?')
                    amount = self.check_money_int()
                    if self.account.transfer_money('savings', amount) == True:
                        print(f'\n${amount} FROM YOUR SAVINGS WAS TRANSFERED TO YOUR CHECKING ACCOUNT')
                    else:
                        print('\nInsufficient funds. No money was transfered')
                    
                    self.save_changes()
                    break
                    
                else:
                    print('Your input was invalid, try again\n')

            # User chooses 'to another user'       
            # Note: transfer_money_p2p(from_acc, account, amount)
            elif command == '2':
                print('\nP2P TRANSFER')
                print('DISCLAIMER: To transfer money to another user, you will need their ACCOUNT NUMBER\n')

                # Do all the other transfer stuff
                while True:
                    print('TO:')
                    # Checks tha acc_num is 12 digits and doesn't consist of only numbers
                    acc_num = self.check_num_in()
                    
                    # Check if user with that account # exists
                    for saved_account in self.accounts:
                        if saved_account.get_account_num() == acc_num:
                            print(f'\nUser found with account #{acc_num}: {saved_account.get_name().upper()}')
                            confirm = input('Is this who you\'re looking for? (y/n): ')
                            if confirm == 'y' or confirm == 'Y':
                                while True:
                                    print('\nSelect account you would like to transfer money from:')
                                    print('( 1 ) - Checking')
                                    print('( 2 ) - Savings')
                                    command = input('\nEnter command: ')

                                    print(f'\nHow much money would you like to send?')
                                    amount = self.check_money_int()
                                    if command == '1':
                                        if self.account.transfer_money_p2p('checking', saved_account, amount) == True:
                                            print(f'\n${str(amount)} from your CHECKING successfully sent to {saved_account.get_name().upper()}')
                                            
                                            self.save_changes()
                                            break
                                        else:
                                            print('Insufficient funds, no many was transfered')
                                    elif command == '2':
                                        if self.account.transfer_money_p2p('savings', saved_account, amount) == True:
                                            print(f'\n${str(amount)} from your SAVINGS successfully sent to {saved_account.get_name().upper()}')
                                            
                                            self.save_changes()
                                            break
                                        else:
                                            print('Insufficient funds, no many was transfered')
                                    else:
                                        print('Your input was invalid, try again')
                            else:
                                print('\nSorry about that, no other users found with that account #')
                                print('Sending you back to home...')
                                time.sleep(2.5)
                                self.clear('')
                        break
                    print('No users found with that account number, try again\n')
                break
                         
            else:
                print('Your input was invalid, try again\n')

        self.save_changes()


    # Checks to make sure user inputs 12 digit account # and that the number is an int value
    def check_num_in(self):
        while True:
            acc_num = input('Enter User\'s Account #: ')
            try:
                if len(acc_num) != 12:
                    print('Account number too short or too long, no more/less than 12 digits\n')
                    continue
                acc_num = int(acc_num)
                break
            except ValueError:
                    print('Account number included a non-integer value\n')
        return acc_num