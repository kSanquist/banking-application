import random

class Account:
    def __init__(self, email, password, f_name, l_name):
        self.email = email
        self.password = password
        self.f_name = f_name
        self.l_name = l_name
        self.account_num = random.randrange(100000000000, 999999999999)
        self.checking_bal = 0
        self.savings_bal = 0
        self.transfer_bal = 0
        self.dep_with_history = {}  # 'deposit0':[1000, checking]
        self.transfer_history = {}  # 'transfer0':[1000, 'savings', 'checking'] / 'transfer1':[1000, 'kyle sanquist', 'john doe', True]
            
        
    # Allows user to deposit money
    def deposit_money(self, account, amount):
        if account == 'checking':
            self.checking_bal += amount
            if amount > 0:
                self.dep_with_history['deposit'+str(len(self.dep_with_history))] = [amount, 'checking']
        else:
            self.savings_bal += amount
            if amount > 0:
                self.dep_with_history['deposit'+str(len(self.dep_with_history))] = [amount, 'savings']
            
    # Allows user to withdraw money
    def withdraw_money(self, account, amount):
        if account == 'checking':
            if self.checking_bal >= amount:
                self.checking_bal -= amount
                if amount > 0:
                    self.dep_with_history['withdraw'+str(len(self.dep_with_history))] = [amount, 'checking']
                return True
            else:
                return False
        else:
            if self.savings_bal >= amount:
                self.savings_bal -= amount
                if amount > 0:
                    self.dep_with_history['withdraw'+str(len(self.dep_with_history))] = [amount, 'savings']
                return True
            else:
                return False

    # Allows user to transfer funds locally between their own accounts
    def transfer_money(self, from_acc, amount):
        if from_acc == 'checking':  # Checking --> Savnings
            if self.checking_bal >= amount:
                self.checking_bal -= amount
                self.savings_bal += amount
                if amount > 0:
                    self.transfer_history['transfer'+str(len(self.transfer_history))] = [amount, 'checking', 'savings']
                return True
            else:
                return False
        else:  # Savings --> Checking
            if self.savings_bal >= amount:
                self.savings_bal -= amount
                self.checking_bal += amount
                if amount > 0:
                    self.transfer_history['transfer'+str(len(self.transfer_history))] = [amount, 'savings', 'checking']
                return True
            else:
                return False

    # Allows user to transfer funds to another account provided they
    # know the other account's account number and routing number
    def transfer_money_p2p(self, from_acc, account, amount):
        # Handles sending money
        if from_acc == 'checking':  # Checking --> Transfer
            if self.checking_bal >= amount:
                self.checking_bal -= amount
                account.transfer_bal += amount
                if amount > 0:
                    self.transfer_history['transfer'+str(len(self.transfer_history))] = [amount, from_acc.upper(), account.get_name(), True]
                    account.transfer_history['transfer'+str(len(account.transfer_history))] = [amount, account.get_name(), self.get_name(), True, True]
                return True
            else:
                False
        else:  # Savings --> Transfer
            if self.savings_bal >= amount:
                self.savings_bal -= amount
                account.transfer_bal += amount
                if amount > 0:
                    self.transfer_history['transfer'+str(len(self.transfer_history))] = [amount, from_acc.upper(), account.get_name(), True]
                    account.transfer_history['transfer'+str(len(account.transfer_history))] = [amount, account.get_name(), self.get_name(), True, True]
                return True
            else:
                False


    # Resets account number
    # Used only in create_acc() class to maintain uniqueness of ID numbers
    def reset_acc_num(self):
        new_account_num = random.randrange(100000000000, 999999999999) 
        self.account_num = new_account_num
        
    
    # Displays all info on an Account class object in a nice string format
    def display_all_info(self):
        print(f'{self.get_name().title()}:')
        print(f'Email: {self.email}')
        print(f'Pswrd: {self.password}')
        print(f'Acct#: {self.account_num}')
        print(f'check: {self.checking_bal}')
        print(f'savin: {self.savings_bal}')

        
    # GETTERS
    def get_email(self):
        return self.email
    def get_password(self):
        return self.password
    def get_name(self):
        return self.f_name + ' ' + self.l_name
    def get_account_num(self):
        return self.account_num
    def get_checking_balance(self):
        return self.checking_bal
    def get_savings_balance(self):
        return self.savings_bal
    def get_transfer_balance(self):
        return self.transfer_bal
    def get_dep_with_history(self):
        return self.dep_with_history
    def get_transfer_history(self):
        return self.transfer_history

        
    # SETTERS
    def set_email(self, email):
        self.email = email
    def set_password(self, password):
        self.password = password
    def set_f_name(self, f_name):
        self.f_name = f_name
    def set_l_name(self, l_name):
        self.l_name = l_name
    def set_checking_bal(self, amount):
        self.checking_bal = amount
    def set_savings_bal(self, amount):
        self.savings_bal = amount
    def set_transfer_bal(self, amount):
        self.transfer_bal = amount