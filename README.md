# SIMULATED BANKING APPLICATION
A simulated command line banking application

## What You'll Find
### main.py
  - The start of the program; handles to intro page, where you can create an account, login, and exit the program
### account.py
  - Handles what an account is and the various functions that can be run by the class
### home_page.py
  - The bulk of the programming, once logged in, this is the code that handles everything from that point on; mostly formatting and idiot proofing
### accounts.txt
  - A text file that holds the pickled accounts and their information for use later
### admin_home.py
  - Similar to home page, used by admin to remove accounts, among other things
### WIP admin_key_gen.py
  - WIP intended to send a random 6-digit code to adming emails allowing access admin_home 

## MAIN.PY
### Intro page
  - Handles user input, allowing them to select one of three options:
    1. Create an account
    2. Log into an existing account
    3. Exit the program
### Creating an account
  - When creating an account the user is asked to enter personal info:
    - First and last name
    - Email address
      - As of right now, there is no authentication for emails so anything can be entered
    - Password
  - When creating a new account the program checks to make sure the inputted email is unique to the new account
### Logging into an account
  - Works the way you'd probably expect:
    - Asks user for email and password
    - Checks accounts.txt file to see if there is an account with those credentials
    - If there is it sends them to their Home Page

## ACCOUNT.PY
### Class methods
 - Deposit money
 - Withdraw money
 - Transfer money
 - Reset account number
   - Used if a new account is created with the same account number as an already existing account

## ACCOUNTS.TXT
 - Through the use of the pickle library, created accounts are stored in accounts.txt for use even after the program ceases execution

## HOME_PAGE.PY
 - Once logged into an account the homepage shows the users the folllowing:
   - Their account number
   - Their savings and checking balance
   - Various commands the user can enter:
     - View ledger
     - Deposit money
     - Withdraw money
     - Transfer money
### View ledger
 - Allows user to view previous transactions from deposits and withdraws, to internal and P2P transfers
### Deposit and Withdraw money
 - Relatively the same in how they work, deposit adds, withdraw subtracts
 - However, with withdraw, before withdrawing, it makes sure there's enough money to withdraw in the account
### Internal Transfer
 - A transfer from one's checking to their savings or vice versa
 - Simple mechanics: subtracts from the transfer from, and adds to the transfer to
### P2P Transfer
 - A transfer from one user's account to another user's account
 - Similar to an internal transfer except the program finds the other person the user wants to transfer to using their account number
 - Once a user is found the transfer happens in the same way as the internal transfer
 - The user that was transfered the money is then given a notification and is asked which account they want to transfer the money to

## ADMIN_HOME.PY
 - After entering random 6-digit code provided in email through admin_pin_gen.py, the user has the ability to:
   1. View created accounts
   2. View info on a single account
   3. Remove accounts
