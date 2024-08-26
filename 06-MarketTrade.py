# -*- coding: utf-8 -*-
"""
  某交易日中買賣搓合商品交易
  賣家交易統計
"""

from pyArango.connection import Connection
import numpy
import uuid
import math


class MarketTrade:
    def __init__(self, dbHost='localhost', dbUser='emprogria', dbSecret='sun7flower27'):
        dbConnection = Connection(arangoURL='http://%s:8529/' % dbHost,
                                  username=dbUser, password=dbSecret)

        self.database = dbConnection['Emprogria']

    def get_market_trade(self, today):
        aql = [
            'FOR doc IN MarketTrade FILTER (doc.`buyDate` == "%s") ' % today,
            'SORT doc.supplierID, doc.itemID '
            'RETURN doc'
        ]

        market_trade = self.database.AQLQuery(' '.join(aql), rawResults=True, batchSize=100)

        return market_trade

    def query(self, today):
        market_trade = self.get_market_trade(today)
        _supplierID = ''
        _itemID = ''
        _soldAmount = 0.00

        for _trade in market_trade:
            if _supplierID != _trade['supplierID']:
                if _soldAmount > 0.00:
                    print('\t\t\t\t%8.2f :小計' % _soldAmount)

                _supplierID = _trade['supplierID']
                _itemID = ''
                _soldAmount = 0.00

                print('%s-%s' % (_trade['supplierID'], _trade['supplierName']))

            if _itemID != _trade['itemID']:
                _itemID = _trade['itemID']

                if _soldAmount > 0.00:
                    print('\t\t\t\t%8.2f :小計\n\t%s-%s' % (_soldAmount, _trade['itemID'], _trade['itemName']))
                else:
                    print('\t%s-%s' % (_trade['itemID'], _trade['itemName']))

            _soldAmount +=  _trade['buyAmount']
            print('\t\t%s\t%3d\t%8.2f' % (_trade['buyerName'], _trade['buyQty'], _trade['buyAmount']))

        print('\t\t\t\t%8.2f :小計' % _soldAmount)


if __name__ == '__main__':
    worker = MarketTrade()
    worker.query(today='2024-03-15')
