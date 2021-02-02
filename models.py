import requests
from bs4 import BeautifulSoup
from math import *
import re
import csv
import asyncio


class Book:

    @classmethod
    async def create(cls, url):
        loop = asyncio.get_event_loop()

        self = Book()
        self.product_page_url = url
        print(f'{url} : creation started')

        book_page = await loop.run_in_executor(None, requests.get, url)
        soup = BeautifulSoup(book_page.content, 'html.parser')

        self.title = soup.find(
            'div', id='content_inner').article.find_all('div')[0].find(
            "div", {"class": "col-sm-6 product_main"}).h1.string
        self.universal_product_code = soup.find(
            'div', id='content_inner').article.table.find_all('tr')[0].td.string
        self.price_including_tax = soup.find(
            'div', id='content_inner').article.table.find_all('tr')[3].td.string
        self.price_excluding_tax = soup.find(
            'div', id='content_inner').article.table.find_all('tr')[2].td.string
        self.number_available = soup.find(
            'div', id='content_inner').article.table.find_all('tr')[5].td.string
        self.product_description = soup.find(
            'div', id='content_inner').article.find_all('p')[3].string
        self.category = soup.find_all(
            "div", {"class": "page_inner"})[1].ul.find_all('li')[2].a.string
        self.review_rating = soup.find(
            'div', id='content_inner').article.find_all('div')[0].find(
            "div", {"class": "col-sm-6 product_main"}).find_all('p')[2].attrs['class'][1] + " out of five stars."
        self.image_url = "http://books.toscrape.com/" + \
            soup.find_all('img')[0].attrs['src'][6:]

        print(f'{url} : CREATED')

        return self

    def save_to_csv(self, category_title):

        keys = self.__dict__.keys()
        with open('assets/books-%s.csv' % (category_title), 'w', newline='') as file:
            dict_writer = csv.DictWriter(file, keys)
            dict_writer.writeheader()
            dict_writer.writerow(self.__dict__)

    async def download_picture(self):

        loop = asyncio.get_event_loop()

        picture = await loop.run_in_executor(None,
                                             requests.get,
                                             self.image_url)
        formatted_title = re.sub(r'\W+', '', self.title)
        with open(f'assets/{formatted_title}.jpg', 'wb') as file:
            return file.write(picture.content)


class Category:
    def __init__(self, url):
        category_page = requests.get(url)
        soup = BeautifulSoup(category_page.text, 'html.parser')

        self.url = url
        self.title = soup.find('h1').string
        self.number_of_books = soup.find_all(
            'form')[0].find_all('strong')[0].string
        self.number_of_pages = ceil(int(self.number_of_books) / 20)

    async def get_list_of_books(self):
        list_of_books = []
        loop = asyncio.get_event_loop()

        for i in range(1, self.number_of_pages + 1):
            if i != 1:
                next_page_url = self.url[:-10] + \
                    '/page-' + str(i) + '.html'
                next_page = await loop.run_in_executor(None,
                                                       requests.get,
                                                       next_page_url)
                soup = BeautifulSoup(next_page.text, 'html.parser')
            else:
                first_page = await loop.run_in_executor(None,
                                                        requests.get,
                                                        self.url)
                soup = BeautifulSoup(first_page.text, 'html.parser')

            books_on_page = soup.find_all('article')

            for book in books_on_page:
                url = book.h3.a.attrs['href']
                new_book = "http://books.toscrape.com/catalogue/" + url[9:]
                list_of_books.append(new_book)

        return list_of_books
