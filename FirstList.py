# Create an ATM (ATM) wherever possible
# insert a card and enter the code. Upon introduction
# correct code, open a menu where you can deposit,
# withdraw, transfer, obtain proof of NIB (generates a PDF),
# check balance and view account details. Put all
# these features in action.

class ATM:
    def __init__(self, account_number, pin_code):
        self.account_number = account_number
        self.pin_code = pin_code
        self.balance = 0
        self.transactions = []
        self.account_details = {
            'account_number': self.account_number,
            'pin_code': self.pin_code,
            'balance': self.balance,
            'transactions': self.transactions,
            'account_holder_name': 'John Doe',
            'account_type': 'savings',
            'account_status': 'active',
            'account_creation_date': '2022-01-01',
            'account_last_updated': '2022-01-01'}
        self.generate_pdf()

    def generate_pdf(self):
        # Generate a PDF of account details
        pass

    def insert_card(self):
        # Insert a card and validate the pin code
        pass
    def authenticate_card(self):
        # Validate the inserted card and pin code
        pass
    def open_menu(self):
        # Open the ATM menu where users can perform transactions
        pass
    def deposit(self, amount):
        # Deposit money into the account
        pass
    def withdraw(self, amount):
        # Withdraw money from the account
        pass
    def transfer(self, amount, recipient_account_number):
        # Transfer money from the account to another account
        pass
    def check_balance(self):
        # Check the current balance in the account
        pass
    def view_account_details(self):
        # View account details
        pass
    def logout(self):
        # Logout from the ATM
        pass
    def main(self):
        # Main loop of the ATM
        pass
    def run(self):
        # Run the ATM
        self.main()
