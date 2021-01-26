from models import *

print('Start scrapping, please wait...')

soup = BeautifulSoup(requests.get(
    'http://books.toscrape.com/index.html').text, 'html.parser')

navList = soup.find("ul", {"class": "nav nav-list"}).li.ul.find_all("li")

for category in navList:
    url_of_category = 'http://books.toscrape.com/' + category.a.attrs['href']
    cat = Category(url_of_category)
    books_in_category = cat.get_list_of_books()

    for book_url in books_in_category:
        book = Book(book_url)
        book.save_to_csv(cat.title)
        book.download_picture()

print('Done.')
