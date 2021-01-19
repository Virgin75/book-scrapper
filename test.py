import requests
from bs4 import BeautifulSoup
from math import *
import csv
import random

books = []
# Fonction qui récupère toutes les infos liées à un livre (prix, titre, etc.)


def getBookData(bookUrl):
    bookData = {
        "product_page_url": "",
        "universal_product_code": "",
        "title": "",
        "price_including_tax": "",
        "price_excluding_tax": "",
        "number_available": "",
        "product_description": "",
        "category": "",
        "review_rating": "",
        "image_url": ""
    }

    bookPage = requests.get(bookUrl)
    soup = BeautifulSoup(bookPage.content, 'html.parser')

    bookData["product_page_url"] = bookUrl

    bookData["universal_product_code"] = soup.find(
        'div', id='content_inner').article.table.find_all('tr')[0].td.string

    bookData["title"] = soup.find(
        'div', id='content_inner').article.find_all('div')[0].find(
            "div", {"class": "col-sm-6 product_main"}).h1.string

    bookData["price_including_tax"] = soup.find(
        'div', id='content_inner').article.table.find_all('tr')[3].td.string

    bookData["price_excluding_tax"] = soup.find(
        'div', id='content_inner').article.table.find_all('tr')[2].td.string

    bookData["number_available"] = soup.find(
        'div', id='content_inner').article.table.find_all('tr')[5].td.string

    bookData["product_description"] = soup.find(
        'div', id='content_inner').article.find_all('p')[3].string

    bookData["category"] = soup.find_all(
        "div", {"class": "page_inner"})[1].ul.find_all('li')[2].a.string

    bookData["review_rating"] = soup.find(
        'div', id='content_inner').article.find_all('div')[0].find(
            "div", {"class": "col-sm-6 product_main"}).find_all('p')[2].attrs['class'][1] + " out of five stars."

    bookData["image_url"] = "http://books.toscrape.com/" + \
        soup.find_all('img')[0].attrs['src'][6:]

    books.append(bookData)


def getBooksOfCategory(categoryUrl):

    categoryBooks = []
    bookPage = requests.get(categoryUrl)
    soup = BeautifulSoup(bookPage.text, 'html.parser')

    numberOfBooks = soup.find_all('form')[0].find_all('strong')[0].string
    numberOfPage = ceil(int(numberOfBooks) / 20)

    for i in range(1, numberOfPage + 1):
        if i != 1:
            nextPageUrl = categoryUrl[:-10] + '/page-' + str(i) + '.html'
            bookPage = requests.get(nextPageUrl)
            soup = BeautifulSoup(bookPage.text, 'html.parser')

        booksOnPage = soup.find_all('article')

        for book in booksOnPage:

            bookURL = book.h3.a.attrs['href']
            newBook = "http://books.toscrape.com/catalogue/" + bookURL[9:]
            categoryBooks.append(newBook)

    for bookURL in categoryBooks:
        getBookData(bookURL)

    # Export all books of the category in CSV
    keys = books[0].keys()
    with open('books-%s.csv' % (random.randint(0, 999)), 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(books)

    books.clear()


def getAllData():
    soup = BeautifulSoup(requests.get(
        'http://books.toscrape.com/index.html').text, 'html.parser')

    categoriesList = []

    navList = soup.find("ul", {"class": "nav nav-list"}).li.ul.find_all("li")

    for category in navList:
        categoriesList.append(
            'http://books.toscrape.com/' + category.a.attrs['href'])

    for categoryURL in categoriesList:
        getBooksOfCategory(categoryURL)


# getBookData("http://books.toscrape.com/catalogue/forever-and-forever-the-courtship-of-henry-longfellow-and-fanny-appleton_894/index.html")
# getBooksOfCategory("http://books.toscrape.com/catalogue/category/books/historical-fiction_4/index.html")
getAllData()
