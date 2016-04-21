
class TheAuctionMill():
    """ Module for the http://www.theauctionmill.com site """
    def __init__(self, auction_helper):
        self.base_url = "http://www.theauctionmill.com"
        self.url = "http://www.theauctionmill.com/upcoming-auctions/"
        self.AuctionHelper = auction_helper

    def process_page(self, soup):
        print "Processing {}".format(self.url)
        auctions = []

        # Step 1: Get the containing div for the auctions

        container = soup.find("div", {"id": "acListWrap"})

        # Step 2: Get all of the divs for the auctions
        auction_divs = container.find_all("div", {"class": "auctionList"})

        for auction in auction_divs:
            auction_data = auction.find("div", {"class": "auctionListingMiddle"})

            auction_title = auction.find("a").text

            _list_subtitle = auction_data.find("div", {"id": "listSubtitle"})
            description = _list_subtitle.text
            more_info_link = self.base_url + _list_subtitle.find("a").get("href")


            print ""
            print "Title: {}".format(auction_title)
            print "Type: {}".format(auction_type)
            print "More info link: {}".format(more_info_link)
            print "Description: {}".format(description)
            print "Location: {}".format(location)
            print "Auction Location: {}".format(auction_location)
            print "Auction Time: {}".format(auction_time)
            print ""

            struct = {
                "title": auction_title,
                "type": auction_type,
                "more_info_link": more_info_link,
                "description": description,
                "location": location,
                "auction_location": auction_location,
                "auction_time": auction_time
            }
            # Convert all the values away from unicode
            struct = {k: str(v) for k,v in struct.iteritems()}

            auctions.append(struct)




        print "Finished processing auctions for {}".format(self.base_url)
        return auctions
