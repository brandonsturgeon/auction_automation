
class PurpleWave():
    """ Module for the http://www.purplewave.com site """
    def __init__(self, auction_helper):
        self.base_url = "https://www.purplewave.com"
        self.url = "https://www.purplewave.com"
        self.AuctionHelper = auction_helper
        self.require_js = True

    def clean_up(self, text):
        """ Takes a string and encodes it to utf-8, gets rid of excess spaces/tabs """
        return " ".join(text.encode("utf-8").strip().split())

    def process_page(self, soup):
        print "Processing {}".format(self.url)
        auctions = []

        upcoming_auctions = soup.find("div", {"id": "auction-event-list"}).find_all("div", recursive=False)

        for auction in upcoming_auctions:
            # Ignore the auction if it's closed
            closed = auction.find("span", {"class": "text-red"})
            if closed:
                continue

            print "----------------------------------------"

            auction_date = self.clean_up(auction.find("span", {"class": ""}).text)

            _auction_title = auction.find("p", {"class": "auction-title"})
            auction_title = self.clean_up(_auction_title.text)
            more_info_link = self.base_url + _auction_title.find("a").get("href")

            # Very Flaky
            _auction_time = auction.find("div", {"class": "col-xs-12 col-md-5 auction-date"})
            auction_time = self.clean_up(_auction_time.text)

            # DEFAULTS
            auction_location = "Online Only"

            print ""
            print "Title: {}".format(auction_title)
            print "More info link: {}".format(more_info_link)
            #print "Description: {}".format(description)
            print "Auction Location: {}".format(auction_location)
            print "Auction Time: {}".format(auction_time)
            print "Auction Date: {}".format(auction_date)
            print ""

            struct = {
                "title": auction_title,
                "more_info_link": more_info_link,
            #    "description": description,
                "auction_location": auction_location,
                "auction_date": auction_date,
                "auction_time": auction_time,
            }
            # Convert all the values away from unicode
            struct = {k: str(v) for k,v in struct.iteritems()}

            auctions.append(struct)

            print "----------------------------------------"

        print "Finished processing auctions for {}".format(self.base_url)
        return auctions
