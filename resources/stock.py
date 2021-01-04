from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
from modules.stock import StockSource
from db import db

from datetime import datetime as dt
import random as rnd

class Stock(Resource):
    
    parser = reqparse.RequestParser()
    #parser.add_argument('stockHeadline', type=str, required=False, help="You Must add Headline")
    parser.add_argument('stockName', type=str, required=False, help="Stock name must be addes")
    parser.add_argument('stockLow',type=str,required=False,help="Stock low must be added")
    parser.add_argument('stockLast',type=str,required=False,help="Stock last must be added")
    parser.add_argument('stockHigh',type=str,required=False,help="Stock high must be added")
    parser.add_argument('stockChg',type=str,required=False,help="Stock chg must be added")
    parser.add_argument('stockChgp',type=str,required=False,help="Stock chgp must be added")
    parser.add_argument('stockCreationDate',type=str,required=False,help="date must be added")
    parser.add_argument('stockId',type=int,required=False,help="ID must be added")

    def get(self, stockId):
        stockId = StockSource.findstockById(stockId)
        if stockId:
            return stockId.json()
        return {"message":"stock Headline not found"}, 404

    #@jwt_required
    def post(self, stockId):

        stockData = Stock.parser.parse_args()
        stockData['stockCreationDate'] = dt.strftime(dt.now(), "%d-%m-%Y %H:%M")
        stockData['stockId'] = rnd.randint(1,len(stockData['stockName'])*1000) + rnd.randint(1,len(stockData['stockName'])*2) 
    
        stock = StockSource(stockId, **stockData)
        
        try:
            stock.savestockToDb()
            #CrystockId = stockSource.query.delete()

        except:
            return {"message":"An error occured while loading"}, 400
        
        return stock.json(), 201

    #@jwt_required
    def delete(self, stockId):
        stock_id =  StockSource.findstockById(stockId)

        #Temporary fix for a serious problem 
        if stockId == "1x5678Tr24Xpn677Ss":
            db.drop_all(bind='stock')
            db.create_all(bind='stock')
            return {"message":"Database deleted"},200

        try:
            if stock_id:
                stock_id.deletestockFromDb()
            else:
                return {"message":f"id {stockId} was not found in database"},400
            
            return {"nessage":f"id {stockId} deleted from database"},200
        
        except:
            return {"Someting went wrong with deletion"},500
    
    #@jwt_required
    def put(self, stockId):

        stockData = Stock.parser.parse_args()
        stock_id =  StockSource.findstockById(stockId)
        
        try:
            if stock_id is None:
                stock_id = StockSource(stockId, **stockData)
                stock_id.savestockToDb()
                return {"message":f"{stockId} id added to the databse"},201
            else:
                pass

        except:
            return {"message":f"couldent find {stockId} id"}, 500

        stock_id.savestockToDb()
        return stock_id.json()
        
class StockList(Resource):
    def get(self):
        return {'stock':[x.json() for x in StockSource.query.all()]}