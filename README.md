# Example of parsing(crawling) [yelp.com](www.yelp.com) site

Installation:
  - Download the latest version of [Chromedriver](https://sites.google.com/a/chromium.org/chromedriver/downloads)
  - Unzip and put chromedriver into project directory
  - Go to the [yelp.com](www.yelp.com) and enter your query in the search bar
  - Copy current url
  - Change domain (in main.py) to current url
  - Save main.py
  - type pip3 install -r requirements.txt
  - python3 main.py and wait :)

# Features!

  - Save extracted data into result.xls file in the project directory
  - Multiprocessing

# - result.xls format
| company_name | url | website_url | rating | city_and_state | phone |
| ------ | ------ | ------ | ------ | ------ | ------ |
| Flat Price Moving & Auto Shipping | https://www.yelp.com/biz/flat-price-moving-and-auto-shipping-san-francisco?osq=Movers | flatpriceautotransport.com|4.5|San Francisco, CA 94123|(415) 000-0000 |
