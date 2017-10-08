"""MongoDB """

from pymongo import MongoClient

class OmadaDB(object):
    """Class docstring"""

    db_uri = "mongodb://{user}:{pass}@ds040877.mlab.com:40877/omada_db"

    def __init__(self, config: dict):
        uri = self.db_uri.format(**config)

        self.client = MongoClient(uri)
        self.db = self.client.get_default_database()

        # Set collections.
        self.users = self.db.Users
        self.group = self.db.Groups.find_one()  # Get first group.
        self.stocks = self.db.Stocks


    def add_user(self, data: dict):
        """Add user to database."""

        self.users.insert_one(data)


    def find_user(self, user: str):
        """Return user information from users collection"""

        return self.users.find_one({"username": user})


    def get_stocks(self, stock_id: str):
        """Return unique stock instance information."""

        return self.stocks.find_one({"id": stock_id})


    def update_stocks(self, stock_id, params):
        """Update stock instance with new params"""
        
        return self.stocks.find_one_and_update({"id": int(stock_id)}, params)


    def vote(self, stock_id, buy, approve):
        """Adds vote to stock_id for approve or not approve to buy or sell"""

        vote_str = 'buy' if buy == "1" else 'sell'
        vote_str += '_votes_'
        vote_str += 'for' if approve=="1" else 'against'
        return vote_str
        return str(self.update_stocks(stock_id, {'$inc': {vote_str: 1}}))


    def vote_count(self, stock_id):
        """Returns array of [buy_votes_for, buy_votes_against, sell_votes_for, sell_votes_against]"""

        self.vote("1","1","1")
        stock = self.get_stocks(stock_id)
        # return vars(stock)
        return 1