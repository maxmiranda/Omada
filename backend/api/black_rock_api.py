"""BlackRock API"""

import requests

class BlackRock(object): 

    root_uri = "https://www.blackrock.com/tools/hackathon/"
    security_data_uri = root_uri + "security-data"
    search_securities_uri = root_uri + "search-securities"
    portfolio_analysis_uri = root_uri + "portfolio-analysis"
    perfomance_data_uri = root_uri + "performance"

    @classmethod
    def get_security_data(cls, *symbols):
        """Function docstring."""

        symbols = ",".join(symbols)
        res = requests.get(cls.security_data_uri, params={"identifiers": symbols})

        return res.json()


    @classmethod
    def get_portfolio_analysis(cls, positions: dict):
        """
        Args:
            positions (dict): in form of {{"sym": symbol, "ratio": 100}}
        """

        query = "|".join(["{sym}~{ratio}".format(**pos) for pos in positions])
        params = {"positions": query}
        res = requests.get(cls.portfolio_analysis_uri, params=params)

        return res.json()


    @classmethod
    def get_performance_data(cls, *symbols):
        """Function docstring."""

        symbols = ",".join(symbols)
        res = requests.get(cls.perfomance_data_uri, params={"identifiers": symbols})

        return res.json()


    @classmethod
    def search_securities(cls, *symbols):
        """Function docstring."""

        symbols = ",".join(symbols)
        res = requests.get(cls.search_securities_uri, params={"identifiers": symbols})

        return res.json()


    @classmethod
    def get_stock_performance_key_val(cls, symbol):
        stock = get_performance_data(symbol)
        info = stock["resultMap"]["RETURNS"][0]["returnsMap"]
        pairs = []
        currentPrice = 100
        for k,v in info.items():
            date = float(k)
            price = float(v["level"]) * currentPrice
            pairs.append([date, price])
        return pairs

