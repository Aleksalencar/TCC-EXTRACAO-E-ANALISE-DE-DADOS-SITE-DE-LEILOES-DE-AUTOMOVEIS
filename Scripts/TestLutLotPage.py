import unittest
from typing import Union

from PageObject.Pages import LutLotPage
from PageObject.TestBase.logger_setup import LoggingConfig

logging = LoggingConfig()
logging = logging.get_logging()


class TestLutLotPage(unittest.TestCase):
    def test_get_lot_info_(self):
        test_case = {
            'test_case_name': "Opened case",
            'url': "https://www.lut.com.br/lote/veiculo-peugeot-hb/87589",
            'expeceted_result': {
                'site_lot_id': 87589,
                'actual_bid': "R$ 10.000,00",
                'opening_date': "25/10/2021",
                'ending_date': "28/10/2021 10:00:00",
                'lot_status': Union["Fechado", "Aberto", "Aguardando"]
            }
        }

        logging.info("running " + test_case['test_case_name'])
        lut_page = LutLotPage.LotPage(test_case['url'])
        result = lut_page.get_lot_info()
        self.assertEqual(result, test_case['expeceted_result'])

    def test_get_car_info_(self):
        test_case = {
            'test_case_name': "Opened case",
            'url': "https://www.lut.com.br/lote/veiculo-peugeot-hb/87589",
            'expeceted_result': {
                'site_lot_id': 87589,
                'actual_bid': "R$ 10.000,00",
                'opening_date': "25/10/2021",
                'ending_date': "28/10/2021 10:00:00",
                'lot_status': "Fechado"
            }
        }

        logging.info("running " + test_case['test_case_name'])
        lut_page = LutLotPage.LotPage(test_case['url'])
        result = lut_page.get_lot_info()
        self.assertEqual(result, test_case['expeceted_result'])


if __name__ == '__main__':
    unittest.main()
