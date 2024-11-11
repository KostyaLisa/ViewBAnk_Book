from BookDateBase import Book, PhysicalBook, EBook, display_books, search_books, sell_book, lend_book, return_book, \
    view_all_books


def main():
    while True:
        print("\nLibrary Management System")
        print("1. Add Physical Book")
        print("2. Add EBook")
        print("3. Search Books")
        print("4. Sell Book")
        print("5. Lend Book")
        print("6. Return Book")
        print("7. View All Books")
        print("8. Exit")

        choice = input("Enter choice: ")

        if choice == '1':
            title = input("Enter title: ")
            author = input("Enter author: ")
            price = float(input("Enter price: "))
            pages = int(input("Enter number of pages: "))
            stock = int(input("Enter stock: "))
            PhysicalBook.add_physical_book(title, author, price, pages, stock)

        elif choice == '2':
            title = input("Enter title: ")
            author = input("Enter author: ")
            price = float(input("Enter price: "))
            file_format = input("Enter file format (e.g., PDF, EPUB): ")
            EBook.add_ebook(title, author, price, file_format)

        elif choice == '3':
            keyword = input("Enter search keyword: ")
            books = search_books(keyword)
            display_books(books)

        elif choice == '4':
            book_id = int(input("Enter book ID to sell: "))
            sell_book(book_id)

        elif choice == '5':
            book_id = int(input("Enter book ID to lend: "))
            lend_book(book_id)

        elif choice == '6':
            book_id = int(input("Enter book ID to return: "))
            return_book(book_id)

        elif choice == '7':
            view_all_books()


        elif choice == '8':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Try again.")


# Run the program
if __name__ == '__main__':
    main()