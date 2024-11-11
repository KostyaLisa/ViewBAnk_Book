import datetime
import random
from fpdf import FPDF


class ATM:
    accounts = {}  # Store all accounts in a dictionary

    def __init__(self):
        self.current_account = None
        self.is_authenticated = False

    def create_account(self, account_holder_name, pin_code, account_type="savings"):
        account_number = str(random.randint(1000000000, 9999999999))
        if account_number in self.accounts:
            return self.create_account(account_holder_name, pin_code, account_type)

        account_details = {
            'account_number': account_number,
            'account_holder_name': account_holder_name,
            'account_type': account_type,
            'account_status': 'active',
            'account_creation_date': str(datetime.date.today()),
            'account_last_updated': str(datetime.date.today()),
            'balance': 0,
            'transactions': [],
            'pin_code': pin_code
        }

        self.accounts[account_number] = account_details
        print(f"Account created successfully! Your account number is {account_number}")

    def generate_pdf(self):
        if self.current_account:
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)

            pdf.cell(200, 10, txt="Account Details", ln=True, align='C')
            for key, value in self.current_account.items():
                if key != 'pin_code':  # Exclude pin from PDF
                    pdf.cell(200, 10, txt=f"{key}: {value}", ln=True, align='L')

            pdf.output("account_details.pdf")
            print("PDF generated as account_details.pdf.")

    def insert_card(self, account_number):
        if account_number in self.accounts:
            self.current_account = self.accounts[account_number]
            print("Card inserted. Please enter your PIN.")
            entered_pin = input("Enter PIN: ")
            self.authenticate_card(entered_pin)
        else:
            print("Account not found.")

    def authenticate_card(self, entered_pin):
        if self.current_account and entered_pin == self.current_account['pin_code']:
            self.is_authenticated = True
            print("Authentication successful.")
            self.open_menu()
        else:
            print("Authentication failed. Please try again.")
            self.is_authenticated = False

    def open_menu(self):
        if not self.is_authenticated:
            print("Please authenticate first.")
            return
        while True:
            print("\nATM Menu:")
            print("1. Deposit")
            print("2. Withdraw")
            print("3. Transfer")
            print("4. Check Balance")
            print("5. View Account Details")
            print("6. Get Proof of NIB (PDF)")
            print("7. Logout")
            choice = input("Choose an option: ")

            if choice == "1":
                amount = float(input("Enter amount to deposit: "))
                self.deposit(amount)
            elif choice == "2":
                amount = float(input("Enter amount to withdraw: "))
                self.withdraw(amount)
            elif choice == "3":
                amount = float(input("Enter amount to transfer: "))
                recipient_account_number = input("Enter recipient account number: ")
                self.transfer(amount, recipient_account_number)
            elif choice == "4":
                self.check_balance()
            elif choice == "5":
                self.view_account_details()
            elif choice == "6":
                self.generate_pdf()
            elif choice == "7":
                self.logout()
                break
            else:
                print("Invalid option. Please try again.")

    def deposit(self, amount):
        if self.current_account and amount > 0:
            self.current_account['balance'] += amount
            self.current_account['transactions'].append(
                {'type': 'deposit', 'amount': amount, 'date': str(datetime.date.today())})
            print(f"Deposited {amount}. New balance: {self.current_account['balance']}")
        else:
            print("Enter a valid amount.")

    def withdraw(self, amount):
        if self.current_account and amount > 0 and amount <= self.current_account['balance']:
            self.current_account['balance'] -= amount
            self.current_account['transactions'].append(
                {'type': 'withdrawal', 'amount': amount, 'date': str(datetime.date.today())})
            print(f"Withdrew {amount}. New balance: {self.current_account['balance']}")
        else:
            print("Invalid amount or insufficient balance.")

    def transfer(self, amount, recipient_account_number):
        if self.current_account and amount > 0 and amount <= self.current_account['balance']:
            if recipient_account_number in self.accounts:
                self.current_account['balance'] -= amount
                self.accounts[recipient_account_number]['balance'] += amount
                self.current_account['transactions'].append({
                    'type': 'transfer',
                    'amount': amount,
                    'recipient': recipient_account_number,
                    'date': str(datetime.date.today())
                })
                print(
                    f"Transferred {amount} to account {recipient_account_number}. New balance: {self.current_account['balance']}")
            else:
                print("Recipient account not found.")
        else:
            print("Invalid amount or insufficient balance.")

    def check_balance(self):
        if self.current_account:
            print(f"Current balance: {self.current_account['balance']}")

    def view_account_details(self):
        if self.current_account:
            for key, value in self.current_account.items():
                if key != 'pin_code':
                    print(f"{key}: {value}")
            print("Transactions:")
            for transaction in self.current_account['transactions']:
                print(transaction)

    def logout(self):
        print("Logging out...")
        self.is_authenticated = False
        self.current_account = None

    def main(self):
        while True:
            print("\nATM System")
            print("1. Create Account")
            print("2. Insert Card (Login)")
            print("3. Exit")
            choice = input("Choose an option: ")

            if choice == "1":
                account_holder_name = input("Enter your name: ")
                pin_code = input("Set a 4-digit PIN: ")
                self.create_account(account_holder_name, pin_code)
            elif choice == "2":
                account_number = input("Enter your account number: ")
                self.insert_card(account_number)
            elif choice == "3":
                print("Exiting ATM system.")
                break
            else:
                print("Invalid option. Please try again.")

    def run(self):
        self.main()


# Usage
atm = ATM()
atm.run()
