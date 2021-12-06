from bson import Decimal128, ObjectId

from models.Article import Article


def toMongoDictionary(article):
    article_dict = vars(article).copy()
    if 'actualPrice' in article_dict:
        article_dict.update({'actualPrice': Decimal128(article_dict['actualPrice'])})
    if 'id' in article_dict:
        article_dict.update({'_id': ObjectId(article.id)})
        article_dict.pop('id')
    return article_dict


def toPythonObject(article_mongo_dict):
    return Article(
        article_mongo_dict["code"],
        article_mongo_dict["name"],
        Decimal128.to_decimal(article_mongo_dict["actualPrice"]),
        str(article_mongo_dict["_id"])
    )


class ArticleRepository:
    def __init__(self, articlesMongoHandler):
        self._articles_handler = articlesMongoHandler

    def find(self) -> [Article]:
        article_objects = []
        for article_mongo_dict in self._articles_handler.find():
            article_objects.append(toPythonObject(article_mongo_dict))
        return article_objects

    def findById(self, article_id) -> Article:
        article_mongo_dict = self._articles_handler.find_one({'_id': ObjectId(article_id)})
        if article_mongo_dict is None:
            return None
        return toPythonObject(article_mongo_dict)

    def insert(self, newArticle: Article) -> bool:
        if newArticle is None:
            raise TypeError('Argument newArticle cannot be None')
        if not isinstance(newArticle, Article):
            raise TypeError('Argument newArticle must be of type Article')
        if newArticle.id is not None:
            raise ValueError('New article cannot have assigned id')
        insert_one_result = self._articles_handler.insert_one(toMongoDictionary(newArticle))
        inserted_id = insert_one_result.inserted_id
        if inserted_id is None:
            return False
        newArticle.id = str(inserted_id)  # inserting new article will automatically fill id field by new _id in db
        return True

    def update(self, updatedArticle: Article) -> bool:
        if updatedArticle is None or not isinstance(updatedArticle, Article):
            raise TypeError('Invalid argument: updatedArticle')
        updated_article_dict = toMongoDictionary(updatedArticle)
        update_result = self._articles_handler.update_one({
            '_id': ObjectId(updated_article_dict['_id'])
        }, {
            '$set': updated_article_dict
        })
        return update_result.matched_count() == 1

    def remove(self, existingArticle: Article) -> bool:
        if existingArticle is None or not isinstance(existingArticle, Article):
            raise TypeError('Invalid argument: existingArticle')
        existing_article_dict = toMongoDictionary(existingArticle)
        delete_result = self._articles_handler.delete_one(
            existing_article_dict
        )
        deleted_count = delete_result.deleted_count
        if deleted_count < 1:
            return False
        existingArticle.id = None
        return True
