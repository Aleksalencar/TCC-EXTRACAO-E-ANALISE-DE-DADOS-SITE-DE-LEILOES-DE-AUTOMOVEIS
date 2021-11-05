from datetime import datetime, date

import requests
from lxml import html

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

        # Parse main LotPage
        # page = requests.get(self.url, )
        # self.tree = html.fromstring(page.content)

        # Parse main page
        page = requests.get(self.url)
        self.tree = html.fromstring(page.content)

        pass

    def get_lot_info(self):
        site_lot_id = self.url.split("/")[-1]
        site_lot_id = int(site_lot_id)

        actual_bid = self.tree.xpath(Locator.ACTUAL_BID_XPATH)[0].text

        opening_date = self.tree.xpath(Locator.OPENING_DATE_XPATH)[0].text
        opening_date = self.__remove_escape(opening_date)

        ending_date = self.tree.xpath(Locator.ENDING_DATE_XPATH)[0].text
        ending_date = self.__remove_escape(ending_date)

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
            'site_lot_id': site_lot_id,
            'actual_bid': actual_bid,
            'opening_date': opening_date,
            'ending_date': ending_date,
            'lot_status': lot_stats
        }

        logging.info('info = ' + str(info))

        return info

    @staticmethod
    def __remove_escape(string):
        string = string.replace("\t", "")
        string = string.replace("\r", "")
        string = string.replace("\n", "")
        string = string.strip()
        return string
