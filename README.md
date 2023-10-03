# FYP-reccomender-system

Prerequisites:
- pip install selenium
- pip install beautifulsoup4
- pip install pandas
- pip install openpyxl

Scraping program:
- For every product page:
  - For each product:
    - Scrape Product Name, Price, Total Sold, Seller, Description, Image, Product Page
    Note: Price is a string, image & product page are URLs
          Seller & description is scraped when entering the product page url
    - For each review page:
      - Scrape Product Name, Rating, Reviewer, Content

When CAPTCHA appears:
- Program will stall until it is MANUALLY COMPLETED (User intervention required)
- If it is a review page, return to the previous page
    Note: After solving captcha, there is a tendency for duplicate review pages to be recorded

On program crash/finish:
- Remove duplicates from collected data with pandas
- Save products & reviews to seperate xlsx files

If there is a CRASH, starting the program SHOULD pick up from the last product it stopped at by checking for duplicate product entries (Not tested enough)
