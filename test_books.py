import unittest
from books import Book, validate_book_fields, addBook, showBooks, removeBook, searchBook, saveToJson, loadFromJson
from unittest.mock import patch
import os

class TestBookManager(unittest.TestCase):
    def setUp(self):
        self.book1 = Book("the hobbit", 1, "tolkien", 1933)
        self.book2 = Book("harry potter", 2, "j.k rowling", 1999)
        self.book3 = Book("1984", 3, "george orwell", 1949)
        self.bookList = [self.book1, self.book2]
        self.test_json = "test_books.json"

    def tearDown(self):
        if os.path.exists(self.test_json):
            os.remove(self.test_json)

    def test_validate_book_fields_valid(self):
        self.assertTrue(validate_book_fields("book", 10, "author", 2000, self.bookList))

    def test_validate_book_fields_empty_title(self):
        self.assertFalse(validate_book_fields("", 10, "author", 2000, self.bookList))

    def test_validate_book_fields_empty_author(self):
        self.assertFalse(validate_book_fields("book", 10, "", 2000, self.bookList))

    def test_validate_book_fields_invalid_id(self):
        self.assertFalse(validate_book_fields("book", -1, "author", 2000, self.bookList))
        self.assertFalse(validate_book_fields("book", 0, "author", 2000, self.bookList))

    def test_validate_book_fields_invalid_year(self):
        self.assertFalse(validate_book_fields("book", 10, "author", -2000, self.bookList))
        self.assertFalse(validate_book_fields("book", 10, "author", 0, self.bookList))

    def test_validate_book_fields_duplicate_id(self):
        self.assertFalse(validate_book_fields("book", 1, "author", 2000, self.bookList))

    @patch('builtins.input', side_effect=["the great gatsby", "4", "f. scott fitzgerald", "1925"])
    def test_addBook_success(self, mock_input):
        books = self.bookList.copy()
        addBook(books)
        self.assertEqual(len(books), 3)
        self.assertEqual(books[-1].title, "the great gatsby")

    @patch('builtins.input', side_effect=["", "5", "author", "2020"])
    def test_addBook_empty_title(self, mock_input):
        books = self.bookList.copy()
        addBook(books)
        self.assertEqual(len(books), 2)

    @patch('builtins.input', side_effect=["book", "1", "author", "2020"])
    def test_addBook_duplicate_id(self, mock_input):
        books = self.bookList.copy()
        addBook(books)
        self.assertEqual(len(books), 2)

    @patch('builtins.input', side_effect=["the hobbit"])
    def test_searchBook_found(self, mock_input):
        with patch('builtins.print') as mock_print:
            searchBook(self.bookList)
            self.assertTrue(any("book(s) found" in str(call) for call in mock_print.call_args_list))

    @patch('builtins.input', side_effect=["notfound"])
    def test_searchBook_not_found(self, mock_input):
        with patch('builtins.print') as mock_print:
            searchBook(self.bookList)
            self.assertTrue(any("No books found" in str(call) for call in mock_print.call_args_list))

    @patch('builtins.input', side_effect=["the hobbit", "y"])
    def test_removeBook_success(self, mock_input):
        books = self.bookList.copy()
        with patch('builtins.print') as mock_print:
            removeBook(books)
            self.assertEqual(len(books), 1)
            self.assertTrue(any("removed" in str(call) for call in mock_print.call_args_list))

    @patch('builtins.input', side_effect=["notfound"])
    def test_removeBook_not_found(self, mock_input):
        books = self.bookList.copy()
        with patch('builtins.print') as mock_print:
            removeBook(books)
            self.assertEqual(len(books), 2)
            self.assertTrue(any("No book found" in str(call) for call in mock_print.call_args_list))

    def test_save_and_load_json(self):
        books = [self.book1, self.book2, self.book3]
        saveToJson(books, self.test_json)
        loaded = loadFromJson(self.test_json)
        self.assertEqual(len(loaded), 3)
        self.assertEqual(loaded[0].title, "the hobbit")
        self.assertEqual(loaded[1].author, "j.k rowling")

if __name__ == "__main__":
    unittest.main()
