from db import db

from datetime import datetime as dt


class NewsSource(db.Model):
    
    __bind_key__ ='news'
    __tablename__= 'news'

    id = db.Column(db.Integer, primary_key=True, info={'bind_key':'news'})
    newsHeadline = db.Column(db.String(60), info={'bind_key':'news'})
    newsArticle = db.Column(db.String(2000), info={'bind_key':'news'})
    newsArticleWWW = db.Column(db.String(200), info={'bind_key':'news'})
    newsPolarityNeg = db.Column(db.Float, info={'bind_key':'news'})
    newsPolarityPos = db.Column(db.Float, info={'bind_key':'news'})
    newsPolarityNeu = db.Column(db.Float, info={'bind_key':'news'})
    creationDate = db.Column(db.String(15), info={'bind_key':'news'})
    articleDate = db.Column(db.String(15), onupdate=dt.strftime(dt.now(), "%d-%m-%Y %H:%M"), info={'bind_key':'news'})
    newsArticleId = db.Column(db.Integer, db.ForeignKey('news.id'), info={'bind_key':'news'})

    def __init__(self, 
                 newsHeadline, 
                 newsArticle,
                 newsArticleWWW, 
                 newsPolarityNeg, 
                 newsPolarityPos, 
                 newsPolarityNeu,
                 creationDate, 
                 articleDate, 
                 newsArticleId):

        self.newsHeadline = newsHeadline
        self.newsArticle = newsArticle
        self.newsArticleWWW = newsArticleWWW
        self.newsPolarityNeg = newsPolarityNeg
        self.newsPolarityPos = newsPolarityPos
        self.newsPolarityNeu = newsPolarityNeu
        self.creationDate = creationDate
        self.articleDate = articleDate
        self.newsArticleId = newsArticleId

    def json(self):
        return {
                'newsArticle':self.newsArticle,
                'newsArticleWWW':self.newsArticleWWW,
                'articleDate':self.articleDate,
                'newsPolarityNeg':self.newsPolarityNeg,
                'newsPolarityPos':self.newsPolarityPos,
                'newsPolarityNeu':self.newsPolarityNeu,
                'creationDate':self.creationDate,
                'newsArticleId':self.newsArticleId
            }
        
    @classmethod
    def findNewsById(cls,newsArticleId):
        return cls.query.filter_by(newsArticleId=newsArticleId).first()

    @classmethod
    def findNewsByHeadline(cls, newsHeadline):
        return cls.query.filter_by(newsHeadline=newsHeadline).first()

    @classmethod
    def findNewsByDate(cls, articleDate):
        return cls.query.filter_by(articleDate=articleDate).first()   
        
    def saveNewsToDb(self):
        db.session.add(self)
        db.session.commit()

    def deleteNewsFromDb(self):
        db.session.delete(self)
        db.session.commit()

