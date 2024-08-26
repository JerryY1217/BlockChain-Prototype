# -*- coding: utf-8 -*-
"""
  鎖存某交易日中買賣搓合商品交易
  商品交易區塊，休市後由系統管理員執行
"""

from pyArango.connection import Connection
import numpy
import uuid
import hashlib


class MarketTrade:
    def __init__(self, dbHost='localhost', dbUser='emprogria', dbSecret='sun7flower27'):
        dbConnection = Connection(arangoURL='http://%s:8529/' % dbHost,
                                  username=dbUser, password=dbSecret)

        self.database = dbConnection['Emprogria']

    def get_blockchains(self, today, supplierID, buyerID, itemID, buyQty, buyAmount):
        _secureParties = self.get_sesme('%s~%s' % (supplierID, buyerID))
        _secureTrade = self.get_sesme('%s~%.2f~%.2f' % (itemID, buyQty, buyAmount))

        aql = [
            'FOR doc IN TradeBlockChain FILTER ',
            'doc.`offerDate` == "%s" AND ' % today,
            'doc.`secureParties` == "%s" AND ' % _secureParties,
            'doc.`secureTrade` == "%s" ' % _secureTrade,
            'RETURN doc'
        ]

        blockchains = self.database.AQLQuery(' '.join(aql), rawResults=True, batchSize=100)

        return blockchains

    def get_trade_revision(self, tradeKey):
        aql = [
            'FOR doc IN MarketTrade FILTER doc._key == "%s" ' % tradeKey,
            'RETURN doc._rev'
        ]

        tradeRev = self.database.AQLQuery(' '.join(aql), rawResults=True, batchSize=100)
        if len(tradeRev) > 0:
            return tradeRev[0]

        return ''

    def get_sesme(self, s):
        return hashlib.sha256(s.encode('utf-8')).hexdigest()

    def validate(self, today, supplierID, buyerID, itemID, buyQty, buyAmount):
        blockchains = self.get_blockchains(today, supplierID, buyerID,
                                            itemID, buyQty, buyAmount)

        fraud = False
        for _chain in blockchains:
            if self.get_trade_revision(_chain['tradeKey']) != _chain['tradeRev']:
                fraud = True
                print('資料 (%s) 已被塗改' % _chain['tradeKey'])

        if len(blockchains) == 0:
            print('交易紀錄遭偽造')
        else:
            if not fraud:
                print('此商品交易為真')



if __name__ == '__main__':
    worker = MarketTrade()

    # FOR doc IN MarketTrade FILTER (doc._key == "a9bc103d-10fe-488d-a6bc-156741d57804") RETURN doc
    # FOR doc IN TradeBlockChain FILTER (doc.`tradeKey` == "a9bc103d-10fe-488d-a6bc-156741d57804") RETURN doc

    #正確資訊:
    worker.validate(today='2024-03-15', supplierID='S00808',
                    buyerID='B00012', itemID='FF4',
                    buyQty=13, buyAmount=143)
    #變更購賣數量:
    worker.validate(today='2024-03-15', supplierID='S00808',
                    buyerID='B00012', itemID='FF4',
                    buyQty=23, buyAmount=143)
    #變更購賣金額:
    worker.validate(today='2024-03-15', supplierID='S00808',
                    buyerID='B00012', itemID='FF4',
                    buyQty=13, buyAmount=140)