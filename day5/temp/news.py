# import libs
from flask import Flask
import requests

# change this if you want to bind to a different port
PORT = 8080
NEWS_URL = 'https://newsapi.org/v2/top-headlines'
API_KEY = ''

"""
def is_error(status_code):
    return (status_code < 200) or (status_code > 399)
"""

# lambda - a one line function which returns a value
is_error = lambda status_code: (status_code < 200) or (status_code > 399)

def get_news(category, country, apiKey):
    # construct the query string
    query = { 'country': country, 'category': category, 'apiKey': apiKey, 'pageSize': 5 }

    #make the request
    resp = requests.get(NEWS_URL, params=query)
    # status code is between 200 and 399
    if is_error(resp.status_code):
        # use a tuple to return multiple values
        return ([], resp.status_code)

    # no error, extract the relevant fields
    result = resp.json()
    articles = []
    for d in result['articles']:
        articles.append({
            'title': d['title'],
            'urlToImage': d['urlToImage'],
            'description': d['description'],
            'url': d['url']
        })

    # return the result
    return (articles, resp.status_code)

def mk_html(article):
    title = article['title']
    urlToImage = article['urlToImage']
    description = article['description']
    url = article['url']
    return f'''
                <h2>{title}</h2>
                <div><img src="{urlToImage}" width="150px"></div>
                <p>{description}</p>
                <a href="{url}">Go to article</a>
            '''

# create a flask application
app = Flask(__name__)

# route
# GET /singapore - static route
@app.route('/singapore', methods=['GET'])
def news_singapore():
    result = ""
    # ([], status_code) 
    # destructuring where the return result of a tuple from a function
    # is broken up and assigned to different variables
    articles, status_code = get_news('general', 'sg', API_KEY)
    # check for error
    if not is_error(status_code):
        result += '<h1>General</h1>'
        for a in articles:
            result += mk_html(a)

    articles, status_code = get_news('sports', 'sg', API_KEY)
    if not is_error(status_code):
        result += '<h1>Sports</h1>'
        for a in articles:
            result += mk_html(a)

    return result

# dynamic route
# GET /news/us/sports
@app.route('/news/<country>/<category>', methods=['GET'])
def news(category, country):
    result = ""
    # ([], status_code) 
    # destructuring where the return result of a tuple from a function
    # is broken up and assigned to different variables
    articles, status_code = get_news(category, country, API_KEY)
    # check for error
    if not is_error(status_code):
        result += f'<h1>{ category }</h1>'
        for a in articles:
            result += mk_html(a)

    return result

# GET /
@app.route('/', methods=['GET'])
def index():
    return f'''
        <h1>Headline News</h1>
        <h2><a href="/news/sg/general">Singapore General</a></h2>
        <h2><a href="/news/sg/sports">Singapore Sports</a></h2>
        <h2><a href="/news/sg/entertainment">Singapore Entertainment</a></h2>
        <h2><a href="/news/sg/science">Singapore Science</a></h2>
        <h2><a href="/news/sg/technology">Singapore Technology</a></h2>
        <h2><a href="/news/sg/health">Singapore Health</a></h2>
        <h2><a href="/news/sg/business">Singapore Business</a></h2>
    '''

# start the server in debug mode
# debug=True will restart the server automatically 
# when the file is updated
print('Starting News Server')
app.run(port=PORT, debug=True)