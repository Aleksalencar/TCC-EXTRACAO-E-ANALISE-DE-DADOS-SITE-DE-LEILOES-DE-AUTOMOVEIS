import json
import csv
from PageObject.Pages import LutMainPage
from PageObject.Pages import LutAuctionPage
from PageObject.Pages import LutLotPage
import time

start = time.time()
main_page = LutMainPage.MainPage()
auction_page_href = main_page.get_btn_cars_href()

# auction_page_href = 'https://www.lut.com.br/todos-leiloes-online/0/1/2'
base_url = 'https://www.lut.com.br/'
auction_page_href = '/todos-leiloes-online/0/2/3'

csv_file = "Names.csv"
csv_columns = ['url', 'site_lot_id', 'actual_bid', 'opening_date', 'ending_date', 'minimal_increment', 'lot_status',
               'brand', 'model', 'year', 'appraisal_value', 'location']

with open(csv_file, 'a', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
    writer.writeheader()
# Pass trough the pages
lot_list_links = []
while auction_page_href:
    auction_page_url = base_url + auction_page_href
    auction_page = LutAuctionPage.AuctionPage(auction_page_url)
    lot_list_links = auction_page.get_lot_href_list()  # Merge lists

    for lot_link in lot_list_links:
        print(lot_link)
        if 'motocicleta' in lot_link or 'veiculo' in lot_link:
            print('deu bom')
            pass
        else:
            continue

        lut_page = LutLotPage.LotPage(base_url + lot_link)
        try:
            lot_info = lut_page.get_lot_info()
            car_info = lut_page.get_car_info()
        except:
            continue
        lot_info.update(car_info)
        print(json.dumps(lot_info, indent=4))
        with open(csv_file, 'a', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writerow(lot_info)
    auction_page_href = auction_page.get_next_page_href()





print('found total', len(lot_list_links))
not_year = []






print(len(lot_list_links))
end = time.time()
# total time taken
print(f"Runtime of the program is {end - start}")
