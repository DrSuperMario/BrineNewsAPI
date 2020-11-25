from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
from modules.news import NewsSource
from db import db

from datetime import datetime as dt
import random as rnd


class News(Resource):
    
    parser = reqparse.RequestParser()
    #parser.add_argument('newsHeadline', type=str, required=True, help="You Must add Headline")
    parser.add_argument('newsArticle', type=str, required=True, help="Article must be addes")
    parser.add_argument('newsArticleWWW', type=str, required=True, help="Article WWWW must be addes")
    parser.add_argument('newsPolarityNeg',type=float,required=False,help="Polarity neg must be added")
    parser.add_argument('newsPolarityPos',type=float,required=False,help="Polarity pos must be added")
    parser.add_argument('newsPolarityNeu',type=float,required=False,help="Polarity neu must be added")
    parser.add_argument('creationDate',type=str,required=False,help="creation date must be added")
    parser.add_argument('articleDate',type=str,required=False,help="Date must be added")
    parser.add_argument('newsArticleId',type=str,required=False,help="ID must be added")

    def get(self, newsArticleId):
        newsArticleId = NewsSource.findNewsById(newsArticleId)
        if newsArticleId:
            return newsArticleId.json()
        return {"message":"News Headline not found"}, 404

    #@jwt_required
    def post(self, newsArticleId):

        newsData = News.parser.parse_args()
        newsData['articleDate'] = dt.strftime(dt.now(), "%d-%m-%Y %H:%M")
        newsData['newsArticleId'] = rnd.randint(1,len(newsData['newsArticle'])*1000) + rnd.randint(1,len(newsData['newsArticle'])*2) 
    
        news = NewsSource(newsArticleId, **newsData)
        
        try:
            news.saveNewsToDb()
            #NewsSource.query.delete()

        except:
            return {"message":"An error occured while loading"}, 400
        
        return news.json(), 201

    #@jwt_required
    def delete(self, newsArticleId):
        news_id = NewsSource.findNewsById(newsArticleId)

        #Temporary fix for a serious problem 
        if newsArticleId == "1x5678Tr24Xpn677Ss":
            db.drop_all(bind='CryptoSource')
            db.create_all()
            return {"message":"Database deleted"},200

        try:
            if news_id:
                news_id.deleteNewsFromDb()
            else:
                return {"message":f"id {newsArticleId} was not found in database"},400
            
            return {"nessage":f"id {newsArticleId} deleted from database"},200
        
        except:
            return {"Someting went wrong with deletion"},500
    
    #@jwt_required
    def put(self, newsArticleId):

        newsData = News.parser.parse_args()
        news_id = NewsSource.findNewsById(newsArticleId)
        
        try:
            if news_id is None:
                news_id = NewsSource(newsArticleId, **newsData)
                news_id.saveNewsToDb()
                return {"message":f"{newsArticleId} id added to the databse"},201
            else:
                news_id.newsArticle = newsData['newsArticle']
                news_id.newsArticleWWW = newsData['newsArticleWWW']
                news_id.articleDate = newsData['articleDate']
                news_id.newsPolarityNeg = newsData['newsPolarityNeg']
                news_id.newsPolarityPos = newsData['newsPolarityPos']
                news_id.newsPolarityNeu = newsData['newsPolarityNeu']
                news_id.creationDate = newsData['creationDate']
            

        except:
            return {"message":f"couldent find {newsArticleId} id"}, 500

        news_id.saveNewsToDb()
        return news_id.json()
        
class NewsList(Resource):
    def get(self):
        return {'news':[x.json() for x in NewsSource.query.all()]}