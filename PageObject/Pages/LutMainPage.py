import requests
from lxml import html
from PageObject.Pages.Locators import LocatorMainPage as Locator

from PageObject.TestBase.logger_setup import LoggingConfig

logging = LoggingConfig()
logging = logging.get_logging()


class MainPage:
    def __init__(self):
        self.url = "https://www.lut.com.br"

        # Parse main page
        page = requests.get(self.url)
        self.tree = html.fromstring(page.content)

    def get_btn_cars_href(self) -> str:
        logging.info("[def] get_btn_cars_href")
        cars_href = self.__get_button_href(Locator.BTN_CARROS_XPATH)
        return cars_href

    # private
    def __get_button_href(self, xpath):
        btn = self.tree.xpath(xpath)[0]
        btn = btn.attrib
        logging.info(btn['data-href'])
        btn_href = btn['data-href']

        return btn_href

