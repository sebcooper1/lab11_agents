# stock_tool.py
# Sebastian Cooper


class StockLookup:
    """A tool that knows how many of each item is in stock"""

    def __init__(self, stock):
        """Stores the stock this tool can look up."""
        self.stock = stock

    def find_product(self, text):
        """Return the stock of one item, or None if there is no such item."""
        for product in self.stock:
            if product in text.lower():
                return product
        return None

    def count_for(self, product):
        """Return how many of one product are in stock, or None if unknown."""
        if product in self.stock:
            return self.stock[product]
        return None
