import json

from PageObject.Pages import LutMainPage
from PageObject.Pages import LutAuctionPage
from PageObject.Pages import LutLotPage

main_page = LutMainPage.MainPage()
auction_page_href = main_page.get_btn_cars_href()

base_url = "https://www.lut.com.br"

# Pass trough the pages
lot_list_links = []
while auction_page_href:
    auction_page_url = base_url + auction_page_href
    auction_page = LutAuctionPage.AuctionPage(auction_page_url)
    lot_list_links = lot_list_links + auction_page.get_lot_href_list()  # Merge lists
    auction_page_href = auction_page.get_next_page_href()

not_year = []
for lot_link in lot_list_links:
    lut_page = LutLotPage.LotPage(base_url+lot_link)
    lot_info = lut_page.get_lot_info()
    car_info = lut_page.get_car_info()
    if car_info['year'] == "Not found":
        not_year.append(lot_info['url'])

    lot_info.update(car_info)
    print(json.dumps(lot_info, indent=4))
print(not_year)
