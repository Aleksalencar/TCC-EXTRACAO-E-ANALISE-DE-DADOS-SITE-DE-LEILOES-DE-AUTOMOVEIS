from datetime import date
from datetime import datetime
import json
from math import ceil
import os
from pprint import pprint
import re
from requests_html import HTMLSession

import requests
from lxml import html
from os.path import exists

import csv


class Sandre():
    def __init__(self) -> None:
        pass

    def get_data(self):
        today = date.today()
        csv_file = fr"C:\Users\Aleksander\Documents\GitHub\AuctionMinerBot\sandre_{today}.csv"
        csv_columns = ['url', 'brand', 'name', 'year', 'actual_bid', 'local', 'date', 'Placa',
                       'Cor', 'KM', 'Combustível', 'Direção Hidráulica/Elétrica', 'Ar Condicionado', 'Câmbio (Moto)',  'Câmbio', 'Origem', 'Kit Gás', 'Blindagem', 'Estado do Chassi']
        
        if exists(csv_file):
            print("File already colected")
            exit()
            

        with open(csv_file, 'a', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()

        url = "https://www.sodresantoro.com.br/veiculos/ordenacao/data_leilao/tipo-ordenacao/crescente/qtde-itens/30/visualizacao/visual_imagemlista/item-atual/1/pagina/1/v_categoria/carros;utilitarios-leves/v_sinistro/sem-sinistro/v_km/1%7C19999;40000%7C59999;60000%7C79999;80000%7C99999;100000%7C119999;120000%7C139999;140000%7C/v_combustivel/diesel;flex;gasolina/"
        page = self.search(url)
        total_items = self.get_total_items(page)
        total_items = int(total_items)
        total_pages = ceil(total_items / 30)
        for page_number in range(2, total_pages + 2):

            auctions_links = self.get_auctions(page)
            for link in auctions_links:
                auction_page = self.parse_auction(link)

                name = self.get_name(auction_page)
                if not name:
                    continue

                data = {
                    'url': link,
                    'name': name,
                    'year': self.get_year(name),
                    'actual_bid': self.get_actual_bid(auction_page),
                    'local': self.get_local(auction_page),
                    'date': self.get_date(auction_page),
                    'brand': name.split(" ")[5]
                }

                details = self.get_datails(auction_page)
                data.update(details)
                
                pprint(data)
                with open(csv_file, 'a', encoding='utf-8') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
                    writer.writerow(data)

            # Getting next page
            url = f"https://www.sodresantoro.com.br/veiculos/ordenacao/data_leilao/tipo-ordenacao/crescente/qtde-itens/30/visualizacao/visual_imagemlista/item-atual/1/pagina/{page_number}/v_categoria/carros;utilitarios-leves/v_sinistro/sem-sinistro/v_km/1%7C19999;40000%7C59999;60000%7C79999;80000%7C99999;100000%7C119999;120000%7C139999;140000%7C/v_combustivel/diesel;flex;gasolina/"
            page = self.search(url)

    def search(self, url):
        self.session = HTMLSession()
        response = self.session.get(url)
        return response

    def get_total_items(self, initial_page):

        total_items = re.search(
            "[0-9]+(?=</b> lotes)", initial_page.text).group()
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

        name = auction_page.xpath('//h1/text()')
        name = ''.join(name)
        if not "Leilão" in name:
            return None
        name = name.strip()
        name = name.replace("  ", " ")
        print(name)
        return name

    def get_year(self, nome):
        year = nome.split(" ")[-1]
        years = year.split("/")
        years_list = []
        for year in years:
            try:
                try:
                    year = datetime.strptime(year, "%Y")
                except ValueError:
                    year = datetime.strptime(year, "%y")
            except:
                continue

            year = year.year
            years_list.append(year)
        return years_list

    def get_datails(self, auction_page):
        lis = auction_page.xpath(
            '//*[@id="coluna4"]/div[3]/div[1]/div[8]/div/div[1]/ul/li')
        details = {}
        for li_i in range(1, len(lis) + 1):
            key = auction_page.xpath(
                f'//*[@id="coluna4"]/div[3]/div[1]/div[8]/div/div[1]/ul/li[{li_i}]/p/text()')[0]
            key = key.strip()
            key = key.replace(":", "")

            value = auction_page.xpath(
                f'//*[@id="coluna4"]/div[3]/div[1]/div[8]/div/div[1]/ul/li[{li_i}]/p/b')[0].text
            if value:
                value = value.strip()
            details[key] = value

        return details

    def get_actual_bid(self, auction_page):
        bid = auction_page.xpath('//*[@class="valor"]')[0].text
        return bid

    def get_local(self, auction_page):
        local = auction_page.xpath(
            '//p[contains(text(),"Local do lote")]')[0].text
        return local

    def get_date(self, auction_page):
        date_text = auction_page.xpath(
            '//*[@id="statusLote_id"]/span/span')[0].text
        try:
            date = datetime.strptime(date_text, "%d/%m - %H:%M")
        except ValueError:
            return None

        date = date.replace(year=date.today().year)
        date = date.strftime("%d/%m/%Y, %H:%M:%S")
        return date


if __name__ == '__main__':
    s = Sandre()
    s.get_data()
