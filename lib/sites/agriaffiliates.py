
class Agriaffiliates():
    """ Module for the http://www.agriaffiliates.com site """
    def __init__(self, auction_helper):
        self.base_url = "http://www.agriaffiliates.com/"
        self.url = "http://www.agriaffiliates.com/properties.php?Type=Auction"
        self.AuctionHelper = auction_helper

    def process_page(self, soup):
        print "Processing {}".format(self.url)
        auctions = []

        # Step 1: Get all of the font elements
        font_elements = soup.find_all("font")

        # Step 2: Get the 3rd parent of each font object where object.text == "NEW"
        new_auctions = [x.parent.parent.parent for x in font_elements if x.text == "NEW"]

        # Step 3: Parse the information out of the HTML and into the auctions list
        for auction in new_auctions:
            auction_data = auction.find("td", {"class":"propRight"})

            auction_title = auction_data.find("a").text
            more_info_link = self.base_url + auction_data.find("a").get("href")
            # For easy url usage
            more_info_link = more_info_link.replace(" ", "%20")

            _desc = auction_data.text.split("NEW")[1]
            description = _desc.split("\r\n")[0]

            # This is the location of the actual land
            location = description.split(" in ")[-1]

            # This is where/when the auction will be held
            _date_time = _desc.split("\r\n")[-1]
            _date_time = _date_time.replace("Offered at public auction ", "")
            _date_time = _date_time.split(", ")

            auction_location = ", ".join(_date_time[-2:])
            auction_time = ", ".join(_date_time[:3])

            # Find the type of auction
            auction_type = self.AuctionHelper.determine_auction_type(auction_data.text)

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
