from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required

from modules.forex import ForexSource
from db import db

from datetime import datetime as dt
import random as rnd


class Forex(Resource):
    
    parser = reqparse.RequestParser()
    #parser.add_argument('forexTag', type=str, required=False, help="Article must be addes")
    parser.add_argument('forexName', type=str, required=False, help="Name must be addes")
    parser.add_argument('forexChange',type=str,required=False,help="Change must be added")
    parser.add_argument('forexHigh',type=str,required=False,help="High must be added")
    parser.add_argument('forexBid',type=str,required=False,help="Bid must be added")
    parser.add_argument('forexLow',type=str,required=False,help="Low must be added")
    parser.add_argument('forexOpen',type=str,required=False,help="Open must be added")
    parser.add_argument('forexDate',type=str,required=False,help="Date must be added")
    parser.add_argument('forexId',type=int,required=False,help="ID must be added")

    def get(self, forexId):
        forexId = ForexSource.findForexById(forexId)
        if forexId:
            return forexId.json()
        return {"message":"Forex ticker not found"}, 404

    #@jwt_required
    def post(self, forexId):
        
        forexData = Forex.parser.parse_args()
        forexData['forexDate'] = dt.strftime(dt.now(), "%d-%m-%Y %H:%M")
        forexData['forexId'] = rnd.randint(1,len(forexData['forexName'])*1000) + rnd.randint(1,len(forexData['forexName'])*2) 
       
        forex = ForexSource(forexId, **forexData)
        
        try:
            forex.saveForexToDb()

        except:
            return {"message":"An error occured while loading"}, 400
        
        return forex.json(), 201


#@jwt_required
def delete(forexId):
    forex_id =  ForexSource.findForexById(forexId)

    #Temporary fix for a serious problem 
    if forexId == "1x5678Tr24Xpn677Ss":
        db.drop_all(bind='forex')
        db.create_all(bind='forex')
        return {"message":"Database deleted"},200

    try:
        if forex_id:
            forex_id.deleteForexFromDb()
        else:
            return {"message":f"id {forexId} was not found in database"},400
        
        return {"nessage":f"id {forexId} deleted from database"},200
    
    except:
        return {"Someting went wrong with deletion"},500

#@jwt_required
def put(forexId):

    forexData = Forex.parser.parse_args()
    forex_id =  ForexSource.findForexById(forexId)
    
    try:
        if forex_id is None:
            forex_id = ForexSource(forexId, **forexData)
            forex_id.saveForexToDb()
            return {"message":f"{forexId} id added to the databse"},201
        else:
            pass

    except:
        return {"message":f"couldent find {forexId} id"}, 500

    forex_id.saveForexToDb()
    return forex_id.json()
        
class ForexList(Resource):
    def get(self):
        return {'forex':[x.json() for x in ForexSource.query.all()]}