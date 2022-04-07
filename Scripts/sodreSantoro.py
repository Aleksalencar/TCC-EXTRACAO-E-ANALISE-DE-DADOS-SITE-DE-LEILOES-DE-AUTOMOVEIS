from math import ceil
from pprint import pprint
import re
from tkinter import N
from tkinter.messagebox import NO
from requests_html import HTMLSession

import requests
from lxml import html


class Sandre():
    def __init__(self) -> None:
        pass 
    
    def search(self, url):
        self.session = HTMLSession()
        response =  self.session.get(url)
        return response
    
    def get_total_items(self, initial_page):
        
        total_items = re.search("[0-9]+(?=</b> lotes)", initial_page.text).group()
        total_items = int(total_items)
        return total_items
    
    def get_auctions(self, initial_page):
        links = initial_page.html.links
        auction_links = []
        
        base_url = "https://www.sodresantoro.com.br"
        for link in links:
            if "/leilao/" in link:
                auction_links.append(base_url + link)
        return auction_links
    
    def parse_auction(self, url):
        print(f"getting {url}")
        page = requests.get(url)
        tree = html.fromstring(page.content)
        return tree
    
    def get_name(self, auction_page):
        
        name = auction_page.xpath('//h1')[0].text
        if not "Leilão" in name:
            return None
        name = name.strip()
        print(name)
        return name
    
    def get_year(self, nome):
        year = nome.split(" ")[-1]
        years = year.split("/")
        years_list = []
        for year in years:
            year = int(year)
            years_list.append(year)
        return years_list
        
    def get_datails(self, auction_page):
        lis = auction_page.xpath('//*[@id="coluna4"]/div[3]/div[1]/div[8]/div/div[1]/ul/li')
        a = {}
        for li_i in range(1, len(lis)+1):
            key = auction_page.xpath(f'//*[@id="coluna4"]/div[3]/div[1]/div[8]/div/div[1]/ul/li[{li_i}]/p/text()')[0]
            key = key.strip()
            key = key.replace(":", "")
            
            value = auction_page.xpath(f'//*[@id="coluna4"]/div[3]/div[1]/div[8]/div/div[1]/ul/li[{li_i}]/p/b')[0].text
            if value:
                value = value.strip()
            a[key] = value
            
        print(a)
            
            

sandre = Sandre()
url = "https://www.sodresantoro.com.br/veiculos/ordenacao/data_leilao/tipo-ordenacao/crescente/qtde-itens/30/visualizacao/visual_imagemlista/item-atual/1/pagina/1"
page = sandre.search(url)
total_items = sandre.get_total_items(page)
total_items = int(total_items)
total_pages = ceil(total_items/30)
for page_number in range(2, total_pages+2): 
    auctions_links = sandre.get_auctions(page)
    for link in auctions_links:
        auction_page =  sandre.parse_auction(link)
        
        name = sandre.get_name(auction_page)
        if not name:
            continue
        
        details = sandre.get_datails(auction_page)
        
        data = {
            'nome': name,
            'ano': sandre.get_year(name)
        }
        pprint(data)
    
    # Getting next page
    url = url.split("/")
    url[-1] = str(page_number)
    url = "/".join(url)
    page = sandre.search(url)
    




