from models import *
import os
import time

start_time = time.time()

print('Start scrapping, please wait...')

# Create empty directory for assets (book pictures and CSV)
current_directory = os.getcwd()
final_directory = os.path.join(current_directory, r'assets')
if not os.path.exists(final_directory):
    os.makedirs(final_directory)

# Empty list of categories
task_category_list = []

soup = BeautifulSoup(requests.get(
    'http://books.toscrape.com/index.html').text, 'html.parser')

navList = soup.find("ul", {"class": "nav nav-list"}).li.ul.find_all("li")

for category in navList:
    url_of_category = 'http://books.toscrape.com/' + category.a.attrs['href']
    task_category_list.append(Category(url_of_category).get_list_of_books())


async def async_task():
    task_book_list = []

    categories = await asyncio.gather(*task_category_list)
    flat_list = [item for sublist in categories for item in sublist]

    print(flat_list)

    for book_url in flat_list:
        task_book_list.append(Book().create(book_url))

    books = await asyncio.gather(*task_book_list)

    print(books)

    async def get_data(book):
        await book.download_picture()
        book.save_to_csv(book.category)

    await asyncio.gather(*[get_data(book) for book in books])


asyncio.run(async_task())

print("--- %s seconds ---" % (time.time() - start_time))
print('Done.')
