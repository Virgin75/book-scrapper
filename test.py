import requests
from bs4 import BeautifulSoup

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
    soup = BeautifulSoup(bookPage.text, 'html.parser')

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

    print(bookData)


getBookData("http://books.toscrape.com/catalogue/forever-and-forever-the-courtship-of-henry-longfellow-and-fanny-appleton_894/index.html")
