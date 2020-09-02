from flask_restful import Resource, reqparse
from modules.news import NewsSource

from datetime import datetime as dt

class News(Resource):
    
    parser = reqparse.RequestParser()
    parser.add_argument('newsHeadline', type=str, required=False, help="You Must add Headline")
    parser.add_argument('Article', type=str, required=True, help="Article must be addes")
    parser.add_argument('date',type=str,required=False,help="Date must be added")
    parser.add_argument('ArticleId',type=int,required=False,help="ID must be added")

    def get(self, newsHeadline):
        newsHeadline = NewsSource.findNewsById(newsHeadline)
        if newsHeadline:
            return newsHeadline.json()
        return {"message":"News Headline not found"}, 404

    def post(self, newsHeadline):
        newsData = News.parser.parse_args()
        newsData['date'] = dt.now()
        print(newsHeadline)
        news = NewsSource(newsHeadline, **newsData)
        newsId = NewsSource.findNewsById(newsData['newsArticleId'])
        if not newsId:
            return {"message":"News article ID not found"}, 404
        try:
            news.saveNewsToDb()
        except:
            return {"message":"An error occured while loading"}, 400
        
        return news.json(), 201

class NewsList(Resource):
    def get(self):
        return {'news':[x.json() for x in NewsSource.query.all()]}