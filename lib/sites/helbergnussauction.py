
class HelbergNussAuction():
    """ Module for the http://www.helbergnussauction.com site """
    def __init__(self, auction_helper):
        self.base_url = "http://www.helbergnussauction.com"
        self.url = "http://www.helbergnussauction.com/auctions.php"
        self.AuctionHelper = auction_helper
        self.require_js = False

    def chunks(self, l, n):
        """Yield successive n-sized chunks from l."""
        for i in range(0, len(l), n):
            yield l[i:i+n]

    def get_direct_link_soup(self, link):
        """ Takes a link and returns a processed soup """
        soup = self.AuctionHelper.get_direct_link_soup(link)
        return soup

    def determine_auction_type(self, text):
        """ Given a block of text, returns a string of aution type """
        auction_type = self.AuctionHelper.determine_auction_type(text)
        return auction_type

    def process_page(self, soup):
        print "Processing {}".format(self.url)
        auctions = []

        container = soup.find("div", {"id": "html1"})
        print "__________"
        container = container.find("table")

        auction_rows = container.find_all("font")

        for auction in self.chunks(auction_rows, 3):


            auction_text = [str(x.text) for x in auction]
            auction_title = auction_text[0]
            auction_begin_time = auction_text[1]
            auction_location = auction_text[2]

            description = auction_title
            auction_end_time = "Unknown"

            more_info_link = "{}/{}".format(self.base_url, auction[0].find("a").get("href"))

            _direct_info = self.get_direct_link_soup(more_info_link)

            auction_type = self.AuctionHelper.determine_auction_type(_direct_info.text)

            print ""
            print "Title: {}".format(auction_title)
            print "Type: {}".format(auction_type)
            print "More info link: {}".format(more_info_link)
            print "Description: {}".format(description)
            print "Auction Location: {}".format(auction_location)
            print "Auction Begin Time: {}".format(auction_begin_time)
            print "Auction End Time: {}".format(auction_end_time)
            print ""

            struct = {
                "title": auction_title,
                "type": auction_type,
                "more_info_link": more_info_link,
                "description": description,
                "auction_location": auction_location,
                "auction_begin_time": auction_begin_time,
                "auction_end_time": auction_end_time,
            }
            # Convert all the values away from unicode
            struct = {k: str(v) for k,v in struct.iteritems()}

            auctions.append(struct)

        print "Finished processing auctions for {}".format(self.base_url)
        return auctions
