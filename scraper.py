from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
import sqlite3
 
conn = sqlite3.connect("books.db")
 
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS books(
title TEXT,
price INTEGER,
rating INTEGER
)""")
conn.commit()
conn.close()
 
urls = []
 
special_url = "http://books.toscrape.com/"
urls.append(special_url)

for i in range(2, 51):
   urls.append("http://books.toscrape.com/catalogue/page-" + str(i) +".html")
 
 
titles = []
prices = []
ratings = []
 
for url in urls:
   get = requests.get(url)
   soup = bs(get.content, "html.parser")
   bookshelf = soup.findAll("li", {"class": "col-xs-6 col-sm-4 col-md-3 col-lg-3"})
 
   for book in bookshelf:
      title = book.h3.a["title"]
 
      price = book.findAll("p", {"class": "price_color"})[0].text.strip()
      price = price.replace("£", "")
      price = float(price)
 
      rating = str(book.findAll("p")[0])[21:27]
      rating = rating.replace('"', "")
      rating = rating.replace(">", "")
    
      titles.append(title)
      prices.append(price)
      ratings.append(rating)
 
conn = sqlite3.connect("books.db")
cursor = conn.cursor()
for i in range(len(titles)):
   cursor.execute("INSERT INTO books (title, price, rating) VALUES (?, ?, ?)", 
(titles[i], prices[i], ratings[i]))
conn.commit()
conn.close()
 
dict_obj = {
"title": titles,
"price": prices,
"ratings": ratings
}
 
df = pd.DataFrame(dict_obj)
df.to_csv("books.csv")