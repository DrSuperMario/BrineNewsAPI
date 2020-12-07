import os

from flask import Flask, request
from flask_restful import Api
from flask_jwt_extended import JWTManager

from resources.news import News, NewsList 
from resources.crypto import Crypto, CryptoList 
from resources.forex import Forex, ForexList
from resources.admin import AdminRegister, AdminLogin

from db import db

app = Flask(__name__)

app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
app.config['SQLALCHEMY_BINDS'] = {
                                    'users':'sqlite:///users.db',
                                    'news':'sqlite:///news.db',
                                    'forex':'sqlite:///forex.db',
                                    'crypto':'sqlite:///crypto.db'
                                    }
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXEPTIONS'] = True
app.secret_key = 'CF9SBmhAKeQEYhGWtgMt'

api = Api(app)
jwt = JWTManager(app)

api.add_resource(NewsList,'/newslist')
api.add_resource(News, '/news/<string:newsArticleId>')
api.add_resource(CryptoList,'/cryptolist')
api.add_resource(Crypto, '/crypto/<string:cryptoId>')
#api.add_resource(News, '/updatenews/<int:newsArticleId>')
api.add_resource(ForexList,'/forexlist')
api.add_resource(Forex, '/forex/<string:forexId>')
api.add_resource(AdminRegister,'/handsoff')
api.add_resource(AdminLogin,'/login')

db.init_app(app)

@app.before_first_request
def create_tables():
    try:
        if request.method == "POST":
            if os.path.exists('data.db'):
                os.remove('data.db')
        db.create_all(bind='crypto')
        db.create_all(bind='forex')
        db.create_all(bind='news')
        

    except:
        print("UUPS Something went seriously wrong") 


if __name__=="__main__":

    app.run(threaded=True, port=5000)
   



