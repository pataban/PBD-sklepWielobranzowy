from bson import Decimal128, ObjectId

from models.Article import Article


def toMongoDictionary(article):
    dict = vars(article).copy()
    if 'actualPrice' in dict:
        dict.update({'actualPrice': Decimal128(dict.get('actualPrice'))})
    if 'id' in dict:
        dict.update({'_id': ObjectId(article.id)})
        dict.pop('id')
    return dict


def toPythonObject(mongoDictionary):
    return Article(
        mongoDictionary["code"],
        mongoDictionary["name"],
        Decimal128.to_decimal(mongoDictionary["actualPrice"]),
        mongoDictionary["_id"]
    )


class ArticleRepository:
    def __init__(self, articlesMongoHandler):
        self._articles_handler = articlesMongoHandler

    def find(self) -> [Article]:
        articles_objects = []
        for article_dict in self._articles_handler.find():
            articles_objects.append(toPythonObject(article_dict))
        return articles_objects

    def findById(self, article_id) -> Article:
        print("founding by id: " + str(ObjectId(article_id)))
        article_dict = self._articles_handler.find_one({'_id': ObjectId(article_id)})
        return toPythonObject(article_dict)

    def insert(self, newArticle: Article) -> bool:
        if newArticle is None:
            raise TypeError('Argument Article cannot be None')
        if not isinstance(newArticle, Article):
            raise TypeError('Argument newArticle must be of type Article')
        if newArticle.id is not None:
            raise ValueError('New article cannot have assigned id')
        inserted_id = (self._articles_handler.insert_one(toMongoDictionary(newArticle))).inserted_id
        newArticle.id = inserted_id  # inserting new article will automatically fill id field by new _id in db
        return True

    def update(self, updatedArticle: Article):
        updated_article_dict = toMongoDictionary(updatedArticle)
        self._articles_handler.update_one({
            '_id': ObjectId(updated_article_dict.get('_id'))
        }, {
            '$set': updated_article_dict
        })
        return None

    def removeArticleById(self, id):
        return None
