from flask import Flask, jsonify, request
import json
from typing import List
from books import  saveToJson, Book
from flasgger import Swagger


app = Flask(__name__)
swagger = Swagger(app)  # ativa swagger
booksFile = "books.json"

def loadBooks() -> List[dict]:
    try:
        with open(booksFile, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        print("⚠️ No saved book list found. Starting with an empty list.")
        return []

# --- Utility functions for validation and book operations ---
def validate_book_fields(book: dict, booksList: List[dict]):
    required_fields = ["id", "title", "author", "publicationYear"]
    for field in required_fields:
        if field not in book:
            return False, f"Missing required field: {field}"
    if not isinstance(book["id"], int) or book["id"] <= 0:
        return False, "ID must be a positive integer."
    if not isinstance(book["publicationYear"], int) or book["publicationYear"] <= 0:
        return False, "Publication year must be a positive integer."
    if not book["title"] or not book["author"]:
        return False, "Title and author cannot be empty."
    if any(b["id"] == book["id"] for b in booksList):
        return False, "Book with this ID already exists."
    return True, None

def find_book_by_id(booksList: List[dict], book_id):
    for book in booksList:
        if str(book.get("id")) == str(book_id):
            return book
    return None

# --- RESTful Endpoints ---
@app.route('/books', methods=['GET'])
def get_books():
    """
    Get the list of all books
    ---
    responses:
      200:
        description: A list of all books
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
              title:
                type: string
              author:
                type: string
              publicationYear:
                type: integer
    """
    books = loadBooks()
    return jsonify(books), 200

@app.route('/books/<int:book_id>', methods=['GET'])
def get_book_by_id(book_id):
    """
    Get a book by its ID
    ---
    parameters:
      - name: book_id
        in: path
        type: integer
        required: true
        description: ID of the book
    responses:
      200:
        description: Book found
      404:
        description: Book not found
    """
    books = loadBooks()
    book = find_book_by_id(books, book_id)
    if book:
        return jsonify(book), 200
    return jsonify({"error": "Book not found."}), 404

@app.route('/books/search', methods=['GET'])
def search_books():
    """
    Search books by title, author, or id
    ---
    parameters:
      - name: title
        in: query
        type: string
        required: false
        description: Filter by book title
      - name: author
        in: query
        type: string
        required: false
        description: Filter by author name
      - name: id
        in: query
        type: integer
        required: false
        description: Filter by book ID
    responses:
      200:
        description: A list of filtered books
    """
    booksList: List[dict] = loadBooks()
    filteredBooks: List[dict] = []
    title = request.args.get("title")
    book_id = request.args.get("id")
    author = request.args.get("author")
    for book in booksList:
        # Check if the 'title' parameter was provided in the query.
        # If it was, convert both the search term and the book's title to lowercase
        # and check if the search term is NOT contained in the book's title.
        # If the condition is true (meaning the book's title does NOT contain the search term),
        # skip this book and continue to the next iteration of the loop.

        if title and title.lower() not in book.get("title", "").lower():
            continue
        if author and author.lower() not in book.get("author", "").lower():
            continue
        if book_id and str(book.get("id")) != str(book_id):
            continue
        filteredBooks.append(book)
    return jsonify(filteredBooks), 200

@app.route('/books', methods=['POST'])
def add_book():
    """
    Add a new book to the collection
    ---
    parameters:
      - in: body
        name: book
        required: true
        schema:
          type: object
          required:
            - id
            - title
            - author
            - publicationYear
          properties:
            id:
              type: integer
            title:
              type: string
            author:
              type: string
            publicationYear:
              type: integer
    responses:
      201:
        description: Book successfully added
      400:
        description: Missing fields or book ID already exists
    """
    booksList: List[dict] = loadBooks()
    newBook = request.get_json()
    is_valid, error_msg = validate_book_fields(newBook, booksList)
    if not is_valid:
        return jsonify({"error": error_msg}), 400
    booksList.append(newBook)
    saveToJson([Book(**book) for book in booksList])
    return jsonify(newBook), 201

@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    """
    Delete a book by its ID
    ---
    parameters:
      - name: book_id
        in: path
        type: integer
        required: true
        description: ID of the book to remove
    responses:
      200:
        description: Book removed successfully
      404:
        description: No matching book found
    """
    booksList: List[dict] = loadBooks()
    book = find_book_by_id(booksList, book_id)
    if not book:
        return jsonify({"error": "No matching book found to remove."}), 404
    booksList = [b for b in booksList if str(b.get("id")) != str(book_id)]
    saveToJson([Book(**b) for b in booksList])
    return jsonify({"message": f"Book with ID {book_id} removed successfully."}), 200

if __name__ == "__main__":
    app.run(port=5000, host='localhost', debug=True)
