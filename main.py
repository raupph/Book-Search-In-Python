from books import *

if __name__ == "__main__":
    bookList = loadFromJson()

    while True:
        option = MainMenu()

        match option:
            case "1":
                print("Adding book...")
                addBook(bookList)

            case "2":
                print("Listing books...")
                showBooks(bookList)

            case "3":
                print("Searching book...")
                searchBook(bookList)

            case "4":
                print("Remove book...")
                removeBook(bookList)

            case "q" | "Q":
                print("Exiting program. Bye!")
                break

            case _:
                print("Invalid option, try again.")