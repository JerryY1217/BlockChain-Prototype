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

    def get_market_trade(self, today):
        aql = [
            'FOR doc IN MarketTrade FILTER (doc.`buyDate` == "%s") ' % today,
            'SORT doc.buyerID, doc.itemID '
            'RETURN doc'
        ]

        market_trade = self.database.AQLQuery(' '.join(aql), rawResults=True, batchSize=100)

        return market_trade

    def get_sesme(self, s):
        return hashlib.sha256(s.encode('utf-8')).hexdigest()

    def secure(self, today):
        market_trade = self.get_market_trade(today)

        dbTable = self.database['TradeBlockChain']
        dbTable.truncate()

        _prevKey = 'HEAD'

        for _trade in market_trade:
            _doc = dbTable.createDocument()

            _doc['offerDate'] = today
            _doc['tradeRev'] = _trade['_rev']
            _doc['tradeKey'] = _trade['_key']

            _doc['secureParties'] = self.get_sesme('%s~%s' % (_trade['supplierID'], _trade['buyerID']))
            _doc['secureTrade'] = self.get_sesme('%s~%.2f~%.2f' % (_trade['itemID'], _trade['buyQty'], _trade['buyAmount']))

            _doc['tradeLink'] = _prevKey
            _prevKey = _trade['_key']

            _doc._key = str(uuid.uuid4())
            _doc.save()


if __name__ == '__main__':
    worker = MarketTrade()
    worker.secure(today='2024-03-15')
