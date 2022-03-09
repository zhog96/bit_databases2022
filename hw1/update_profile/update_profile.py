import pandas as pd
from pymongo import MongoClient, ASCENDING, TEXT
import json
import time
from tqdm import tqdm

class TimeCheck:
    def __init__(self, tag):
        self.tag = tag

    def __enter__(self):
        self.start_time = time.time()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_val:
            raise
        time_passed = (time.time() - self.start_time) * 1000
        print(f'--- {self.tag} took {time_passed} micro_seconds ---')

def reload_data(coll, batch_count):
    data = pd.read_csv('./dataloader/titanic.csv')
    coll.delete_many(filter={})
    for batch_n in tqdm(range(batch_count)):
        data['BatchN'] = batch_n
        payload = json.loads(data.to_json(orient='records'))
        coll.insert_many(payload)
    print(f'inserted {coll.count_documents(filter={})} docks')

def test_update(coll, path, tag): 
    with TimeCheck(tag):
        with open(path) as f:
            query = json.load(f)
        coll.update_many(**query)

if __name__ == "__main__":
    client = MongoClient('localhost', port=27017)
    db = client.get_database('titanic')
    coll = db.get_collection('passengers')
    reload_data(coll, 1000)

    test_update(coll, './queries/update1.json', 'update1_no_index')
    reload_data(coll, 1000)
    coll.create_index([('Fare', ASCENDING)], name='Fare')
    test_update(coll, './queries/update1.json', 'update1_with_index')
    coll.drop_index('Fare')

    test_update(coll, './queries/update2.json', 'update2_no_index')
    reload_data(coll, 1000)
    coll.create_index([('Name', TEXT)], name='Name')
    test_update(coll, './queries/update2.json', 'update2_with_index')
    coll.drop_index('Name')

    reload_data(coll, 1000)
    test_update(coll, './queries/update3_1.json', 'update3_no_index')
    reload_data(coll, 1000)
    coll.create_index([('Name', TEXT)], name='Name')
    test_update(coll, './queries/update3_2.json', 'update3_with_index')
    coll.drop_index('Name')
