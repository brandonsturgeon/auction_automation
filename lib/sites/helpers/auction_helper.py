
class AuctionHelper():
    """ A set of helper functions to be used across each site module """
    def __init__(self):

        real_estate_terms = (
            "real estate",
            "realestate",
            "irrigated",
            "nonirrigated",
            "non irrigated",
            "non-irrigated"
        )
        self.auction_types = {
            "Real Estate": real_estate_terms,
        }

    def determine_auction_type(self, text):
        scores = {}

        for auction_type, terms in self.auction_types.iteritems():
            count = 0
            for term in terms:
                if term in text:
                    count += 1
            scores[auction_type] = count

        types = list(scores.keys())
        values = list(scores.values())
        highest = types[values.index(max(values))]
        print "Determined auction type to be: {}".format(highest)

        print "Debug: Auction Type scores"
        print ""
        print scores
        print ""

        if scores[highest] == 0:
            return "Unknown"
        return highest
