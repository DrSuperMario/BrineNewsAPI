import os

from flask import Flask
from flask_restful import Api
#from flask_jwt_extended import JWTManager

from resources.news import NewsSource, NewsList 

from db import db

app = Flask(__name__)

app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['PROPAGATE_EXEPTIONS'] = True
app.secret_key = 'Z5dsads77730j'

api = Api(app)
#jwt = JWTManager(app)

api.add_resource(NewsList,'/NewsList')

if __name__=="__main__":
    app.run(port=5050)




