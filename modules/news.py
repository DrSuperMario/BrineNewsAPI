from db import db

from datetime import datetime as dt


class NewsSource(db.Model):
    
    __tablename__='news'

    id = db.Column(db.Integer, primary_key=True)
    newsHeadline = db.Column(db.String(30))
    newsArticle = db.Column(db.String(200))
    articleDate = db.Column(db.String(15), onupdate=dt.now())
    newsArticleId = db.Column(db.Integer, db.ForeignKey('news.id'))

    def __init__(self, newsHeadline, newsArticle, articleDate, newsArticleId):
        self.newsHeadline = newsHeadline
        self.newsArticle = newsArticle
        self.articleDate = articleDate
        self.newsArticleId = newsArticleId

    def json(self):
        return {
                'newsHeadline':self.newsHeadline,
                'newsArticle':self.newsArticle,
                'date':self.articleDate,
                'articleDate':self.newsArticleId
            }
    @classmethod
    def findNewsById(cls, newsArticleId):
        return cls.query.filter_by(Id=newsArticleId).first()

    @classmethod
    def findNewsByHeadline(cls, newsHeadline):
        return cls.query.filter_by(newsHeadline=newsHeadline).first()

    def saveNewsToDb(self):
        db.session.add(self)
        db.session.commit()

    def deleteNewsFromDb(self):
        db.session.delete(self)
        db.session.commit()