from db import db

from datetime import datetime as dt


class NewsSource(db.Model):
    
    __tablename__='NewsSource'

    id = db.Column(db.Integer, primary_key=True)
    newsHeadline = db.Column(db.String(30))
    newsArticle = db.Column(db.String(2000))
    newsArticleWWW = db.Column(db.String(200))
    newsPolarityNeg = db.Column(db.Float)
    newsPolarityPos = db.Column(db.Float)
    newsPolarityNeu = db.Column(db.Float)
    articleDate = db.Column(db.String(15), onupdate=dt.now())
    newsArticleId = db.Column(db.Integer, db.ForeignKey('NewsSource.id'))

    def __init__(self, newsHeadline, newsArticle, newsArticleWWW, newsPolarityNeg, newsPolarityPos, newsPolarityNeu, articleDate, newsArticleId):
        self.newsHeadline = newsHeadline
        self.newsArticle = newsArticle
        self.newsArticleWWW = newsArticleWWW
        self.newsPolarityNeg = newsPolarityNeg
        self.newsPolarityPos = newsPolarityPos
        self.newsPolarityNeu = newsPolarityNeu
        self.articleDate = articleDate
        self.newsArticleId = newsArticleId

    def json(self):
        return {
                'newsHeadline':self.newsHeadline,
                'newsArticle':self.newsArticle,
                'newsArticleWWW':self.newsArticleWWW,
                'articleDate':self.articleDate,
                'newsPolarityNeg':self.newsPolarityNeg,
                'newsPolarityPos':self.newsPolarityPos,
                'newsPolarityNeu':self.newsPolarityNeu,
                'newsArticleId':self.newsArticleId
            }
        
    @classmethod
    def findNewsById(cls, newsArticleId):
        return cls.query.filter_by(id=newsArticleId).first()

    @classmethod
    def findNewsByHeadline(cls, newsHeadline):
        return cls.query.filter_by(newsHeadline=newsHeadline).first()

    def saveNewsToDb(self):
        db.session.add(self)
        db.session.commit()

    def deleteNewsFromDb(self):
        db.session.delete(self)
        db.session.commit()