from bs4 import BeautifulSoup
import requests

# Site Imports
from lib.sites.agriaffiliates import Agriaffiliates

class Main():
    def __init__(self):
        self.sites = {Agriaffiliates}
        pass

    def process_sites(self):
        for site in self.sites:
            page = requests.get(site.url).text
            processed_data = site.process_page(page)


if __name__ == "__main__":
    Main()

