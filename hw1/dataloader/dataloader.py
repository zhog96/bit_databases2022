import pandas as pd
from pymongo import MongoClient
import json

if __name__ == "__main__":
    client = MongoClient('10.5.0.5', port=27017)
    db = client.get_database('titanic')
    coll = db.get_collection('passengers')
    data = pd.read_csv('data/titanic.csv')
    coll.delete_many(filter={})
    for batch_n in range(1000):
        data['BatchN'] = batch_n
        payload = json.loads(data.to_json(orient='records'))
        coll.insert_many(payload)
    print(f'inserted {coll.count_documents(filter={})} docks')
