# What is book-scrapper?

book-scrapper is a Python CLI script to scrap data of the books on [Books To Scrape website](http://books.toscrape.com/)

After successful execution, you will get one .csv file per book category. Each .csv file will be downloaded in your working directory. All the cover pictures of all the books will also be downloaded in .jpg format.

Each line of the .csv file will have the folowing columns :

- product_page_url
- universal_product_code
- title
- price_including_tax
- price_excluding_tax
- number_available
- product_description
- category
- review_rating
- image_url

# Usage:

## Usage

1. Download this repo locally
2. Create a virtual env & activate it

```bash
$ python3 -m venv env
$ source env/bin/activate

```

3. Install all dependencies

```bash
$  pip3 install -r requirements.txt
```

4. Run it

```bash
$  python3 book-scrapper.py
```
