import csv
import json
import requests
from bs4 import BeautifulSoup
import sqlite3
URL = "http://books.toscrape.com/"
 
def create_table():
 
   
    con = sqlite3.connect('book.sqlite3')
    cur = con.cursor()
    cur.execute(
         """
            CREATE TABLE IF NOT EXISTS book(
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 title TEXT,
                 currency TEXT,
                 price REAL
         );
    """
    )
    con.close()
    print('Database and table created successfully.')
 
 
def insert_book(title,currency,price):
    con = sqlite3.connect("book.sqlite3")
    cur = con.cursor()
    cur.execute(
        "INSERT INTO book(title,currency,price)VALUES(?,?,?)",
        (title,currency,price),
    )
    con.commit()
    con.close()
def scrape_book(url):
    response = requests.get(url)
    if response.status_code!= 200:
        return
    response.encoding = response.apparent_encoding
 
   
    soup = BeautifulSoup(response.text,"html.parser")
    book_element = soup.find_all("article",class_="product_pod")
    for book in book_element:
        title = book.h3.a['title']
     
        price_text = book.find("p",class_ = "price_color").text
        currency = price_text[0]
        price = float(price_text[1:])
        print(title,currency,price)
        insert_book(title,currency,price)

        book.append(
            {
                'title':title,
                'currency':currency,
                'price':price,
            }
        )
 
    print("all all books are scrapped.")
    return book
def save_to_json(book):
    
    with open('book.json','w',encoding='utf-8')as f:
        json.dump(book,f,indent=2,ensure_ascii=False)
def save_to_csv(book):
    
    with open('books.csv','w',newline="",encoding="utf=8")as f:
        writer=csv.DictWriter(f,fieldnames=['title','currency','price'])
        writer.writeheader()
        writer.writerows(book)
    
 
create_table()
book=scrape_book(URL)
print(book)
