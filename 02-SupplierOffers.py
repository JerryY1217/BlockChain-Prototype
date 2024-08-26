# -*- coding: utf-8 -*-
"""
  某交易日中賣家可提供商品
  暫由隨機產生資料，之後需賣家由應用系統輸入
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

    def get_random_suppliers(self):
        aql = "FOR doc IN Suppliers RETURN doc._key"
        supplierIDs = self.database.AQLQuery(aql, rawResults=True, batchSize=100)
        minNumOfSuppliers = int(0.6 * len(supplierIDs))
        randomSupplyers = numpy.random.choice(supplierIDs, numpy.random.randint(minNumOfSuppliers, len(supplierIDs)))

        return randomSupplyers

    def get_product_keys(self):
        aql = "FOR doc IN Products RETURN doc._key"
        itemIDs = self.database.AQLQuery(aql, rawResults=True, batchSize=100)

        return itemIDs

    def generate(self, today):
        randomSupplyers = self.get_random_suppliers()
        itemIDs = self.get_product_keys()

        dbTable = self.database['SupplierOffers']
        dbTable.truncate()

        dbTableSuppliers = self.database['Suppliers']
        dbTableProducts = self.database['Products']

        for _key in randomSupplyers:
            _doc = dbTable.createDocument()

            _doc['offerDate'] = today
            _doc['supplierID'] = dbTableSuppliers[_key]['supplierID']
            _doc['supplierKey'] = _key
            _doc['supplierName'] = dbTableSuppliers[_key]['name']
            _doc['phone'] = dbTableSuppliers[_key]['phone']

            randomItems = numpy.random.choice(itemIDs, numpy.random.randint(1, 5))
            _offer = []

            for _key2 in randomItems:
                _prices = [math.ceil(dbTableProducts[_key2]['LowPrice']),
                            math.ceil(dbTableProducts[_key2]['HighPrice'])]

                if _prices[0] == _prices[1]:
                    _prices[1] += 1

                _offer.append({
                    'itemID': dbTableProducts[_key2]['itemID'],
                    'itemName': '%s-%s' % (dbTableProducts[_key2]['name'], dbTableProducts[_key2]['subname']),
                    'itemKey': _key2,
                    'itemQty': numpy.random.randint(15, 50),
                    'itemPrice': numpy.random.randint(_prices[0], _prices[1])
                    })

            _doc['itemKeyList'] = _offer

            _doc._key = str(uuid.uuid4())

            _doc.save()


if __name__ == '__main__':
    worker = MarketTrade()
    worker.generate(today='2024-03-15')
