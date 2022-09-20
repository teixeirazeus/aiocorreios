from decimal import Decimal

class DataUtil:
    @staticmethod
    def to_decimal(data):
        return Decimal(data.replace(',', '.'))