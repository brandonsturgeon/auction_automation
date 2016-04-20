from bs4 import BeautifulSoup
import logging

logger = logging.getLogger(__name__)
class Agriaffiliates():
    def __init__(self):
        self.base_url = "http://www.agriaffiliates.com/"
        self.url = "http://www.agriaffiliates.com/properties.php?Type=Auction"
        self.main()

    def process_page(self, page):
        soup = BeautifulSoup(pagedata)
        auctions = []

        # Step 1: Get all of the font elements
        font_elements = soup.find_all("font")

        # Step 2: Get the 3rd parent of each font object where object.text == "NEW"
        new_auctions = [x.parent.parent.parent for x in font_elements if x.text == "NEW"]

        # Step 3: Parse the information out of the HTML and into the auctions list
        for auction in new_auctions:
            auction_data = auction.find("td", {"class":"propRight"})

            auction_title = auction_data.find("a").text
            more_info_link = self.base_url + auction_data.find("a").get("href")

            # Dirty text parsing
            _desc = auction_data.text.split("NEW")[1]
            description = _desc.split("\r\n")
