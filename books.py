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
    print("==============================")
    print("📚 Welcome to Book Manager 📚")
    print("==============================")
    print("1  Add a book")
    print("2  List all books")
    print("3  Search for a book")
    print("4  Remove a book")
    print("Q  to Quit ❌")
    option = input("👉 Choose an option: ")
    return option


# Adds a new book to the list
def addBook(bookList: List[Book]):
    # Prompt user for book details
    title = input("Enter the book title: ").lower()
    id = int(input("Enter the book ID (number): "))
    author = input("Enter the author's name: ").lower()
    publicationYear = int(input("Enter the publication year: "))

    # Create new Book object and append to list
    newBok = Book(title, id, author, publicationYear)
    bookList.append(newBok)

    print(f'Book "{title}" added successfully!')

    saveToJson(bookList)


# Lists all books in the book list
def showBooks(bookList: List[Book]):
    for book in bookList:
        print(f'Book: {book.title}')


# Removes a book from the list by title (case insensitive)
def removeBook(bookList: List[Book]):
    bookToRemove = input("Write the book title to remove: ").lower()

    for book in bookList:
        # Compare lowercased input with book titles
        if bookToRemove == book.title.lower():
            bookList.remove(book)
            print(f'Book {book.title} removed ❌')
            saveToJson(bookList)
            return

    print(f'Could not find the {bookToRemove} in the books list ❌')


# Searches for a book by title (case insensitive)
def searchBook(bookList: List[Book]):
    searchTitle = input("Write the book title to search: ").lower()

    for book in bookList:
        # Compare lowercased input with book titles
        if searchTitle == book.title.lower():
            print(f'Book found...')
            print(book)
            return

    print(f'Book {searchTitle} not found ❌')

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