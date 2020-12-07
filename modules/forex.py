from db import db 

from datetime import datetime as dt


class ForexSource(db.Model):

    __bind_key__ = 'forex'
    __tablename__ = 'forex'

    id = db.Column(db.Integer, primary_key=True, info={'bind_key':'forex'})
    forexTag = db.Column(db.String(16), info={'bink_key':'forex'})
    forexName = db.Column(db.String(30), info={'bink_key':'forex'})
    forexChange = db.Column(db.String(30), info={'bink_key':'forex'})
    forexHigh = db.Column(db.Float, info={'bink_key':'forex'})
    forexBid = db.Column(db.Float, info={'bink_key':'forex'})
    forexLow = db.Column(db.Float, info={'bink_key':'forex'})
    forexOpen = db.Column(db.Float, info={'bink_key':'forex'})
    forexDate = db.Column(db.String(20), onupdate=dt.strftime(dt.now(), "%d-%m-%Y %H:%M"), info={'bind_key':'forex'})
    forexId = db.Column(db.Integer, db.ForeignKey('forex.id'), info={'bind_key':'forex'})


    def __init__(self,
                 forexTag,
                 forexName,
                 forexChange,
                 forexHigh,
                 forexBid,
                 forexLow,
                 forexOpen,
                 forexDate,
                 forexId):
        
        self.forexTag = forexTag
        self.forexName = forexName
        self.forexChange = forexChange
        self.forexHigh = forexHigh
        self.forexBid = forexBid
        self.forexLow = forexLow
        self.forexOpen = forexOpen
        self.forexDate = forexDate
        self.forexId = forexId

    def json(self):
        return {

                'forexTag':self.forexTag,
                'forexName':self.forexName,
                'forexChange':self.forexChange,
                'forexHigh':self.forexHigh,
                'forexBid':self.forexBid,
                'forexLow':self.forexLow,
                'forexOpen':self.forexOpen,
                'forexDate':self.forexDate,
                'forexId':self.forexId
        }

    @classmethod
    def findForexById(cls,forexId):
        return cls.query.filter_by(forexId=forexId).first()

    def saveForexToDb(self):
        db.session.add(self)
        db.session.commit()


    def deleteForexFromDb(self):
        db.session.delete(self)
        db.session.commit()
