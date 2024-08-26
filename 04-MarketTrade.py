# -*- coding: utf-8 -*-
"""
  某交易日中買賣搓合商品交易
  暫由隨機產生資料，之後需買家由應用系統輸入
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

    def get_random_buyers(self):
        aql = "FOR doc IN Buyers RETURN doc._key"
        buyerIDs = self.database.AQLQuery(aql, rawResults=True, batchSize=100)
        minNumOfBuyers = int(0.6 * len(buyerIDs))
        randomBuyers = numpy.random.choice(buyerIDs, numpy.random.randint(minNumOfBuyers, len(buyerIDs)))

        return randomBuyers

    def get_supplier_offers(self, today):
        aql = [
            'FOR doc IN SupplierOffers FILTER (doc.`offerDate` == "%s") ' % today,
            'RETURN { key: doc._key, rev: doc._rev, supplierID: doc.`supplierID`, ',
            'supplierName: doc.`supplierName`, itemKeyList: doc.`itemKeyList` }'
        ]

        supplier_offers = self.database.AQLQuery(''.join(aql), rawResults=True, batchSize=100)

        return supplier_offers

    def generate(self, today):
        randomBuyers = self.get_random_buyers()
        supplier_offers = self.get_supplier_offers(today)

        dbTable = self.database['MarketTrade']
        dbTable.truncate()

        dbTableBuyers = self.database['Buyers']

        for _key in randomBuyers:
            _offers = numpy.random.choice(supplier_offers, numpy.random.randint(1, 5))
            
            for _offer in _offers:
                _items = numpy.random.choice(_offer['itemKeyList'], numpy.random.randint(0, len(_offer['itemKeyList'])))

                for _item in _items:
                    _doc = dbTable.createDocument()

                    _doc['buyDate'] = today
                    _doc['buyerKey'] = _key
                    _doc['buyerID'] = dbTableBuyers[_key]['buyerID']
                    _doc['buyerName'] = dbTableBuyers[_key]['name']
                    _doc['buyerPhone'] = dbTableBuyers[_key]['phone']
                    _doc['offerKey'] = _offer['key']
                    _doc['offerRev'] = _offer['rev']
                    _doc['supplierID'] = _offer['supplierID']
                    _doc['supplierName'] = _offer['supplierName']
                    _doc['itemID'] = _item['itemID']
                    _doc['itemName'] = _item['itemName']
                    _doc['itemQty'] = _item['itemQty']
                    _doc['buyQty'] = numpy.random.randint(1, _item['itemQty'])
                    _doc['itemPrice'] = _item['itemPrice']
                    _doc['buyAmount'] = _doc['itemPrice'] * _doc['buyQty']

                    _doc._key = str(uuid.uuid4())

                    _doc.save()


if __name__ == '__main__':
    worker = MarketTrade()
    worker.generate(today='2024-03-15')
