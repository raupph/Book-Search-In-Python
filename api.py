from flask import Flask, request
import json

app = Flask(__name__)
booksFile = "books.json"

@app.route('/livros')
def jsontoAPI():
    try:
        with open(booksFile, "r") as file:
            booksAsDict = json.load(file)
            return booksAsDict
    except FileNotFoundError:
        print("⚠️ No saved book list found. Starting with an empty list.")
        return []
    
if __name__ == "__main__":
    app.run(port=5000, host='localhost', debug=True)
