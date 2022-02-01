from typing import Optional

import pymongo
from bson import ObjectId
import sqlalchemy as sqla

from models.Article import Article
from dbConnectivity.MysqlConnector import *

class ArticleRepository:
    def __init__(self, articlesHandler):
        self._articles_handler = articlesHandler

    def find(self) -> [Article]:
        session=sqla.orm.sessionmaker(bind=self._articles_handler)()
        article_objects = []
        for article_orm in session.query(ArticleORM).all():
            article_objects.append(Article.fromORM(article_orm))
        session.close()
        return article_objects

    def findById(self, article_id) -> Optional[Article]:
        session=sqla.orm.sessionmaker(bind=self._articles_handler)()
        article_orm = session.query(ArticleORM).filter_by(id=article_id).one()
        session.close()
        if article_orm is None:
            return None
        return Article.fromORM(article_orm)

    def findByCode(self, code: int) -> Optional[Article]:
        session=sqla.orm.sessionmaker(bind=self._articles_handler)()
        article_orm = session.query(ArticleORM).filter_by(code=code).one()
        session.close()
        if article_orm is None:
            return None
        return Article.fromORM(article_orm)

    def insert(self, newArticle: Article) -> bool:
        if newArticle is None:
            raise TypeError('Argument newArticle cannot be None')
        if not isinstance(newArticle, Article):
            raise TypeError('Argument newArticle must be of type Article')
        if newArticle.id is not None:
            raise ValueError('New article cannot have assigned id')
        session=sqla.orm.sessionmaker(bind=self._articles_handler)()
        articleOrm=newArticle.toORM()
        session.add(articleOrm)
        inserted_id = articleOrm.inserted_id
        session.commit()
        session.close()
        if inserted_id is None:
            return False
        newArticle.id = str(inserted_id)  # inserting new article will automatically fill id field by new _id in db
        return True

    def update(self, updatedArticle: Article) -> bool:
        if updatedArticle is None or not isinstance(updatedArticle, Article):
            raise TypeError('Invalid argument: updatedArticle')
        session=sqla.orm.sessionmaker(bind=self._articles_handler)()
        updated_article_orm = updatedArticle.toORM()
        article_orm = session.query(ArticleORM).filter_by(id=updated_article_orm.id)
        update_result=article_orm.count()
        if(update_result==1):
            article_orm=article_orm.one()
            article_orm.update(updated_article_orm)
        session.commit()
        session.close()
        return update_result.matched_count == 1

    def remove(self, article_id: str) -> bool:
        session=sqla.orm.sessionmaker(bind=self._articles_handler)()
        delete_result = session.query(ArticleORM).filter_by(id=article_id)
        delete_count = delete_result.count()
        if(delete_count>0):
            session.delete(delete_result.all())
        session.commit()
        session.close()
        return delete_count >= 1

    def maxArticleCode(self) -> int:
        session=sqla.orm.sessionmaker(bind=self._articles_handler)()
        for result in  session.query(ArticleORM).order_by(ArticleORM.code.desc()).all(): 
            if result.code is not None:
                session.close()
                return result['code']
        session.close()
        return -1
