import flet as ft
from BookDateBase import Book, PhysicalBook, EBook, display_books, search_books, sell_book, lend_book, return_book, \
    session


# Create a new function for adding physical books and e-books directly in the class
def add_physical_book(title, author, price, pages, stock):
    book = PhysicalBook(title=title, author=author, price=price, pages=pages, stock=stock)
    session.add(book)
    session.commit()

def add_ebook(title, author, price, file_format):
    book = EBook(title=title, author=author, price=price, file_format=file_format)
    session.add(book)
    session.commit()

def main(page: ft.Page,  ):


    page.title = "Library Management System"
    page.window.min_width = 400
    page.window.min_height = 200

    # Define input fields and controls
    title_input = ft.TextField(label="Title")
    author_input = ft.TextField(label="Author")
    price_input = ft.TextField(label="Price", keyboard_type=ft.KeyboardType.NUMBER)
    pages_input = ft.TextField(label="Pages", keyboard_type=ft.KeyboardType.NUMBER)
    stock_input = ft.TextField(label="Stock", keyboard_type=ft.KeyboardType.NUMBER, value="1")
    format_input = ft.TextField(label="Format (e.g., PDF, EPUB)")

    output_text = ft.Text()

    def view_all_books():
        books = session.query(Book).all()
        if not books:
            return ["No books in the library."]
        else:
            return [str(book) for book in books]

    # Function to display books in output area
    def show_books(books):
        output_text.value = "\n".join(str(book) for book in books)
        page.update()

    # Functions for each operation
    def add_physical_book_click(e):
        title = title_input.value
        author = author_input.value
        price = float(price_input.value)
        pages = int(pages_input.value)
        stock = int(stock_input.value)
        add_physical_book(title, author, price, pages, stock)
        output_text.value = f"Added Physical Book: {title}"
        page.update()

    def add_ebook_click(e):
        title = title_input.value
        author = author_input.value
        price = float(price_input.value)
        file_format = format_input.value
        add_ebook(title, author, price, file_format)
        output_text.value = f"Added EBook: {title}"
        page.update()

    def search_books_click(e):
        keyword = title_input.value
        books = search_books(keyword)
        show_books(books)

    def sell_book_click(e):
        book_id = int(title_input.value)
        sell_book(book_id)
        output_text.value = f"Sold book with ID: {book_id}"
        page.update()

    def lend_book_click(e):
        book_id = int(title_input.value)
        lend_book(book_id)
        output_text.value = f"Lent book with ID: {book_id}"
        page.update()

    def return_book_click(e):
        book_id = int(title_input.value)
        return_book(book_id)
        output_text.value = f"Returned book with ID: {book_id}"
        page.update()



    # Add components to the Flet page layout
    page.add(
        ft.Text("Library Management System", size=30, weight="bold"),
        title_input,
        author_input,
        price_input,
        pages_input,
        stock_input,
        format_input,
        ft.Row([
            ft.ElevatedButton("Add Physical Book", on_click=add_physical_book_click),
            ft.ElevatedButton("Add EBook", on_click=add_ebook_click),
        ]),
        ft.Row([
            ft.ElevatedButton("Search Books", on_click=search_books_click),
            ft.ElevatedButton("Sell Book", on_click=sell_book_click),
            ft.ElevatedButton("Lend Book", on_click=lend_book_click),
            ft.ElevatedButton("Return Book", on_click=return_book_click),
            ft.ElevatedButton("All books", on_click=view_all_books),
        ]),
        output_text
    )

# Run the Flet app
if __name__ == '__main__':
    ft.app(target=main)
