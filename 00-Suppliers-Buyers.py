# -*- coding: utf-8 -*-
'''
  暫由隨機產生資料，之後需買/賣家由應用系統輸入
'''

from pyArango.connection import Connection
from faker import Faker
import uuid


class MarketTrade:
    def __init__(self, dbHost='localhost', dbUser='emprogria', dbSecret='sun7flower27'):
        dbConnection = Connection(arangoURL='http://%s:8529/' % dbHost,
                                    username=dbUser, password=dbSecret)

        self.database = dbConnection['Emprogria']
        self.fake = Faker('zh_TW')

    def generate_suppliers(self, numOfSupplers=1000):
        dbTable = self.database['Suppliers']
        dbTable.truncate()

        for i in range(numOfSupplers):
            _doc = dbTable.createDocument()

            _doc['supplierID'] = 'S%05d' % (i + 1)
            _doc['name'] = self.fake.name()
            _doc['phone'] = self.fake.phone_number()
            _doc['email'] = self.fake.email()
            _doc['address'] = self.fake.address()

            _doc._key = str(uuid.uuid4())

            _doc.save()

    def generate_buyers(self, numOfBuyers=3000):
        dbTable = self.database['Buyers']
        dbTable.truncate()

        for i in range(numOfBuyers):
            _doc = dbTable.createDocument()

            _doc['buyerID'] = 'B%05d' % (i + 1)
            _doc['name'] = self.fake.name()
            _doc['phone'] = self.fake.phone_number()
            _doc['email'] = self.fake.email()
            _doc['address'] = self.fake.address()

            _doc._key = str(uuid.uuid4())

            _doc.save()


if __name__ == '__main__':
    worker = MarketTrade()

    worker.generate_suppliers()
    worker.generate_buyers()
