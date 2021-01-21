import requests
from bs4 import BeautifulSoup
from math import *
import csv
import re

books = []

'''
Fonction qui récupère toutes les infos liées à un 
livre (prix, titre, etc.) à partir d'une URL de page produit
'''


def get_book_data(book_url):
    book_data = {
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

    book_page = requests.get(book_url)
    soup = BeautifulSoup(book_page.content, 'html.parser')

    book_data["product_page_url"] = book_url

    book_data["universal_product_code"] = soup.find(
        'div', id='content_inner').article.table.find_all('tr')[0].td.string

    book_data["title"] = soup.find(
        'div', id='content_inner').article.find_all('div')[0].find(
            "div", {"class": "col-sm-6 product_main"}).h1.string

    book_data["price_including_tax"] = soup.find(
        'div', id='content_inner').article.table.find_all('tr')[3].td.string

    book_data["price_excluding_tax"] = soup.find(
        'div', id='content_inner').article.table.find_all('tr')[2].td.string

    book_data["number_available"] = soup.find(
        'div', id='content_inner').article.table.find_all('tr')[5].td.string

    book_data["product_description"] = soup.find(
        'div', id='content_inner').article.find_all('p')[3].string

    book_data["category"] = soup.find_all(
        "div", {"class": "page_inner"})[1].ul.find_all('li')[2].a.string

    book_data["review_rating"] = soup.find(
        'div', id='content_inner').article.find_all('div')[0].find(
            "div", {"class": "col-sm-6 product_main"}).find_all('p')[2].attrs['class'][1] + " out of five stars."

    book_data["image_url"] = "http://books.toscrape.com/" + \
        soup.find_all('img')[0].attrs['src'][6:]

    books.append(book_data)
    download_book_picture(url=book_data['image_url'], title=book_data['title'])


'''
Fonction qui télécharge l'image d'un livre sur le disque dur
'''


def download_book_picture(url, title):
    picture = requests.get(url)
    formatted_title = re.sub(r'\W+', '', title)
    with open(f'{formatted_title}.jpg', 'wb') as file:
        file.write(picture.content)


'''
Fonction qui récupère une liste de livres à partir de l'URL d'une page de catégorie, 
puis génère le .CSV pour chaque catégorie en récupérant les données de chaque livre 
via get_book_data()
'''


def get_books_from_category(category_url):

    category_books = []
    category_page = requests.get(category_url)
    soup = BeautifulSoup(category_page.text, 'html.parser')

    number_of_books = soup.find_all('form')[0].find_all('strong')[0].string
    number_of_pages = ceil(int(number_of_books) / 20)

    category_name = soup.find('h1').string

    for i in range(1, number_of_pages + 1):
        if i != 1:
            next_page_url = category_url[:-10] + '/page-' + str(i) + '.html'
            next_page = requests.get(next_page_url)
            soup = BeautifulSoup(next_page.text, 'html.parser')

        books_on_category_page = soup.find_all('article')

        for book in books_on_category_page:

            url = book.h3.a.attrs['href']
            new_book = "http://books.toscrape.com/catalogue/" + url[9:]
            category_books.append(new_book)

    for book_Url in category_books:
        get_book_data(book_Url)

    # Export all books of the category in CSV
    keys = books[0].keys()
    with open('books-%s.csv' % (category_name), 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(books)

    books.clear()
    print(f'{category_name} books have been scrapped in
          "books-{category_name}.csv file"')


'''
Fonction qui récupère la liste des catégories de livres, puis lance
le process en appelant la fonction get_books_from_category()
'''


def get_all_data():
    print(f'Start scrapping, please wait...')
    soup = BeautifulSoup(requests.get(
        'http://books.toscrape.com/index.html').text, 'html.parser')

    categories_list = []

    navList = soup.find("ul", {"class": "nav nav-list"}).li.ul.find_all("li")

    for category in navList:
        categories_list.append(
            'http://books.toscrape.com/' + category.a.attrs['href'])

    for category_URL in categories_list:
        get_books_from_category(category_URL)


get_all_data()
