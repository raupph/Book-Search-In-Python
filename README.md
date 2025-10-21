# Book Search in Python

A small project to manage and search books locally using a command-line interface (CLI) and a simple Flask-based HTTP API.

## Overview

The project provides two ways to interact with a collection of books stored in `books.json`:

- CLI: `main.py` uses `books.py` to add, list, search, and remove books via the terminal.
- HTTP API: `api.py` exposes REST endpoints to list, search, add, and remove books. The API also includes Swagger documentation (via `flasgger`).

This is a lightweight application intended for learning and prototyping. Data is persisted to a JSON file (`books.json`).

## Features

- List all books
- Search books by title, author, or id (API and CLI)
- Add and remove books
- Automatic API documentation with Swagger (Flasgger)

## Requirements

- Python 3.10 or newer (the CLI uses `match/case`, available since Python 3.10)
- `pip`

Project dependencies are listed in `requirements.txt`.

## Quick install

On Linux / macOS:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

On Windows (PowerShell):

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Project structure

- `api.py` - Flask API with endpoints to list, search, add, and remove books. Includes Swagger.
- `books.py` - Core application logic: `Book` class, CLI helper functions, save/load JSON.
- `main.py` - Command-line interface that uses `books.py`.
- `books.json` - JSON file used as local storage (contains sample books).
- `requirements.txt` - Python dependencies.

## How to use

### 1) Command-line interface (CLI)

After activating the virtual environment and installing dependencies, run:

```bash
python main.py
```

Follow the interactive menu to add, list, search, or remove books.

Notes:
- When adding books via the CLI, the requested fields are: title (string), id (integer), author (string), and publicationYear (integer).
- Titles and authors are converted to lowercase in the interactive functions (the original project applies lowercase to some inputs).

### 2) HTTP API (Flask)

Run the API:

```bash
python api.py
```

The API runs by default at `http://localhost:5000`.

The Swagger UI (interactive documentation) will be available at:

```
http://localhost:5000/apidocs
```

(Depending on the `flasgger` version, the path may vary slightly — typically `/apidocs`.)

### Main endpoints

1. List all books

- GET /books

Example:

```bash
curl http://localhost:5000/books
```

2. Search books (by title, author or id)

- GET /books/search?title=<term>
- GET /books/search?author=<term>
- GET /books/search?id=<id>

Example (search by title):

```bash
curl "http://localhost:5000/books/search?title=hobbit"
```

Note: searches by `title` and `author` are case-insensitive and perform a "contains" match (i.e., substring search).

3. Add a book

- POST /books
- Body (JSON): {"id": int, "title": string, "author": string, "publicationYear": int}

Example:

```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{"id":99,"title":"My Book","author":"Me","publicationYear":2025}' \
  http://localhost:5000/books
```

The API returns 400 if a required field is missing or if the `id` already exists.

4. Remove a book

- DELETE /books/remove?id=<id>
- DELETE /books/remove?title=<title>

Example (remove by id):

```bash
curl -X DELETE "http://localhost:5000/books/remove?id=99"
```

If no book matches the filter, the API returns a 404.

## Data format (books.json)

Each item in `books.json` has the form:

```json
{
  "title": "the hobbit",
  "id": 1,
  "author": "tolkien",
  "publicationYear": 1933
}
```
curl "http://localhost:5000/books/search?title=hobbit"
```

Note: searches by `title` and `author` are case-insensitive and perform a "contains" match (i.e., substring search).

3. Add a book

- POST /books
- Body (JSON): {"id": int, "title": string, "author": string, "publicationYear": int}

Example:

```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{"id":99,"title":"My Book","author":"Me","publicationYear":2025}' \
  http://localhost:5000/books
```

The API returns 400 if a required field is missing or if the `id` already exists.

4. Remove a book

- DELETE /books/remove?id=<id>
- DELETE /books/remove?title=<title>

Example (remove by id):

```bash
curl -X DELETE "http://localhost:5000/books/remove?id=99"
```

If no book matches the filter, the API returns a 404.

## Data format (books.json)

Each item in `books.json` has the form:

```json
{
  "title": "the hobbit",
  "id": 1,
  "author": "tolkien",
  "publicationYear": 1933
}
```
