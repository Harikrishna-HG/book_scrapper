import requests
from bs4 import BeautifulSoup
import sqlite3

def create_database():
    conn =  sqlite3.connect("books.sqlite3")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            price REAL,
            currency TEXT        
        )
    """)
    conn.commit()
    conn.close()

def insert_book(title, price, currency):
    conn = sqlite3.connect("books.sqlite3")
    cursor = conn.cursor()
    cursor.execute(
        """ 
            INSERT INTO books (title, price, currency) VALUES (?, ? , ?)
        """,
            (title,price, currency),
    )
    conn.commit()
    conn.close()

def scrape_book(url):
    response = requests.get(url)
    if response.status_code != 200:
        return
    
    # Set encoding explicitly to handle special characters
    response.encoding = response.apparent_encoding

    #print(response.text) -> shows index.html

    soup = BeautifulSoup(response.text, "html.parser")
    books = soup.find_all("article" , class_ = "product_pod")
    #print(books)-> shows the lists
    for book in books:
        title= book.h3.a["title"]
        price_text = book.find("p" , class_ = "price_color").text

        #print(title, price_text)

        currency = price_text[0]
        price = price_text[1:]
        insert_book(title,price,currency)

create_database()
scrape_book("http://books.toscrape.com/")




