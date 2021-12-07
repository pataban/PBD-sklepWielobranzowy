from bson import Decimal128, ObjectId

from decimal import Decimal
from models.Article import Article


class ArticleInBill:  # should be used only for new articleInBill creation
    def __init__(self, article, quantity=1, purchasePrice=None):
        if article is None or not isinstance(article, Article):
            raise TypeError('Invalid argument: article')
        if purchasePrice is not None and not isinstance(purchasePrice, Decimal):
            raise TypeError('Invalid argument: purchasePrice')
        if not isinstance(quantity, int) and not isinstance(quantity, Decimal):
            raise TypeError('Invalid argument: quantity, actual instance: ')

        self.article = article
        if purchasePrice is None:
            self.purchasePrice = article.actualPrice
        else:
            self.purchasePrice = purchasePrice
        self.quantity = quantity

    def toMongoDictionary(self):
        article_in_bill_dict = vars(self).copy()
        if 'article' in article_in_bill_dict:
            article_in_bill_dict['article_id'] = ObjectId(self.article.id)
            article_in_bill_dict.pop('article')
        if 'quantity' in article_in_bill_dict and isinstance(self.quantity, Decimal):
            article_in_bill_dict.update({'quantity': Decimal128(self.quantity)})
        if 'purchasePrice' in article_in_bill_dict:
            article_in_bill_dict.update({'purchasePrice': Decimal128(self.purchasePrice)})
        return article_in_bill_dict
