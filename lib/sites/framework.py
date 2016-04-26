
class BasicSite():
    """ Module for the http://www.BasicSite.com site """
    def __init__(self, auction_helper):
        self.base_url = ""
        self.url = ""
        self.AuctionHelper = auction_helper
        self.require_js = False

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

        for auction in enumerable:
            print "----------------------------------------"


            # Find the type of auction
            #auction_type = self.determine_auction_type(auction_data.text)

            #print ""
            #print "Title: {}".format(auction_title)
            #print "Type: {}".format(auction_type)
            #print "More info link: {}".format(more_info_link)
            #print "Description: {}".format(description)
            #print "Auction Location: {}".format(auction_location)
            #print "Auction Begin Time: {}".format(auction_begin_time)
            #print "Auction End Time: {}".format(auction_end_time)
            #print ""

            #struct = {
            #    "title": auction_title,
            #    "type": auction_type,
            #    "more_info_link": more_info_link,
            #    "description": description,
            #    "auction_location": auction_location,
            #    "auction_begin_time": auction_begin_time,
            #    "auction_end_time": auction_end_time,
            #}
            ## Convert all the values away from unicode
            #struct = {k: str(v) for k,v in struct.iteritems()}

            #auctions.append(struct)

            print "----------------------------------------"

        print "Finished processing auctions for {}".format(self.base_url)
        return auctions
