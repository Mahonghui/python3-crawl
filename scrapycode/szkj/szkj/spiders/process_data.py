from pymongo import mongo_client
from csv import DictWriter


class Mongo2Csv():
    def __init__(self, path='./policy.csv', host='127.0.0.1', port=27017, db_name='szkj', doc_name='policy'):
        self.to_path = path
        self.conn = mongo_client.MongoClient(host=host, port=port)
        self.db = self.conn[db_name]
        self.doc = self.db[doc_name]
        if not self.conn:
            raise Exception('Connection failure')

    def migrate(self):
        cursor = self.doc.find()
        filed_names = cursor[0].keys()
        with open(self.to_path, 'w') as f:
            csv_writer = DictWriter(f, filed_names)
            csv_writer.writeheader()
            for item in cursor:
                csv_writer.writerow(item)


client = Mongo2Csv()
client.migrate()
