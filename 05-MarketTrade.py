# -*- coding: utf-8 -*-
"""
  某交易日中買賣搓合商品交易
  買家交易統計
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
            'SORT doc.buyerID, doc.itemID '
            'RETURN doc'
        ]

        market_trade = self.database.AQLQuery(' '.join(aql), rawResults=True, batchSize=100)

        return market_trade

    def query(self, today):
        market_trade = self.get_market_trade(today)
        _buyerID = ''
        _itemID = ''
        _buyAmount = 0.00

        for _trade in market_trade:
            if _buyerID != _trade['buyerID']:
                if _buyAmount > 0.00:
                    print('\t\t\t\t%8.2f :小計' % _buyAmount)

                _buyerID = _trade['buyerID']
                _itemID = ''
                _buyAmount = 0.00

                print('%s-%s' % (_trade['buyerID'], _trade['buyerName']))

            if _itemID != _trade['itemID']:
                _itemID = _trade['itemID']

                if _buyAmount > 0.00:
                    print('\t\t\t\t%8.2f :小計\n\t%s-%s' % (_buyAmount, _trade['itemID'], _trade['itemName']))
                else:
                    print('\t%s-%s' % (_trade['itemID'], _trade['itemName']))

            _buyAmount +=  _trade['buyAmount']
            print('\t\t%s\t%3d\t%8.2f' % (_trade['supplierName'], _trade['buyQty'], _trade['buyAmount']))

        print('\t\t\t\t%8.2f :小計' % _buyAmount)


if __name__ == '__main__':
    worker = MarketTrade()
    worker.query(today='2024-03-15')
