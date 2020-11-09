from flask_restful import Resource, reqparse
from modules.news import NewsSource

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
    parser.add_argument('articleDate',type=str,required=False,help="Date must be added")
    parser.add_argument('newsArticleId',type=int,required=False,help="ID must be added")

    def get(self, newsHeadline):
        newsHeadline = NewsSource.findNewsById(newsHeadline)
        if newsHeadline:
            return newsHeadline.json()
        return {"message":"News Headline not found"}, 404

    def post(self, newsHeadline):
        newsData = News.parser.parse_args()
        newsData['articleDate'] = dt.now()  
        newsData['newsArticleId'] = rnd.randint(1,len(newsHeadline)*1000) + rnd.randint(1,len(newsData['newsArticle'])*2) 
    
        news = NewsSource(newsHeadline, **newsData)
        
        try:
            news.saveNewsToDb()
        except:
            return {"message":"An error occured while loading"}, 400
        
        return news.json(), 201

class NewsList(Resource):
    def get(self):
        return {'news':[x.json() for x in NewsSource.query.all()]}