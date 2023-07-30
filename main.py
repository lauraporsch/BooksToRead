import bs4
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv


GOOD_READS = "https://www.goodreads.com/genres"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "Accept-Language": "en-CA,en;q=0.9,de-DE;q=0.8,de;q=0.7,en-GB;q=0.6,en-US;q=0.5,fr;q=0.4",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7"
}

# # create csv file (only running first time)
# with open('books_to_read.csv', mode='w', encoding='utf-8', newline='') as books_to_read:
#     writer = csv.writer(books_to_read)
#     field = ["title", "author", "rating (out of 5)", "summary"]
#     writer.writerow(field)

# using chrome as browser, pre-downloaded chrome driver
chrome_driver_path = "chromedriver.exe"
service = Service(chrome_driver_path)

# use options so window stays open and doesn't close unless you tell it to
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=options, service=service)

# define a maximum wait-time of 10 seconds for Selenium
# (used instead of time.sleep() to keep processing time to a minimum)
wait = WebDriverWait(driver, 10)

# open website full screen
driver.get(GOOD_READS)
driver.maximize_window()

# navigate to "New Releases" page (dynamic URL changing monthly, therefore not able to open directly)
browse_button = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div[1]/div/header/div['
                                                                 '2]/div/nav/ul/li[3]/div/a')))
browse_button.click()
new_releases = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div[1]/div/header/div['
                                                                '2]/div/nav/ul/li[3]/div/div/div/ul/li[5]/a')))
new_releases.click()

# close popup
close_popup = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[3]/div/div[1]/div')))
close_popup.click()

# get current (dynamic) URL and  scrape content with BeautifulSoup
url = driver.current_url

response = requests.get(url=url, headers=HEADERS)
goodreads_new_releases = response.text
soup = bs4.BeautifulSoup(goodreads_new_releases, "html.parser")

books = soup.find_all(name="div", class_="BookListItem__body")
book_info = []

for book in books:
    title = book.find(name="h3", class_="Text Text__title3 Text__umber").getText()
    author = book.find(name="div", class_="BookListItem__authors").getText()
    rating_info = book.find(name="div", class_="BookListItemRating").getText()
    rating = rating_info[:4]
    summary = book.find(name="div", class_="TruncatedContent").getText()
    book_info += [[title, author, rating, summary]]

# add books to CSV file
with open('books_to_read.csv', mode='a', encoding='utf-8', newline='') as books_to_read:
    writer = csv.writer(books_to_read)
    writer.writerows(book_info)
