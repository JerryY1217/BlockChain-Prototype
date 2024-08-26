# -*- coding: utf-8 -*-
'''
  匯入商品資料
'''

import pandas
from pyArango.connection import Connection
import json
import uuid


class MarketTrade:
    def __init__(self, dbHost='localhost', dbUser='emprogria', dbSecret='sun7flower27'):
        dbConnection = Connection(arangoURL='http://%s:8529/' % dbHost,
                                    username=dbUser, password=dbSecret)

        self.database = dbConnection['Emprogria']

    def generate(self, priceTableFile):
        source = pandas.read_csv(priceTableFile)
        print(source.shape)

        dbTable = self.database['Products']
        dbTable.truncate()

        for i in range(source.shape[0]):
            _row = source.iloc[i]

            _doc = dbTable.createDocument()

            _doc['itemID'] = _row['產品']
            _doc['name'] = _row['名稱']

            if _row['品名'] == _row['品名']:
                _doc['subname'] = _row['品名']
            else:
                _doc['subname'] = _row['名稱']

            _doc._key = str(uuid.uuid4())

            _doc['HighPrice'] = float(_row['平均上價'])
            _doc['MidPrice'] = float(_row['平均中價'])
            _doc['LowPrice'] = float(_row['平均下價'])

            _doc.save()


if __name__ == '__main__':
    worker = MarketTrade()
    worker.generate(priceTableFile='data/產品當期價格對照表.csv')
