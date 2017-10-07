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

        return self.users.find_one({"user": user})


    def get_stocks(self, stock_id: str):
        """Return unique stock instance information."""

        return self.stocks.find_one({"id": stock_id})
