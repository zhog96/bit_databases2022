const express = require('express')
var r = require('rethinkdb')
const app = express()
const port = 3000

var conn
r.connect({host: 'localhost', db: 'test'}).then(res => {conn = res})

app.get('/', (req, res) => {
    r.table('game').orderBy({index: r.desc('score')}).limit(3).changes().run(conn, function(err, cursor) {
        cursor.each(console.log);
    });
})

app.listen(port, () => {
  console.log(`Example app listening on port ${port}`)
})