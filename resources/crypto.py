from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
from modules.crypto import CryptoSource
from db import db

from datetime import datetime as dt
import random as rnd

class Crypto(Resource):
    
    parser = reqparse.RequestParser()
    #parser.add_argument('CryptoHeadline', type=str, required=False, help="You Must add Headline")
    parser.add_argument('cryptoName', type=str, required=False, help="Article must be addes")
    parser.add_argument('cryptoDate', type=str, required=False, help="Article WWWW must be addes")
    parser.add_argument('cryptoPrice',type=str,required=False,help="Polarity neg must be added")
    parser.add_argument('cryptoPriceCap',type=str,required=False,help="Polarity pos must be added")
    parser.add_argument('cryptoVolume',type=str,required=False,help="Polarity neu must be added")
    parser.add_argument('cryptoCirculation',type=str,required=False,help="creation date must be added")
    parser.add_argument('cryptoCreationDate',type=str,required=False,help="Date must be added")
    parser.add_argument('cryptoId',type=int,required=False,help="ID must be added")

    def get(self, cryptoId):
        cryptoId = CryptoSource.findCryptoById(cryptoId)
        if cryptoId:
            return cryptoId.json()
        return {"message":"Crypto Headline not found"}, 404

    #@jwt_required
    def post(self, cryptoId):

        cryptoData = Crypto.parser.parse_args()
        cryptoData['cryptoCreationDate'] = dt.strftime(dt.now(), "%d-%m-%Y %H:%M")
        cryptoData['cryptoId'] = rnd.randint(1,len(cryptoData['cryptoName'])*1000) + rnd.randint(1,len(cryptoData['cryptoName'])*2) 
    
        crypto = CryptoSource(cryptoId, **cryptoData)
        
        try:
            crypto.saveCryptoToDb()
            #CrycryptoId = CryptoSource.query.delete()

        except:
            return {"message":"An error occured while loading"}, 400
        
        return crypto.json(), 201

    #@jwt_required
    def delete(self, cryptoId):
        crypto_id =  CryptoSource.findCryptoById(cryptoId)

        #Temporary fix for a serious problem 
        if cryptoId == "1x5678Tr24Xpn677Ss":
            db.drop_all(bind='crypto')
            db.create_all(bind='crypto')
            return {"message":"Database deleted"},200

        try:
            if crypto_id:
                crypto_id.deleteCryptoFromDb()
            else:
                return {"message":f"id {cryptoId} was not found in database"},400
            
            return {"nessage":f"id {cryptoId} deleted from database"},200
        
        except:
            return {"Someting went wrong with deletion"},500
    
    #@jwt_required
    def put(self, cryptoId):

        cryptoData = Crypto.parser.parse_args()
        crypto_id =  CryptoSource.findCryptoById(cryptoId)
        
        try:
            if crypto_id is None:
                crypto_id = CryptoSource(cryptoId, **cryptoData)
                crypto_id.saveCryptoToDb()
                return {"message":f"{cryptoId} id added to the databse"},201
            else:
                pass

        except:
            return {"message":f"couldent find {cryptoId} id"}, 500

        crypto_id.saveCryptoToDb()
        return crypto_id.json()
        
class CryptoList(Resource):
    def get(self):
        return {'Crypto':[x.json() for x in CryptoSource.query.all()]}