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
        article_result=session.query(ArticleORM).filter_by(id=article_id)
        article=None
        if(article_result.count()==1):
            article_orm = article_result.one()
            article=Article.fromORM(article_orm)
        session.close()
        return article

    def findByCode(self, code: int) -> Optional[Article]:
        session=sqla.orm.sessionmaker(bind=self._articles_handler)()
        article_result=session.query(ArticleORM).filter_by(code=code)
        article=None
        if(article_result.count()==1):
            article_orm = article_result.one()
            article=Article.fromORM(article_orm)
        session.close()
        return article

    def insert(self, newArticle: Article) -> bool:
        if newArticle is None:
            raise TypeError('Argument newArticle cannot be None')
        if not isinstance(newArticle, Article):
            raise TypeError('Argument newArticle must be of type Article')
        if newArticle.id is not None:
            raise ValueError('New article cannot have assigned id')
        session=sqla.orm.sessionmaker(bind=self._articles_handler)()
        articleORM=newArticle.toORM()
        session.add(articleORM)
        session.commit()
        inserted_id = articleORM.id
        session.close()
        if inserted_id is None:
            return False
        newArticle.id = inserted_id  # inserting new article will automatically fill id field by new _id in db
        return True

    def update(self, updatedArticle: Article) -> bool:
        if updatedArticle is None or not isinstance(updatedArticle, Article):
            raise TypeError('Invalid argument: updatedArticle')
        session=sqla.orm.sessionmaker(bind=self._articles_handler)()
        updated_article_orm = updatedArticle.toORM()
        select_result=session.query(ArticleORM).filter_by(id=updated_article_orm.id)
        if(select_result.count()==1):
            article_orm = select_result.one()
            article_orm.update(updated_article_orm)
            select_result=True
        else:
            select_result=False
        session.commit()
        session.close()
        return select_result

    def remove(self, article_id: str) -> bool:
        session=sqla.orm.sessionmaker(bind=self._articles_handler)()
        select_result = session.query(ArticleORM).filter_by(id=article_id)
        delete_count = select_result.count()
        if(delete_count>0):
            session.delete(select_result.all())
        session.commit()
        session.close()
        return delete_count >= 1

    def maxArticleCode(self) -> int:
        session=sqla.orm.sessionmaker(bind=self._articles_handler)()
        for result in  session.query(ArticleORM).order_by(ArticleORM.code.desc()).all(): 
            if result.code is not None:
                session.close()
                return result.code
        session.close()
        return -1
