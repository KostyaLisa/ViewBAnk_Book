import datetime
import random
from sqlalchemy import Column, String, Integer, Float, Date, Sequence
from sqlalchemy.ext.declarative import declarative_base
from fpdf import FPDF

from Bank.DataBaseSQlite import DatabaseSession

# Initialize SQLAlchemy base
Base = declarative_base()


# Define Account model
class Account(Base):
    __tablename__ = 'accounts'
    id = Column(Integer, Sequence('account_id_seq'), primary_key=True)
    account_number = Column(String(10), unique=True, nullable=False)
    pin_code = Column(String(4), nullable=False)
    account_holder_name = Column(String, nullable=False)
    account_type = Column(String, default="savings")
    account_status = Column(String, default="active")
    account_creation_date = Column(Date, default=datetime.date.today)
    account_last_updated = Column(Date, default=datetime.date.today)
    balance = Column(Float, default=0.0)


# ATM class definition with DatabaseSession
class ATM:
    def __init__(self, db_session):
        self.db_session = db_session
        self.current_account = None
        self.is_authenticated = False
        Base.metadata.create_all(db_session.engine)  # Create tables if not exists

    def create_account(self, account_holder_name, pin_code, account_type="savings"):
        # Generate a unique 10-digit account number
        account_number = str(random.randint(1000000000, 9999999999))

        # Start a session with the DatabaseSession
        with self.db_session as session:
            # Ensure account number is unique in the database
            while session.query(Account).filter_by(account_number=account_number).first():
                account_number = str(random.randint(1000000000, 9999999999))

            # Create and add new account to session
            new_account = Account(
                account_number=account_number,
                pin_code=pin_code,
                account_holder_name=account_holder_name,
                account_type=account_type,
                account_creation_date=datetime.date.today(),
                account_last_updated=datetime.date.today(),
                balance=0.0
            )
            session.add(new_account)
            print(f"Account created successfully! Your account number is {account_number}")

    def generate_pdf(self):
        if self.current_account:
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)

            pdf.cell(200, 10, txt="Account Details", ln=True, align='C')
            for key, value in vars(self.current_account).items():
                if key != 'pin_code' and not key.startswith('_'):
                    pdf.cell(200, 10, txt=f"{key}: {value}", ln=True, align='L')

            pdf.output("account_details.pdf")
            print("PDF generated as account_details.pdf.")

    def insert_card(self, account_number):
        with self.db_session as session:
            account = session.query(Account).filter_by(account_number=account_number).first()
            if account:
                self.current_account = account
                print("Card inserted. Please enter your PIN.")
                entered_pin = input("Enter PIN: ")
                self.authenticate_card(entered_pin)
            else:
                print("Account not found.")

    def authenticate_card(self, entered_pin):
        if self.current_account and entered_pin == self.current_account.pin_code:
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
            with self.db_session as session:
                account = session.query(Account).filter_by(account_number=self.current_account.account_number).first()
                account.balance += amount
                account.account_last_updated = datetime.date.today()
                print(f"Deposited {amount}. New balance: {account.balance}")
        else:
            print("Enter a valid amount.")

    # Define `withdraw`, `transfer`, `check_balance`, `view_account_details`, and `logout`
    # following the same pattern, using `with self.db_session as session`...

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
db_session = DatabaseSession()
atm = ATM(db_session)
atm.run()
