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

@app.route('/books', methods=['GET'])
def booksAvaible():
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
    return jsonify(books)

@app.route('/books/search', methods=['GET'])
def searchBook():
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

    return jsonify(filteredBooks)

@app.route('/books', methods=['POST'])
def addBook():
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
        schema:
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
      400:
        description: Missing fields or book ID already exists
    """
    booksList: List[dict] = loadBooks()
    newBok = request.get_json()
    requiredFields = ["id", "title", "author", "publicationYear"]

    #returns true only if all the components were write
    if not all(field in newBok for field in requiredFields):
        #Bad request
        return jsonify({"error": "Missing one or more required fields"}), 400
    #Returns true if any book have the same id
    if any(book["id"] == newBok["id"] for book in booksList):
        #Bad request
        return jsonify({"error": "Book with this ID already exists"}), 400

    booksList.append(newBok)
    #Unpacking each Dict of the booksList
    #Ex:. Book(id=1, title="The Hobbit", author="Tolkien", publicationYear=1933)
    ## The ** says that all the keys and values will be passed
    saveToJson([Book(**book) for book in booksList])

    return jsonify(newBok), 201


if __name__ == "__main__":
    app.run(port=5000, host='localhost', debug=True)
