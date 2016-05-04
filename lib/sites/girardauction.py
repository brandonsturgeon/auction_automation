
class GirardAuction():
    """ Module for the http://www.girardauction.com site """
    def __init__(self, auction_helper):
        self.base_url = "http://www.girardauction.com"
        self.url = "http://www.girardauction.com/"
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

    def get_auction_time(self, description):
        """ Takes a string and attempts to return an auction time """
        # Gets rid of the Bidding Now alert
        _a = description.replace("Bidding now open!", "")

        # We do these 2 steps because some of the auctions say
        # "Located" and some of them say "Location" so we split
        # by both just in case
        _b = _a.split("Located:")[0]
        _c = _b.split("Location:")[0]
        return _c

    def process_page(self, soup):
        print "Processing {}".format(self.url)
        auctions = []

        auction_area = soup.find("td", {"class": "wsite-multicol-col"})

        # NOTE: these should be the same length always, this will cause isues if they're somehow not
        titles = auction_area.find_all("h2", {"class": "wsite-content-title"})
        contents = auction_area.find_all("div", {"class": "paragraph"})


        for auction_num in range(len(titles)):
            print "----------------------------------------"
            print auction_num
            _title = titles[auction_num]
            _content = contents[auction_num]

            auction_title = self.clean_up(_title.text)
            description = self.clean_up(_content.text)

            _title_link = _title.find("a")

            # Some auctions don't have a more info link
            if _title_link:
                _more_info_link = _title_link.get("href")
                # Sometimes they link offiste to girardbid, in which case
                # they use a full path
                if "girardbid" in _more_info_link:
                    more_info_link = _more_info_link
                else:
                    more_info_link = self.base_url + _more_info_link
            else:
                more_info_link = "No additional information link provided"


            auction_time = self.get_auction_time(description)
            # After we separated the auction_time, get rid of the auction_time from the description
            description = description.replace(auction_time, "").replace("Bidding now open!", "")

            print ""
            print "Title: {}".format(auction_title)
            #print "Type: {}".format(auction_type)
            print "More info link: {}".format(more_info_link)
            print "Description: {}".format(description)
            #print "Auction Location: {}".format(auction_location)
            print "Auction Time: {}".format(auction_time)
            print ""

            struct = {
                "title": auction_title,
            #    "type": auction_type,
                "more_info_link": more_info_link,
                "description": description,
            #    "auction_location": auction_location,
                "auction_time": auction_time,
            #    "auction_end_time": auction_end_time,
            }
            ## Convert all the values away from unicode
            struct = {k: str(v) for k,v in struct.iteritems()}

            auctions.append(struct)

            print "----------------------------------------"

        print "Finished processing auctions for {}".format(self.base_url)
        return auctions
