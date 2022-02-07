from bson import Decimal128, ObjectId

from decimal import Decimal
from models.Article import Article


class ArticleInBillDto:
    def __init__(self, article_code, quantity=1, purchasePrice=None):
        if article_code is None or not isinstance(article_code, int):
            raise TypeError('Invalid argument: article')
        if purchasePrice is not None and not isinstance(purchasePrice, Decimal):
            raise TypeError('Invalid argument: purchasePrice')
        if not isinstance(quantity, int) and not isinstance(quantity, Decimal):
            raise TypeError('Invalid argument: quantity, actual instance: ')

        self.article_id = article_code
        self.purchasePrice = purchasePrice
        self.quantity = quantity

