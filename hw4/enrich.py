from rethinkdb import RethinkDB
import names
from random import randint
from tqdm import tqdm

r = RethinkDB()

r.connect( "localhost", 28015).repl()
r.db("test").table_create("users").run()

name = [names.get_full_name() for _ in tqdm(range(1000))]
for _ in tqdm(range(100)):
    data = []
    for idx in range(10000):
        data.append({ "name": name[idx % 1000], "info": { "age": randint(0, 100), "height": randint(150, 220) } })
    r.table("users").insert(data).run()
