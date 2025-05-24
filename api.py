from flask import Flask, jsonify, request
import json
from typing import List

app = Flask(__name__)
booksFile = "books.json"

def loadBooks() -> List[dict]:
    try:
        with open(booksFile, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        print("⚠️ No saved book list found. Starting with an empty list.")
        return []

@app.route('/livros', methods=['GET'])
def booksAvaible():
    books = loadBooks()
    return jsonify(books)

@app.route('/livros/search', methods = ['GET'])
def searchBook():
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

if __name__ == "__main__":
    app.run(port=5000, host='localhost', debug=True)