from sqlalchemy import create_engine, Column, Integer, String, Boolean, Float, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

# Initialize SQLAlchemy base and engine
Base = declarative_base()
engine = create_engine('sqlite:///library.db', echo=True)
Session = sessionmaker(bind=engine)
session = Session()

# General Book Model
class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    available = Column(Boolean, default=True)  # availability status

    # Polymorphic type to handle different types of books
    type = Column(String)

    __mapper_args__ = {
        'polymorphic_on': type,
        'polymorphic_identity': 'book'
    }

    def __repr__(self):
        return f"<Book(title='{self.title}', author='{self.author}', price={self.price})>"

# Physical Book Model
class PhysicalBook(Book):
    __tablename__ = 'physical_books'
    id = Column(Integer, ForeignKey('books.id'), primary_key=True)
    pages = Column(Integer, nullable=False)
    stock = Column(Integer, default=1)  # number of copies

    __mapper_args__ = {
        'polymorphic_identity': 'physical_book',
    }

    def __repr__(self):
        return f"<PhysicalBook(title='{self.title}', author='{self.author}', pages={self.pages}, stock={self.stock})>"

# EBook Model
class EBook(Book):
    __tablename__ = 'ebooks'
    id = Column(Integer, ForeignKey('books.id'), primary_key=True)
    file_format = Column(String, nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'ebook',
    }

    def __repr__(self):
        return f"<EBook(title='{self.title}', author='{self.author}', file_format='{self.file_format}')>"

# Create all tables
Base.metadata.create_all(engine)

# Functions to add books, search, sell, lend, and return books remain the same
# No changes are needed to these as they only interact with the database models.



def add_physical_book(title, author, price, pages, stock=1):
    book = PhysicalBook(title=title, author=author, price=price, pages=pages, stock=stock)
    session.add(book)
    session.commit()
    print(f"Physical book '{title}' added to library.")


def add_ebook(title, author, price, file_format):
    book = EBook(title=title, author=author, price=price, file_format=file_format)
    session.add(book)
    session.commit()
    print(f"EBook '{title}' added to library.")


def search_books(keyword):
    books = session.query(Book).filter((Book.title.contains(keyword)) | (Book.author.contains(keyword))).all()
    return books


def sell_book(book_id):
    book = session.query(Book).filter_by(id=book_id).first()
    if book:
        if isinstance(book, PhysicalBook) and book.stock > 0:
            book.stock -= 1
            session.commit()
            print(f"Sold 1 copy of '{book.title}'. Remaining stock: {book.stock}")
        elif isinstance(book, EBook):
            print(f"EBook '{book.title}' sold. No stock reduction needed.")
        else:
            print(f"Physical book '{book.title}' is out of stock.")
    else:
        print("Book not found.")


def lend_book(book_id):
    book = session.query(Book).filter_by(id=book_id).first()
    if book and book.available:
        book.available = False  # Mark as lent
        session.commit()
        print(f"'{book.title}' has been lent.")
    else:
        print(f"'{book.title}' is currently unavailable or not found.")


def return_book(book_id):
    book = session.query(Book).filter_by(id=book_id).first()
    if book and not book.available:
        book.available = True  # Mark as returned
        session.commit()
        print(f"'{book.title}' has been returned.")
    else:
        print("Book not found or not currently lent.")


def display_books(books):
    if not books:
        print("No books found.")
    for book in books:
        print(book)


def view_all_books():
    # Query all books from the books table
    books = session.query(Book).all()

    # Display each book
    if not books:
        print("No books in the library.")
    else:
        print("All books in the library:")
        for book in books:
            print(book)


