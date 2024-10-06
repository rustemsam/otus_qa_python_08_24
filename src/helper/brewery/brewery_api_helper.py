class BreweryApiHelper:
    BREWERY_API_URL = "https://api.openbrewerydb.org/v1/breweries"

    def get_single_brewery(self, brewery_id):
        return f"{self.BREWERY_API_URL}/{brewery_id}"

    def get_list_all_breweries(self):
        return f"{self.BREWERY_API_URL}"

    def get_random_brewery(self):
        return f"{self.BREWERY_API_URL}/random"

    def get_brewery_meta(self):
        return f"{self.BREWERY_API_URL}/meta"
