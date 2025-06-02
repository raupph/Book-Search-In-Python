from typing import List, Tuple
import json


# Book class definition
class Book:
    def __init__(self, title, id, author, publicationYear):
        # Initializes a Book object with title, ID, author, and publication year
        self.title = title
        self.id = id
        self.author = author
        self.publicationYear = publicationYear

    def __str__(self):
        # Returns a string representation of the book
        return f"ID: {self.id} | Title: {self.title} | Author: {self.author} | Year: {self.publicationYear}"
    

# Displays the main menu and returns the user's option
def MainMenu():
    print("\n" + "="*40)
    print("\033[1;36m📚  Welcome to Book Manager  📚\033[0m")
    print("="*40)
    print("\033[1;33m[1]\033[0m  ➕  Add a book")
    print("\033[1;33m[2]\033[0m  📋  List all books")
    print("\033[1;33m[3]\033[0m  🔍  Search for a book")
    print("\033[1;33m[4]\033[0m  ❌  Remove a book")
    print("\033[1;31m[Q]\033[0m  🚪  Quit")
    print("-"*40)
    option = input("\033[1;32m👉 Choose an option: \033[0m")
    print("\n")
    return option

# Helper: Validate book fields
def validate_book_fields(title, id, author, publicationYear, bookList):
    if not title or not author:
        print("\033[1;31m[Error]\033[0m Title and author cannot be empty.")
        return False
    if not isinstance(id, int) or id <= 0:
        print("\033[1;31m[Error]\033[0m ID must be a positive integer.")
        return False
    if not isinstance(publicationYear, int) or publicationYear <= 0:
        print("\033[1;31m[Error]\033[0m Publication year must be a positive integer.")
        return False
    if any(book.id == id for book in bookList):
        print(f"\033[1;31m[Error]\033[0m A book with ID {id} already exists.")
        return False
    return True

# Adds a new book to the list
def addBook(bookList: List[Book]):
    """Adds a new book to the list, with data validation and error handling."""
    try:
        title = input("Enter the book title: ").strip().lower()
        id_str = input("Enter the book ID (number): ").strip()
        id = int(id_str)
        author = input("Enter the author's name: ").strip().lower()
        year_str = input("Enter the publication year: ").strip()
        publicationYear = int(year_str)
    except ValueError:
        print("\033[1;31m[Error]\033[0m ID and year must be integers.")
        return
    if not validate_book_fields(title, id, author, publicationYear, bookList):
        return
    newBook = Book(title, id, author, publicationYear)
    bookList.append(newBook)
    print(f'\033[1;32mBook "{title}" added successfully!\033[0m')
    saveToJson(bookList)

# Lists all books in the book list
def showBooks(bookList: List[Book]):
    if not bookList:
        print("\033[1;33mNo books registered.\033[0m")
        return
    print("\n\033[1;36mBook List:\033[0m")
    for book in bookList:
        print(f'  {book}')
    print()

# Removes a book from the list by title or ID (case insensitive)
def removeBook(bookList: List[Book]):
    print("\nYou can remove by title or ID.")
    user_input = input("Enter the title or ID of the book to remove: ").strip().lower()
    found = False
    for book in bookList:
        if user_input == str(book.id).lower() or user_input == book.title.lower():
            confirm = input(f'Are you sure you want to remove "{book.title}" (ID: {book.id})? [y/N]: ').strip().lower()
            if confirm == 'y':
                bookList.remove(book)
                print(f'\033[1;31mBook "{book.title}" removed ❌\033[0m')
                saveToJson(bookList)
                found = True
                break
            else:
                print("Removal cancelled.")
                return
    if not found:
        print(f'\033[1;33mNo book found matching "{user_input}".\033[0m')

# Searches for a book by title or ID (case insensitive, partial search)
def searchBook(bookList: List[Book]):
    search_input = input("Enter part of the title or the book ID to search: ").strip().lower()
    results = []
    for book in bookList:
        if search_input in book.title.lower() or search_input == str(book.id).lower():
            results.append(book)
    if results:
        print(f'\033[1;32m{len(results)} book(s) found:\033[0m')
        for book in results:
            print(f'  {book}')
    else:
        print(f'\033[1;33mNo books found for "{search_input}".\033[0m')

# Saves the current book list to a JSON file
def saveToJson(bookList: List[Book], filename="books.json"):
    # Convert list of Book objects to list of dictionaries
    booksAsDict = [book.__dict__ for book in bookList]
    # Write to JSON file
    with open(filename, "w") as file:
        json.dump(booksAsDict, file, indent=4)
    print("📁 Books saved to JSON.")

# Loads the book list from a JSON file, if it exists
def loadFromJson(filename="books.json") -> List[Book]:
    try:
        with open(filename, "r") as file:
            booksAsDict = json.load(file)
            # Convert list of dictionaries back to list of Book objects
            booksAsObjects = [Book(**book) for book in booksAsDict]
            return booksAsObjects
    except FileNotFoundError:
        print("⚠️ No saved book list found. Starting with an empty list.")
        return []