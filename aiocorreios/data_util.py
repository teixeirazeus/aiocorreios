from decimal import Decimal

class DataUtil:
    @staticmethod
    def to_decimal(data):
        """
        Parse the data to decimal.
        """
        return Decimal(data.replace(',', '.'))