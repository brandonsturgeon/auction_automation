from bs4 import BeautifulSoup
import pprint
import requests
import dryscrape

# Global vars
PP = pprint.PrettyPrinter(indent=4)

# Site Imports
from lib.sites.agriaffiliates import Agriaffiliates
from lib.sites.theauctionmill import TheAuctionMill
from lib.sites.helbergnussauction import HelbergNussAuction
from lib.sites.catesauction import CatesAuction
from lib.sites.wieckauction import WieckAuction
from lib.sites.purplewave import PurpleWave
from lib.sites.wiemanauction import WiemanAuction
from lib.sites.girardauction import GirardAuction

# Helper Imports
from lib.sites.helpers.auction_helper import AuctionHelper

class Main():
    def __init__(self):
        self.auction_helper = AuctionHelper()

        # Set of site modules
        self.sites = {
            Agriaffiliates,
            TheAuctionMill,
            HelbergNussAuction,
            CatesAuction,
            WieckAuction,
            PurpleWave,
            WiemanAuction,
            GirardAuction,
        }
        # Generate an instance of each module and
        # provide it with an instance of the helper class
        self.sites = [site(self.auction_helper) for site in self.sites]

        self.processed_auctions = {}

        self.process_sites()

    def process_sites(self):

        # Determine if a dryscrape session is required for a js-reliant site
        need_session = any([x.require_js for x in self.sites])
        if need_session:
            print "Dryscrape session required, creating now.."
            session = dryscrape.Session()
            print "Dryscrape session created"

        for site in self.sites:
            # If it requires JS, use dryscrape
            if site.require_js:
                session.visit(site.url)
                page = session.body()
            # Otherwise just use requests
            else:
                page = requests.get(site.url).text

            # Processing is done the same regardless
            soup = BeautifulSoup(page, "lxml")
            processed_data = site.process_page(soup)

            self.processed_auctions[site.base_url] = processed_data

        print ""
        print "Done processing sites"
        PP.pprint(self.processed_auctions)


if __name__ == "__main__":
    Main()
