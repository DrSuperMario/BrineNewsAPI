import os

from flask import Flask
from flask_restful import Api
#from flask_jwt_extended import JWTManager

from resources.news import News, NewsList 

from db import db

app = Flask(__name__)

app.config['DEBUG'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXEPTIONS'] = True
app.secret_key = 'Z5dsads77730j'

api = Api(app)
#jwt = JWTManager(app)

api.add_resource(NewsList,'/newslist')
api.add_resource(News, '/postnews/<string:newsHeadline>')

if __name__=="__main__":
    db.init_app(app)

    @app.before_first_request
    def create_tables():
        try:
            db.create_all()
        except:
            print("UUPS Something went seriously wrong")

    app.run(threaded=True, port=5000)




