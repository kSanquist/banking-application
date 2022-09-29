# Banking Application
# Kyle Sanquist

# A Simulated banking application that allows you to make accounts and manipulate their balances
# The features that are available:
#  *  Create new accounts
#  *  Log into existing accounts
#  *  View and keep track of your ledger (account history)
#  *  Deposit and Withdraw money
#  *  Transfer money to and from personal accounts as well as other user's accounts
#  *  Email verification (WIP)

# POSSIBLE FEATURES:
#  *  Email verification
#      * Send email to inputted email with verification code
#  *  Daily 6-digit admin passwords sent to email
#  *  Password changing w/ email for accounts

import time
import sys
import pickle
import os
import random
from home_page import Home
from account import Account
from admin_home import AdminHome
import admin_key_gen

def main():
    list_commands()
    command = get_command()
    handle_command(command)


def header(version):
    print('************************')
    print('  BANKING APPLICATION')
    print('   BY Kyle Sanquist')
    print(f'    Version: {version}')
    print('************************\n')


# Prints a list of accepted commands for users
def list_commands():
    print('Type the number that corresponds to the action you want to take:')
    print('-----------------------------------------')
    print('( 1 ) -- Create a new account')
    print('( 2 ) -- Log into an existing account')
    print('( 3 ) -- Exit the program')
    print('-----------------------------------------')


# Gets the command the user enters and checks if the
#  command is acceptable
def get_command():
    _admin_key = admin_key_gen.admin_key
    while True:
        command = input('Type your command: ')
        if command == _admin_key:
            print('\nLOGGING INTO ADMIN ACCOUNT')
            time.sleep(1)
            clear()
            AdminHome()
            break
        elif command == '1' or command == '2' or command == '3':
            return command
        else:
            print('Invalid command, try again')


# Gets acceptable command from get_command() and sends it
#  to individual commands to do their thing
def handle_command(command): 
    if command == '1':
        create_acc()
    elif command == '2':
        log_in()
    elif command == '3':
        print('\nShutting down program...')
        time.sleep(0.5)
        sys.exit(0)


# Saves list of accounts to accounts.txt
def save_accounts():
    with open('accounts.txt', 'wb') as accounts_file:
        pickle.dump(accounts, accounts_file)


# Loads list of accounts from accounts.txt
def load_accounts():
    with open('accounts.txt', 'rb') as accounts_file:
        try:
            accounts = pickle.load(accounts_file)
        except EOFError:
            return []
    return accounts


accounts = []
# Loads account.txt file to update existing accounts just in case another function changes the file info
#  if there is nothing in the file, the file is not loaded as it will throw an error.
# Then grabs info from the user and stores it into a variable, runs through authentication of email,
#  making sure that no two users can share the same email.
# Creates the new Account class with provided credentials, appends it to accounts list, and then saves accounts list to accounts.txt
# Similar to email, the account and ruoting numbers are unique to each user
def create_acc():
    global accounts
    
    # Makes sure accounts file isn't empty before trying to load it
    accounts = load_accounts()
        
    # Get credentials to put into Account class
    print('\nSIGN UP')
    print('In order to create your account, please answer the following questions:')
    f_name = input('What is your FIRST NAME? : ').lower()
    return_to_start(f_name, '\nFIRST NAME was left blank, returning to start page...')
    l_name = input('What is your LAST NAME? : ').lower()
    return_to_start(l_name, '\nLAST NAME was left blank, returning to start page...')
    email = input('What is your EMAIL ADDRESS? : ').lower()
    return_to_start(email, '\nEMAIL was left blank, returning to start page...')
    
    # make sure one account doesn't have the same email
    # Note: case-sensitive; example@gmail.com and EXAMPLE@gmail.com are the same email
    for account in accounts:
        if email == account.get_email():
            print('That email is already linked to an existing account')
            choice = input('Would you like to log in? (y/n): ').upper()
            if choice == 'Y':
                log_in()
                break
            else:
                print('Understood, sending you back to start page...\n')
                time.sleep(0.5)
                main()
                break
    print(f'A verification code was sent to {email}')  # Email verification
    send_code()
    code = input('Please input your code: ')

    password = input('What will be your PASSWORD? : ').lower()
    new_account = Account(email, password, f_name, l_name)

    # Makes sure account number and routing number are unique for each account
    for account in accounts:
        if new_account.get_account_num() == account.get_account_num():
            new_account.reset_acc_num()   
        
    print('\nPress ENTER to Confirm')
    print('Input any CHARACTER to Decline')
    if input('') == '':
        accounts.append(new_account)
        save_accounts()  # pickles the accounts list every time new user is created
        print('Account created successfully!\n')
    else:
        print('\nAccount creation canceled, sending you back to start page...')
    time.sleep(1)
    clear()
    main()
        

# WIP
def send_code():
    code = str(random.randint(100000,999999))


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')
    header('2.0')


def return_to_start(inpt, message):
    if len(inpt) == 0:
        print(message)
        time.sleep(2)
        clear()
        main()
    

# Handles the logging in process checks to see if the inputted email and password
# is identical to that of a username and password of an Account class in accounts.txt
def log_in():
    global accounts
    # Handles if accounts.txt is empty
    if len(load_accounts()) == 0:
        print('No accounts exist. Redirecting you to account creator...')
        time.sleep(0.5)
        create_acc()
    else:
        accounts = load_accounts()
    
    while True:
        print('\nLOG IN')            
        
        email_in = input('Email: ')
        return_to_start(email_in, '\nReturning to start page...')
        password_in = input('Password: ')
        return_to_start(password_in, '\nReturning to start page...')

        # Go through every account to check if the inputted email and password matches that of a existing account
        # If it does, it sends the user to home_page() where they can use the functions within the account class
        exists = False
        for account in accounts:
            if (email_in.lower() == account.get_email()) and (password_in == account.get_password()):
                print('\nSuccessful Login, sending you to your home page...\n')
                time.sleep(2)
                clear()
                Home(account)
                return

        if exists == False:
            print('\nWe could not find an account with that email or password, try again')
                

if __name__ == '__main__':
    header('2.0')
    main()