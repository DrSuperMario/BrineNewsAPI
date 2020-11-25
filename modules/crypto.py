from db import db

from datetime import datetime as dt


class CryptoSource(db.Model):

    __bind_key__ = 'crypto'
    
    id = db.Column(db.Integer, primary_key=True, info={'bind_key':'crypto'})
    cryptoHeadline = db.Column(db.String(20), info={'bind_key':'crypto'})
    cryptoName = db.Column(db.String(20), info={'bind_key':'crypto'})
    cryptoDate = db.Column(db.String(10), info={'bind_key':'crypto'})
    cryptoPrice = db.Column(db.String(20), info={'bind_key':'crypto'})
    cryptoPriceCap = db.Column(db.String(20), info={'bind_key':'crypto'})
    cryptoVolume = db.Column(db.String(20), info={'bind_key':'crypto'})
    cryptoCirculation = db.Column(db.String(20), info={'bind_key':'crypto'})
    cryptoCreationDate = db.Column(db.String(20), onupdate=dt.strftime(dt.now(), "%d-%m-%Y %H:%M"), info={'bind_key':'crypto'})
    cryptoId = db.Column(db.String(20), db.ForeignKey('crypto.id'), info={'bind_key':'crypto'})

    def __init__(self,
                 cryptoHeadline,
                 cryptoName,
                 cryptoDate,
                 cryptoPrice, 
                 cryptoPriceCap, 
                 cryptoVolume,
                 cryptoCirculation,
                 cryptoCreationDate,
                 cryptoId):

        self.cryptoHeadline = cryptoHeadline
        self.cryptoName = cryptoName
        self.cryptoDate = cryptoDate
        self.cryptoPrice = cryptoPrice
        self.cryptoPriceCap = cryptoPriceCap
        self.cryptoVolume = cryptoVolume
        self.cryptoCirculation = cryptoCirculation
        self.cryptoCreationDate = cryptoCreationDate
        self.cryptoId = cryptoId 

    def json(self):
        return { 

                'cryptoName':self.cryptoName,
                'cryptoDate':self.cryptoDate, 
                'cryptoPrice':self.cryptoPrice,       
                'cryptoPriceCap':self.cryptoPriceCap,    
                'cryptoVolume':self.cryptoVolume,    
                'cryptoCirculation':self.cryptoCirculation,    
                'cryptoCreationDate':self.cryptoCreationDate,    
                'cryptoId':self.cryptoId
        }        

    @classmethod
    def findCryptoById(cls,cryptoId):
        return cls.query.filter_by(cryptoId=cryptoId).first()

    def saveCryptoToDb(self):
        db.session.add(self)
        db.session.commit()

    def deleteCryptoFromDb(self):
        db.session.delete(self)
        db.session.commit()
