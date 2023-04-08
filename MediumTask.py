import csv
import mysql.connector

mydb = mysql.connector.connect(
    host = 'host', # TODO insert your host
    user = 'user', # TODO insert your user
    password = 'password', # TODO insert your password
)
mycursor = mydb.cursor()

try:
    # Create the 'libraries_and_books' database
    mycursor.execute("""CREATE DATABASE IF NOT EXISTS libraries_and_books;""") # TODO change the name of the database if needed
    mycursor.execute("""USE libraries_and_books;""") #TODO change the name of the database if needed

    # Create the 'libraries' table with 'id', 'name', and 'location' columns
    mycursor.execute("""CREATE TABLE libraries (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        location VARCHAR(255) NOT NULL
        );""")

    # Create the 'books' table with 'id', 'title', 'author', 'genre', 'publisher', and 'library_id' columns,
    # with a foreign key- 'library_id' referencing the 'id' column of the 'libraries' table
    mycursor.execute("""CREATE TABLE books (
        id INT AUTO_INCREMENT PRIMARY KEY,
        title VARCHAR(255) NOT NULL,
        author VARCHAR(255) NOT NULL,
        genre VARCHAR(255) NOT NULL,
        publisher VARCHAR(255) NOT NULL,
        library_id INT NOT NULL,
        FOREIGN KEY (library_id) REFERENCES libraries(id)
        );""")


    # Reading data from the 'libraries.csv' file and inserting it into the 'libraries' table
    with open('libraries.csv', 'r') as file:
        reader = csv.DictReader(file)
        query = "INSERT INTO libraries (name, location) VALUES (%s, %s)"
        values = [(line['name'], line['location']) for line in reader]
        mycursor.executemany(query, values)
        mydb.commit()

    # Reading data from the 'books.csv' file and inserting it into the 'books' table
    with open('books.csv', 'r') as file:
        reader = csv.DictReader(file)
        query = "INSERT INTO books (title, author, genre, publisher, library_id) VALUES (%s, %s, %s, %s, %s)"
        values = [
            (
                line['title'],
                line['author'],
                line['genre'],
                line['publisher'],
                line['library_id'],
            )
            for line in reader
        ]
        mycursor.executemany(query, values)
        mydb.commit()

except mysql.connector.Error as error:
    print(f"Error: {error}")

finally:
    mydb.close()