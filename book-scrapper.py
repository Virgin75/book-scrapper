from models import *
import os

print('Start scrapping, please wait...')

# Create empty directory for assets (book pictures and CSV)
current_directory = os.getcwd()
final_directory = os.path.join(current_directory, r'assets')
if not os.path.exists(final_directory):
    os.makedirs(final_directory)

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
