from models import *
import os
import time

start_time = time.time()

print('👉 Please wait, scrapping categories of books...')

# Create empty directory for assets (book pictures and CSV)
current_directory = os.getcwd()
final_directory = os.path.join(current_directory, r'assets')
if not os.path.exists(final_directory):
    os.makedirs(final_directory)

task_category_list = []

soup = BeautifulSoup(requests.get(
    'http://books.toscrape.com/index.html').text, 'html.parser')

navList = soup.find("ul", {"class": "nav nav-list"}).li.ul.find_all("li")

for category in navList:
    url_of_category = 'http://books.toscrape.com/' + category.a.attrs['href']
    task_category_list.append(Category(url_of_category).get_list_of_books())


async def async_task():

    for future in asyncio.as_completed(task_category_list):
        category = await future

        async def get_book_data(book_url):
            book = await Book().create(book_url)
            await book.download_picture()
            await book.save_to_csv()

        await asyncio.gather(*[get_book_data(book_url) for book_url in category])


asyncio.run(async_task())


print(f'--- {time.time() - start_time} seconds ---')
print('Done.')
