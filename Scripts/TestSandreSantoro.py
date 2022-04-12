import unittest

from Scripts.sodreSantoro import Sandre


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.sandre = Sandre()

    def test_get_name(self):
        test_cases = [
            {
                'url': "https://www.sodresantoro.com.br/leilao/22245/lote/2261974/segmento/veiculos/ordenacao/data_leilao/tipo-ordenacao/crescente/qtde-itens/30/visualizacao/visual_imagemlista/item-atual/1/pagina/2/",
                'name': "Leilão 22245 - 0055 - CHEVROLET S10 LT 20/21"

            },
            {
                'url': "https://www.sodresantoro.com.br/leilao/22245/lote/2261964/segmento/veiculos/ordenacao/data_leilao/tipo-ordenacao/crescente/qtde-itens/30/visualizacao/visual_imagemlista/item-atual/1/pagina/3/",
                'name': "Leilão 22245 - 0070 - BLINDADO BMW X6 XDRIVE 35I FG21 10/11"

            },
        ]
        for case in test_cases:
            auction_page = self.sandre.parse_auction(case['url'])
            result = self.sandre.get_name(auction_page)
            self.assertEqual(result, case['name'])


if __name__ == '__main__':
    unittest.main()
