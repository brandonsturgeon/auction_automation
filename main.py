from bs4 import BeautifulSoup
import pprint
import requests

# Global vars
PP = pprint.PrettyPrinter(indent=4)

# Site Imports
from lib.sites.agriaffiliates import Agriaffiliates
from lib.sites.theauctionmill import TheAuctionMill

# Helper Imports
from lib.sites.helpers.auction_helper import AuctionHelper

class Main():
    def __init__(self):
        self.auction_helper = AuctionHelper()

        # Set of site modules
        self.sites = {
            Agriaffiliates,
            TheAuctionMill
        }
        # Generate an instance of each module and
        # provide it with an instance of the helper class
        self.sites = [x(self.auction_helper) for x in self.sites]

        self.processed_auctions = {}

        self.process_sites()

    def process_sites(self):
        for site in self.sites:
            page = requests.get(site.url).text
            soup = BeautifulSoup(page, "lxml")
            processed_data = site.process_page(soup)

            self.processed_auctions[site.base_url] = processed_data

        print ""
        print "Done processing sites"
        PP.pprint(self.processed_auctions)


if __name__ == "__main__":
    Main()
