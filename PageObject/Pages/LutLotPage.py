import json
import re
from datetime import datetime, date

import requests
from lxml import html
from pathlib import Path

from PageObject.Pages.Locators import LocatorLotPage as Locator
from PageObject.TestBase.logger_setup import LoggingConfig

logging = LoggingConfig()
logging = logging.get_logging()


class LotPage:
    def __init__(self, url):
        logging.info("[def] __init__")
        logging.info("url = " + url)
        self.url = url
        logging.info(self.url)

        # Parse lot page
        page = requests.get(self.url)
        self.tree = html.fromstring(page.content)

        pass

    def get_lot_info(self):
        site_lot_id = self.url.split("/")[-1]
        site_lot_id = int(site_lot_id)

        actual_bid = self.tree.xpath(Locator.ACTUAL_BID_XPATH)[0].text

        opening_date = self.tree.xpath(Locator.OPENING_DATE_XPATH)[0].text
        opening_date = self.__remove_escapes(opening_date)

        ending_date = self.tree.xpath(Locator.ENDING_DATE_XPATH)[0].text
        ending_date = self.__remove_escapes(ending_date)

        minimal_increment = self.tree.xpath(Locator.MINIMAL_INCREMENT_XPATH)[0].text

        today = date.today()
        today = datetime(today.year, today.month, today.day)

        ending_datetime = datetime.strptime(ending_date, '%d/%m/%Y %H:%M:%S')
        opening_datetime = datetime.strptime(opening_date, '%d/%m/%Y')

        lot_stats = "Not OK"

        if today < opening_datetime:
            lot_stats = "Aguardando"
        if opening_datetime <= today <= ending_datetime:
            lot_stats = "Aberto"
        if today > ending_datetime:
            lot_stats = "Fechado"

        info = {
            'url': self.url,
            'site_lot_id': site_lot_id,
            'actual_bid': actual_bid,
            'opening_date': opening_date,
            'ending_date': ending_date,
            'minimal_increment': minimal_increment,
            'lot_status': lot_stats
        }

        logging.info('info = ' + str(info))

        return info

    def get_car_info(self):
        car_title = self.tree.xpath(Locator.CAR_TITLE_XPATH)[0].text

        car_title = self.__remove_escapes(car_title)
        car_title = car_title.replace("Veículo ", "")
        car_title = car_title.upper()

        brand = self.compare_car_brand(car_title)

        # from index 1 until the end
        car_title.split(' ', 1)
        model = car_title.split(' ', 1)[1]
        logging.info("model = " + model)

        appraisal_value = self.get_appraisal_value()

        year = self.get_year()

        car_info = {
            'brand': brand,
            'model': model,
            'year': year,
            'appraisal_value': appraisal_value,
            'location': "",
        }
        return car_info

    @staticmethod
    def __remove_escapes(string):
        string = string.replace("\t", "")
        string = string.replace("\r", "")
        string = string.replace("\n", "")
        string = string.strip()
        return string

    @staticmethod
    def compare_car_brand(string):
        brand_file_path = Path(__file__).parent.parent.parent.joinpath(r'Resources\Brands.txt')
        logging.info(brand_file_path)

        car_brands = [line.strip() for line in open(brand_file_path, 'r')]
        logging.debug(car_brands)

        logging.info(string)

        brand = ""

        for car_brand in car_brands:
            if car_brand.upper() in string:
                brand = car_brand
                break

        logging.info("brand = " + brand)

        if not brand:
            logging.critical("Brand not found")
            return "Not Found"

        return brand

    def get_appraisal_value(self):
        elements = self.tree.xpath('//*[@class="info-content"]//p')
        for element in elements:
            text = element.text
            if "Valor de avaliação:" in text:
                appraisal_value = text.split(": ")[1]
                appraisal_value = self.__remove_escapes(appraisal_value)
                logging.info("appraisal_value = " + appraisal_value)
                return appraisal_value

    def get_year(self):
        page_text = ''.join(self.tree.itertext())
        page_text = page_text.lower()
        m = re.search(r'ano.+?([0-9]\/|[0-9]+)', page_text)
        try:
            year = m.group(0)
        except AttributeError:
            logging.critical("Regex not found")
            # exit()
            return "Not found"

        year = year.replace("ano", "")
        year = year.replace("modelo", "")
        year = year.replace("/", "")
        year = year.replace(":", "")
        year = year.replace(" ", "")

        return year
