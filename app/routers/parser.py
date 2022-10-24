# https://taxi.yandex.ru/?utm_source&utm_medium&gfrom=49.87914849407354,%2073.19671863397491&gto=49.858332124564384,73.19832658597096&ref=yoursiteru&level=50



# import requests
# from bs4 import BeautifulSoup

# url = 'https://taxi.yandex.ru/?utm_source&utm_medium&gfrom=49.87914849407354,%2073.19671863397491&gto=49.858332124564384,73.19832658597096&ref=yoursiteru&level=50'
# response = requests.get(url)
# soup = BeautifulSoup(response.text, 'lxml')
# quotes = soup.find_all('span')\

# for quote in quotes:
#     print(quote.text,"\n")    

# print(soup)


parse_url = "https://taxi.yandex.ru/?utm_source&utm_medium&gfrom=49.87914849407354,%2073.19671863397491&gto=49.858332124564384,73.19832658597096&ref=yoursiteru&level=50"

from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
import os

# Use sync version of Playwright
with sync_playwright() as p:
    # Launch the browser
    browser = p.chromium.launch()

    # Open a new browser page
    page = browser.new_page()

    # Create a URI for our test file
    page_path = parse_url

    # Open our test file in the opened page
    page.goto(page_path)
    page_content = page.content()

    # Process extracted content with BeautifulSoup
    soup = BeautifulSoup(page_content)
    # print(soup.find(id="test").get_text())
    print(soup)

    # Close browser
    browser.close()