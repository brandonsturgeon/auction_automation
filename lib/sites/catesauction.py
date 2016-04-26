
class CatesAuction():
    """ Module for the http://www.catesaucton.com site """
    def __init__(self, auction_helper):
        self.base_url = "http://www.catesauction.com"
        self.url = "http://www.catesauction.com/auctions/all-auctions/"
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

        # Step 1: Get the containing div for the auctions

        container = soup.find("div", {"id": "acListWrap"})

        # Step 2: Get all of the divs for the auctions
        auction_divs = container.find_all("div", {"class": "auctionList"})

        for auction in auction_divs:
            print "----------------------------------------"
            auction_data = auction.find("div", {"class": "auctionListingMiddle"})

            _dirty_auction_title = auction.find("h1", {"id": "auction_title"}).text
            auction_title = self.clean_up(_dirty_auction_title)

            _more_info_link = auction_data.find("a", {"class": "details-button list-deets"}).get("href")
            more_info_link = self.base_url + _more_info_link

            description = self.clean_up(auction_data.find("a").text)

            auction_location = self.clean_up(auction.find("div", {"class": "auctionListingLeft"}).text)

            auction_time = self.clean_up(auction_data.find("div").text)


            sub_description = self.clean_up(auction_data.find("div", {"style": "font:14px/17px 'pt sans';color:#555;margin-top:20px"}).text)

            # Determine Auction Type -- Title + Description + Subdescription
            _combined_text = " ".join({auction_title, description, sub_description})
            auction_type = self.AuctionHelper.determine_auction_type(_combined_text)

            print ""
            print "Title: {}".format(auction_title)
            print "Type: {}".format(auction_type)
            print "More info link: {}".format(more_info_link)
            print "Description: {}".format(description)
            print "Sub Description: {}".format(sub_description)
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
