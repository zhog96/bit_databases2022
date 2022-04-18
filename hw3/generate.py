import json
import string
import random
from tqdm import tqdm


if __name__ == '__main__':
    with open('string.json', 'w') as f:
        f.write(''.join([random.choice(string.ascii_letters) for _ in tqdm(range(20_000_000))]))
    
    with open('hash.json', 'w') as f:
        data = {}
        for idx in tqdm(range(100_000)):
            data[f'key {idx}'] = f'value {idx}' * 10
        f.write(json.dumps(data))

    with open('list.json', 'w') as f:
        data = []
        for idx in tqdm(range(200_000)):
            data.append(f'value {idx // 3}' * 10)
        f.write(json.dumps(data))
    
    with open('score_set.json', 'w') as f:
        data = {}
        for idx in tqdm(range(1_000_000)):
            data[f'key {idx}'] = idx * random.randint(0, 9)
        f.write(json.dumps(data))
