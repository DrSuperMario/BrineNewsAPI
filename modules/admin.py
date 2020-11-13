from logging import info
from db import db

class AdminModel(db.Model):
    
    __bind_key__ = 'users'

    id = db.Column(db.Integer, primary_key=True, info={'bind_key':'users'})
    username = db.Column(db.String(80),info={'bind_key':'users'})
    password = db.Column(db.String(30), info={'bind_key':'users'})
    email = db.Column(db.String(40), info={'bind_key':'users'})


    def __init__(self, username, password, email):
        self.username = username
        self.password = password 
        self.email = email 
        

    def json(self):
        return {
            'id':self.id,
            'username':self.username,
            'password':self.password
        }
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls,username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()