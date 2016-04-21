import re

class TheAuctionMill():
    """ Module for the http://www.theauctionmill.com site """
    def __init__(self, auction_helper):
        self.base_url = "http://www.theauctionmill.com"
        self.url = "http://www.theauctionmill.com/upcoming-auctions/"
        self.AuctionHelper = auction_helper

    def determine_auction_type(self, text):
        return self.AuctionHelper.determine_auction_type(text)

    def get_location(self, text):
        """ Given the expected format of text, extracts the Location """
        try:
            location = re.search(r'Location: (.*) (?:Begins|Began):', text).group(1)
        except (AttributeError, IndexError) as e:
            location = "Unknown"
            print "Error! Unable to find Location with Regex"
            print text
            print e
        return location

    def get_begin_time(self, text):
        """ Given the expected format of text, extracts the Begin Time """
        try:
            auction_begin = re.search(r'(?:Begins|Began): (.*) (?:Ends:|$)', text).group(1)
        except (AttributeError, IndexError) as e:
            auction_begin = "Unknown"
            print "Error! Unable to find Begin Time with Regex"
            print text
            print e
        return auction_begin

    def get_end_time(self, text):
        """ Given the expected format of text, extracts the End Time (if present) """
        try:
            auction_end = re.search(r'Ends:(.*)$', text).group(1)
        except (AttributeError, IndexError) as e:
            auction_end = "Unknown"
            print "Error! Unable to find End Time with Regex"
            print text
            print e
        return auction_end

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

            # Gets title
            auction_title = auction.find("a").text

            # Gets description and more info link
            _list_subtitle = auction_data.find("h2", {"id": "listSubtitle"})
            description = _list_subtitle.text
            more_info_link = self.base_url + _list_subtitle.find("a").get("href")

            # Gets the time and location
            _location_div = auction_data.find("div", {"class": "acDetailEventLabel"})
            clean_location_time_data = " ".join(_location_div.text.split())

            auction_location = self.get_location(clean_location_time_data)
            auction_begin_time = self.get_begin_time(clean_location_time_data)
            auction_end_time = self.get_end_time(clean_location_time_data)


            # Find the type of auction
            auction_type = self.determine_auction_type(auction_data.text)

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

            print "----------------------------------------"

        print "Finished processing auctions for {}".format(self.base_url)
        return auctions
