class LocatorMainPage(object):
    # Main page
    BTN_CARROS_XPATH = '//*[@id="cat-2"]'


class LocatorAuctionPage(object):
    # Auction Page
    BTNS_AUCTION_DETAILS_XPATH = '//*[@class="btn-detail"]'
    BTN_NEXT_PAGE_XPATH = "//a[@rel='next']"


class LocatorLotPage(object):
    # LotPage

    MINIMAL_INCREMENT_XPATH = '//*[@id="inc0"]'
    ACTUAL_BID_XPATH = '//*[@id="lance0"]'
    LOT_STATUS_XPATH = '//*[@id="status0"]'
    OPENING_DATE_XPATH = '//*[@class="fa fa-hourglass-start"]//following-sibling::time'
    ENDING_DATE_XPATH = '//*[@id="endDate0"]'

    CAR_TITLE_XPATH = '//*[@id="desc0"]'
