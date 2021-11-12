# import Flask
# flask - module, Flask - is the class in the module
from flask import Flask
from datetime import datetime

# create a web server/web application
app = Flask(__name__) 

# define a function to return the current time
# decorator to map GET /time request to current_time()
# the decorator starts with a @
@app.route('/time', methods=['GET'])
def current_time():
    now = datetime.now()
    curr_time = str(now)
    return f'<h2>Current time is {curr_time}</h2>'

@app.route('/joke', methods=['GET'])
def joke():
    return '<h2>Why does the cat cross the road</h2>'

# workshop
# GET /tvshows/30
# return the tvshow name as a HTML list
# return a list of all the tvshows that the runtime is less than or equals to 30 mins
# pred = { 'runtime': { '$lte': 30 }}

# open a port 3000 on your machine/notebook
# this is for incoming browser request
app.run(port=3000)