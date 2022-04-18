import redis
import rediscluster
import json
import time
from tqdm import tqdm


class TimeCheck:
    def __init__(self, tag, iters):
        self.tag = tag
        self.iters = iters

    def __enter__(self):
        self.start_time = time.time()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_val:
            raise
        time_passed = (time.time() - self.start_time) * 1000
        print(f'--- {self.tag} took {time_passed / self.iters} micro_seconds ---')


if __name__ == '__main__':
    db = redis.Redis(host='localhost', port=6379, db=0)
    rc = rediscluster.RedisCluster(startup_nodes=[
        {'host': "127.0.0.1", 'port': '8001'},
        {'host': "127.0.0.1", 'port': '8002'},
        {'host': "127.0.0.1", 'port': '8003'}
    ], read_from_replicas=True)
    with open('string.json', 'r') as f:
        data = ''.join(f.readlines())
        n_set = 100
        with TimeCheck('save string to redis node', n_set):
            for idx in tqdm(range(n_set)):
                db.set(f'string_{idx}', data)
        n_get = 300
        with TimeCheck('get string from redis node', n_get):
            for idx in tqdm(range(n_get)):
                db.get(f'string_{idx % n_set}')
        for idx in range(n_set):
            db.delete(f'string_{idx}')
        n_set = 100
        with TimeCheck('save string to redis cluster', n_set):
            for idx in tqdm(range(n_set)):
                rc.set(f'string_{idx}', data)
        n_get = 300
        with TimeCheck('get string from redis cluster', n_get):
            for idx in tqdm(range(n_get)):
                rc.get(f'string_{idx}')
        for idx in range(n_set):
            rc.delete(f'string_{idx}')
        
    with open('hash.json', 'r') as f:
        data = json.loads(f.read())
        with TimeCheck('save hash to redis node', 1):
            for key, val in tqdm(data.items()):
                db.hset('hash', key, val)
        with TimeCheck('get hash from redis node', 1):
            for key, _ in tqdm(data.items()):
                db.hget('hash', key)
        db.delete('hash')
        with TimeCheck('save hash to redis cluster', 1):
            for key, val in tqdm(data.items()):
                rc.hset('hash', key, val)
        with TimeCheck('get hash from redis cluster', 1):
            for key, _ in tqdm(data.items()):
                rc.hget('hash', key)
        rc.delete('hash')

    with open('list.json', 'r') as f:
        data = json.loads(f.read())
        with TimeCheck('save list to redis node', 1):
            for val in tqdm(data):
                db.lpush('list', val)
        with TimeCheck('get list from redis node', 1):
            for _ in tqdm(data):
                db.lpop('list')
        db.delete('list')
        with TimeCheck('save list to redis cluster', 1):
            for val in tqdm(data):
                rc.lpush('list', val)
        with TimeCheck('get list from redis cluster', 1):
            for _ in tqdm(data):
                rc.lpop('list')
        rc.delete('list')

    with open('score_set.json', 'r') as f:
        data = json.loads(f.read())
        with TimeCheck('save zset to redis node', 1):
            for key, val in tqdm(data.items()):
                db.zadd('zset', {key: val})
        with TimeCheck('get zset from redis node', 1):
            for _ in tqdm(data):
                db.zpopmax('zset')
        db.delete('zset')
        with TimeCheck('save zset to redis cluster', 1):
            for key, val in tqdm(data.items()):
                rc.zadd('zset', {key: val})
        with TimeCheck('get zset from redis cluster', 1):
            for _ in tqdm(data):
                rc.zpopmax('zset')
        rc.delete('zset')
        