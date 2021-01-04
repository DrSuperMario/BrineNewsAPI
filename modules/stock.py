from db import db

from datetime import datetime as dt


class StockSource(db.Model):

    __bind_key__ = 'stock'
    __tablename__ = 'stock'
    
    id = db.Column(db.Integer, primary_key=True, info={'bind_key':'stock'})
    stockHeadline = db.Column(db.String(20), info={'bind_key':'stock'})
    stockName = db.Column(db.String(20), info={'bind_key':'stock'})
    #stockDate = db.Column(db.String(10), info={'bind_key':'stock'})
    stockLow = db.Column(db.String(20), info={'bind_key':'stock'})
    stockLast = db.Column(db.String(20), info={'bind_key':'stock'})
    stockHigh = db.Column(db.String(20), info={'bind_key':'stock'})
    stockChg = db.Column(db.String(20), info={'bind_key':'stock'})
    stockChgp = db.Column(db.String(20), onupdate=dt.strftime(dt.now(), "%d-%m-%Y %H:%M"), info={'bind_key':'stock'})
    stockCreationDate = db.Column(db.String(20), onupdate=dt.strftime(dt.now(), "%d-%m-%Y %H:%M"), info={'bind_key':'stock'})
    stockId = db.Column(db.Integer, db.ForeignKey('stock.id'), info={'bind_key':'stock'})

    def __init__(self,
                 stockHeadline,
                 stockName,
                 stockLow, 
                 stockLast, 
                 stockHigh,
                 stockChg,
                 stockChgp,
                 stockCreationDate,
                 stockId):

        self.stockHeadline = stockHeadline
        self.stockName = stockName
        self.stockLow = stockLow
        self.stockLast = stockLast
        self.stockHigh = stockHigh
        self.stockChg = stockChg
        self.stockChgp = stockChgp
        self.stockCreationDate = stockCreationDate
        self.stockId = stockId 

    def json(self):
        return { 

                'stockName':self.stockName,
                'stockLow':self.stockLow,       
                'stockLast':self.stockLast,    
                'stockHigh':self.stockHigh,    
                'stockChg':self.stockChg,    
                'stockChgp':self.stockChgp,  
                'stockCreationDate':self.stockCreationDate,  
                'stockId':self.stockId
        }        

    @classmethod
    def findstockById(cls,stockId):
        return cls.query.filter_by(stockId=stockId).first()

    def savestockToDb(self):
        db.session.add(self)
        db.session.commit()

    def deletestockFromDb(self):
        db.session.delete(self)
        db.session.commit()
