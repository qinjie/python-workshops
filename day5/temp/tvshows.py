# import mongo and flask
from pymongo import MongoClient
from flask import Flask, request
import re

# construct the connection string for mongo
username = ''
password = ''
conn_str = f'your url here'

# create a connection to Mongo
client = MongoClient(conn_str)
# get a reference to leisure database
db = client['leisure']
# get a reference to the tvshows collection
tvshows = db['tvshows']

# create Flask application
app = Flask(__name__)

@app.route('/tvshow/30', methods=['GET'])
def tvshow30():
    pred = { 'runtime': { '$lte': 30 }}

    with tvshows.find(pred) as cur:
        lis = ''
        for d in cur:
            lis += f'<li>{d["name"]}</li>'

        return f'<ul>{lis}</ul>'

# GET /search?q=abc123
@app.route('/search', methods=['GET'])
def search():
    # get the query string call q
    to_search = request.args.get('q')
    patt = re.compile(to_search, re.IGNORECASE)
    pred = { 'name': patt }

    # without the with/as
    cur = tvshows.find(pred)
    lis = ''
    for d in cur:
        url = d['url']
        name = d['name']
        lis += f'<li><a href="{url}">{name}</a></li>\n'
        #lis += f'<li>{d["name"]}</li>\n'

    # need to close the cursor, resource leak
    cur.close()

    return f'<ul>\n{lis}\n</ul>'

# start the Flask application, open a port
print('Opening port 3000...')
app.run(port=3000, debug=True)