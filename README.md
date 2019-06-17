# Emag MultiThreaded Product-price Scraper

### Requirements
  * Python 3
  * Requests
  * Bs4
   
### How to use
	After you compile the main.py file you will be requested to input a product name (example: Samsung, Apple etc)
In the end the script will output a csv file that cotains the name, the link and the price.

### Possible issues that may appear
  * You may get temporarly banned because of the big suddenly requests ( possible solution would be to implement a way to use proxies)
  * The output file may be messed up because of the multiprocessing ( possible solution would be to use a multiprocessing queue ) 