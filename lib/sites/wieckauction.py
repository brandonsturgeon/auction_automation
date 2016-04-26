
class WieckAuction():
    """ Module for the http://www.wieckauction.com site """
    def __init__(self, auction_helper):
        self.base_url = "http://www.wieckauction.com"
        self.url = "http://www.wieckauction.com/auctions/"
        self.AuctionHelper = auction_helper

    def determine_auction_type(self, text):
        return self.AuctionHelper.determine_auction_type(text)

    def get_direct_link_soup(self, link):
        """ Takes a link and returns a processed soup """
        soup = self.AuctionHelper.get_direct_link_soup(link)
        return soup

    def clean_up(self, text):
        """ Takes a string and encodes it to utf-8, gets rid of excess spaces/tabs """
        return " ".join(text.encode("utf-8").strip().split())

    def process_page(self, soup):
        print "Processing {}".format(self.url)
        auctions = []

        auction_cards = soup.find("ul", {"class": "cards"}).find_all("li", recursive=False)

        for auction in auction_cards:
            print "----------------------------------------"

            more_info_link = auction.find("a").get("href")

            # Title and Description
            _details = auction.find("div", {"class": "auction-details"})
            auction_title = self.clean_up(_details.find("h5").text)
            description = self.clean_up(_details.find("h6").text)

            # Time and location
            auction_time = self.clean_up(_details.find("span", {"class": "date"}).text)
            auction_location = self.clean_up(_details.find("span", {"class": "location"}).text)


            # Find the type of auction
            _soup = self.get_direct_link_soup(more_info_link)
            _info_block = self.clean_up(_soup.find("div", {"id": "editable"}).text)
            auction_type = self.determine_auction_type(_info_block)

            print ""
            print "Title: {}".format(auction_title)
            print "Type: {}".format(auction_type)
            print "More info link: {}".format(more_info_link)
            print "Description: {}".format(description)
            print "Auction Location: {}".format(auction_location)
            print "Auction Time: {}".format(auction_time)
            print ""

            struct = {
                "title": auction_title,
                "type": auction_type,
                "more_info_link": more_info_link,
                "description": description,
                "auction_location": auction_location,
                "auction_time": auction_time,
            }
            # Convert all the values away from unicode
            struct = {k: str(v) for k,v in struct.iteritems()}

            auctions.append(struct)

            print "----------------------------------------"

        print "Finished processing auctions for {}".format(self.base_url)
        return auctions
