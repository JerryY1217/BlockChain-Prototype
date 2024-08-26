# -*- coding: utf-8 -*-
"""
  買家查找某交易日中可提供指定商品之賣家
"""

from pyArango.connection import Connection


class MarketTrade:
    def __init__(self, dbHost='localhost', dbUser='emprogria', dbSecret='sun7flower27'):
        dbConnection = Connection(arangoURL='http://%s:8529/' % dbHost,
                                  username=dbUser, password=dbSecret)

        self.database = dbConnection['Emprogria']

    def query(self, today, itemID):
        aql = [
               'FOR doc IN SupplierOffers',
               'FILTER (doc.`offerDate` == "%s") AND ("%s" IN doc.`itemKeyList`[*].`itemID`)' % (today, itemID),
               'RETURN { supplierID: doc.`supplierID`, supplierName: doc.`supplierName`, itemKeyList: doc.`itemKeyList` }'
               ]

        supplierOffers = self.database.AQLQuery(' '.join(aql), rawResults=True, batchSize=100)

        for _doc in supplierOffers:
            _itemKeyList = _doc['itemKeyList']

            for _doc2 in _itemKeyList:
                if _doc2['itemID'] == itemID:
                    _doc3 = (_doc['supplierID'], _doc['supplierName'], _doc2['itemID'], _doc2['itemQty'],
                             _doc2['itemPrice'])
                    print('%s\t%6s\t%s\t%4d\t%4d' % _doc3)


if __name__ == '__main__':
    worker = MarketTrade()
    worker.query(today='2024-03-15', itemID='FQ1')
