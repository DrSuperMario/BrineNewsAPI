from flask_restful import Resource, reqparse
from modules.news import NewsSource

from datetime import datetime as dt

class News(Resource):
    
    parser = reqparse.RequestParser()
    parser.add_argument('newsHeadline', type=str, required=True, help="You Must add Headline")
    parser.add_argument('newsArticle', type=str, required=True, help="Article must be addes")
    parser.add_argument('date',type=str,required=True,help="Date must be added")
    parser.add_argument('newsArticleId',type=int,required=True,help="ID must be added")

    def get(self, newsHeadline):
        newsHeadline = NewsSource.findNewsById(newsHeadline)
        if newsHeadline:
            return newsHeadline.json()
        return {"message":"News Headline not found"}, 404

    def post(self, newsHeadline):
        newsdata = News.parser.parse_args()
        newsData['date'] = dt.now()
        news = NewsSource(newsHeadline, **newsData)
        newsId = NewsSource.findNewsById(newsData['newsArticleId'])
        if not market:
            return {"message":"News article ID not found"}, 404
        try:
            News.saveNewsToDb()
        except:
            return {"message":"An error occured while loading"}, 400
        
        return News.json(), 201

class NewsList(Resource):
    def get(self):
        return {'news':[x.json() for x in NewsSource.query_all()]}