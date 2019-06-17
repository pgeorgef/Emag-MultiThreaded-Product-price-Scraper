import requests
import csv
import os
import time
from bs4 import BeautifulSoup
import multiprocessing
url = []
class EmagScraper():
    def __init__(self):
        self.pag = 1
        i = 0

    def get_urls(self,main_url):
        self.url = 'https://www.emag.ro/search/'+ main_url +'/p1'
        self.filename = main_url
        r = requests.get(self.url)
        soup = BeautifulSoup(r.text, 'html.parser')
        numar_pagini = soup.find(class_= 'row' )
        ultima_pagina = numar_pagini.find_all('a')[len(numar_pagini.find_all('a'))-2].get("data-page")
        for i in range(1, int(ultima_pagina)+1):
            url.append('https://www.emag.ro/search/'+ main_url +'/p' + str(i))
    def print_urls(self):
        for urls in url:
            print (urls)

    def scrape(self,url):
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        lista_produse = soup.find(class_ = 'page-container')
        lista_produse_nume = lista_produse.find_all('h2')
        lista_produse_pretvechi = lista_produse.find_all(class_ = 'product-old-price')
        lista_produse_pretnou = lista_produse.find_all(class_ = 'product-new-price')
        for i in range(0, len(lista_produse_nume)):
            nume = lista_produse_nume[i].get_text().strip()
            link = lista_produse_nume[i].find('a').get('href')
            #print(nume)
            #print(len(nume))
            try:
                pret = lista_produse_pretvechi[i].contents[0].get_text()
                pret = pret[:-6]
                #print(pret)
            except IndexError:
                #print("no old price")
                pret = 'Nu exista'
            #print(lista_produse_pretnou[i].contents[0])
            with open(self.filename+'.csv', 'a', encoding = 'utf-8', newline='') as csv_file:
                file_is_empty = os.stat(self.filename+'.csv').st_size == 0
                fieldname = ['nume','link', 'pret_vechi', 'pret_actual']
                writer = csv.DictWriter(csv_file, fieldnames = fieldname)
                if file_is_empty:
                    writer.writeheader()
                writer.writerow({'nume':nume,'link':link, 'pret_vechi':pret, 'pret_actual':lista_produse_pretnou[i].contents[0]})
if __name__=='__main__':
    print("Search for product: ")
    urlsearch = input()
    starttime = time.time()
    scraper = EmagScraper()
    scraper.get_urls(urlsearch)
    scraper.print_urls()
    #scraper.scrape(url[0])
    pool = multiprocessing.Pool()
    pool.map(scraper.scrape,url)
    pool.close()
    print('That took {} seconds'.format(time.time() - starttime))
