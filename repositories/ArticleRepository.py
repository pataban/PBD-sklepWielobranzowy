from typing import Optional

import pymongo
from bson import ObjectId

from models.Article import Article


class ArticleRepository:
    def __init__(self, articlesMongoHandler):
        self._articles_handler = articlesMongoHandler

    def find(self) -> [Article]:
        article_objects = []
        for article_mongo_dict in self._articles_handler.find():
            article_objects.append(Article.fromMongoDictionary(article_mongo_dict))
        return article_objects

    def findById(self, article_id) -> Optional[Article]:
        article_mongo_dict = self._articles_handler.find_one({'_id': ObjectId(article_id)})
        if article_mongo_dict is None:
            return None
        return Article.fromMongoDictionary(article_mongo_dict)

    def findByCode(self, code: int) -> Optional[Article]:
        article_mongo_dict = self._articles_handler.find_one({'code': code})
        if article_mongo_dict is None:
            return None
        return Article.fromMongoDictionary(article_mongo_dict)

    def insert(self, newArticle: Article) -> bool:
        if newArticle is None:
            raise TypeError('Argument newArticle cannot be None')
        if not isinstance(newArticle, Article):
            raise TypeError('Argument newArticle must be of type Article')
        if newArticle.id is not None:
            raise ValueError('New article cannot have assigned id')
        insert_one_result = self._articles_handler.insert_one(newArticle.toMongoDictionary())
        inserted_id = insert_one_result.inserted_id
        if inserted_id is None:
            return False
        newArticle.id = str(inserted_id)  # inserting new article will automatically fill id field by new _id in db
        return True

    def update(self, updatedArticle: Article) -> bool:
        if updatedArticle is None or not isinstance(updatedArticle, Article):
            raise TypeError('Invalid argument: updatedArticle')
        updated_article_dict = updatedArticle.toMongoDictionary()
        update_result = self._articles_handler.update_one({
            '_id': updated_article_dict['_id']
        }, {
            '$set': updated_article_dict
        })
        return update_result.matched_count == 1

    def remove(self, article_id: str) -> bool:
        delete_result = self._articles_handler.delete_one({
            '_id': ObjectId(article_id)
        })
        deleted_count = delete_result.deleted_count
        return deleted_count >= 1

    def maxArticleCode(self) -> int:
        for result in self._articles_handler.find().sort('code', pymongo.DESCENDING):
            if 'code' in result and result['code'] is not None:
                return result['code']
        return -1
