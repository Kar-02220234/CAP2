import os
import random

ACCOUNTS_FILE_DIRECTORY = "accounts.txt"

class Account:
    def __init__(self, account_number, password, account_type, balance=0):
        self.account_number = account_number
        self.password = password  # Note: Consider hashing this value for security
        self.account_type = account_type
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount
        print(f"Deposited {amount}. Your Available balance: {self.balance}")

    def withdraw(self, amount):
        if self.balance >= amount:
            self.balance -= amount
            print(f"Withdrew {amount}. Your Available balance: {self.balance}")
        else:
            print("Insufficient funds!")

    def send_money(self, amount, receiver):
        if self.balance >= amount:
            self.balance -= amount
            receiver.balance += amount
            print(f"Sent {amount} to {receiver.account_number}. Your Available balance: {self.balance}")
        else:
            print("Insufficient funds!")

    def save_to_file(self):
        with open(ACCOUNTS_FILE_DIRECTORY, "a") as file:
            file.write(f"{self.account_number},{self.password},{self.account_type},{self.balance}\n")

    @classmethod
    def load_accounts(cls):
        accounts = []
        if os.path.exists(ACCOUNTS_FILE_DIRECTORY):
            with open(ACCOUNTS_FILE_DIRECTORY, "r") as file:
                for line in file:
                    account_number, password, account_type, balance = line.strip().split(",")
                    accounts.append(cls(account_number, password, account_type, int(balance)))
        return accounts
    
    @classmethod
    def find_account(cls, account_number, password):
        accounts = cls.load_accounts()
        for account in accounts:
            if account.account_number == account_number and account.password == password:
                return account
        return None

    @classmethod
    def delete_account(cls, account_number, password):
        accounts = cls.load_accounts()
        accounts = [acc for acc in accounts if not (acc.account_number == account_number and acc.password == password)]
        with open(ACCOUNTS_FILE_DIRECTORY, "w") as file:
            for account in accounts:
                file.write(f"{account.account_number},{account.password},{account.account_type},{account.balance}\n")
        print("Account deleted.")

class PersonalAccount(Account):
    def __init__(self, account_number, password, balance=0):
        super().__init__(account_number, password, "Personal", balance)

class BusinessAccount(Account):
    def __init__(self, account_number, password, balance=0):
        super().__init__(account_number, password, "Business", balance)

def generate_account_number():
    return str(random.randint(1000000000, 9999999999))

def generate_password():
    return ''.join([str(random.randint(0, 9)) for _ in range(8)])  # Generate an 8-character password

def create_account(account_type):
    account_number = generate_account_number()
    password = generate_password()
    if account_type == "Personal":
        account = PersonalAccount(account_number, password)
    else:
        account = BusinessAccount(account_number, password)
    account.save_to_file()
    print(f"Account created. Number: {account_number}, Password: {password}")

def login():
    account_number = input("Enter account number: ")
    password = input("Enter password: ")
    account = Account.find_account(account_number, password)
    if account:
        print("Login successful!")
        return account
    else:
        print("Invalid account number or password!")
        return None

def main():
    while True:
        print("**********Welcome to KLBANK**********")
        print("\n1. Create New Account")
        print("\n2. Login")
        print("\n3. Exit")
        choice = input("\nEnter your choice: ")

        if choice == "1":
            account_type = input("Enter account type (Personal/Business): ")
            if account_type in ["Personal", "Business"]:
                create_account(account_type)
            else:
                print("Invalid account type!")
        elif choice == "2":
            account = login()
            if account:
                while True:
                    print("What do you want to do?")
                    print("\nEnter 1 to Check Balance")
                    print("\nEnter 2 to Deposit")
                    print("\nEnter 3 to Withdraw")
                    print("\nEnter 4 to Send Money")
                    print("\nEnter 5 to Delete Account")
                    print("\nEnter 6 to Logout")
                    user_choice = input("Enter your choice: ")

                    if user_choice == "1":
                        print(f"Your balance is: {account.balance}")
                    elif user_choice == "2":
                        amount = float(input("Enter amount to deposit: "))
                        account.deposit(amount)
                    elif user_choice == "3":
                        amount = float(input("Enter amount to withdraw: "))
                        account.withdraw(amount)
                    elif user_choice == "4":
                        receiver_account_number = input("Enter receiver's account number: ")
                        receiver_password = input("Enter receiver's password: ")
                        receiver = Account.find_account(receiver_account_number, receiver_password)
                        if receiver:
                            amount = float(input("Enter amount to send: "))
                            account.send_money(amount, receiver)
                        else:
                            print("Receiver account not found or invalid password!")
                    elif user_choice == "5":
                        Account.delete_account(account.account_number, account.password)
                        print("Account deleted. Logging out.")
                        break
                    elif user_choice == "6":
                        print("Logged out.")
                        break
                    else:
                        print("Invalid choice!")

        elif choice == "3":
            break
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main()
