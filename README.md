# BooksToRead
Python based application that scrapes the "New Release" section of goodreads.com and saves the books into a CSV file

The "New Realease" section is updated every week and is built with a dynamic URL.
Therefore I used Selenium to navigate to the corresponding URL. 
The data then gets scraped using BeautifulSoup library.

## What I learned / used for the first time:
- Automating the webiste-navigation process, using Selenium Webdriver
- Defining an explicit wait for the Webdriver and setting Expected Conditions, to make sure all elements are fully loaded before continuing
- Scrape content from a website using BeautifulSoup and prepare the data for further processing
  
