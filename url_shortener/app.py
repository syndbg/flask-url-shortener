from flask import Flask, request, jsonify
from flask.ext.mongoengine import MongoEngine, Q

from utils import apify, UrlEncoder


app = Flask(__name__)
app.config['SECRET_KEY'] = 'flaskangularmongo'
app.config['MONGODB_SETTINGS'] = {
    'db': 'url-shortener',
    'host': '127.0.0.1',
    'port': 27017
}
db = MongoEngine(app)
encoder = UrlEncoder()


@app.route('/')
def index():
    return 'insert JS frontend'


# API constants
DEFAULT_PAGE = 1
DEFAULT_PER_PAGE = 50


# API routes
@app.route('/api/urls/', methods=['GET, POST'])
def urls():
    method_type = request.method
    data = request.json

    if method_type == 'GET':
        page = data.get('page', DEFAULT_PAGE)
        per_page = data.get('per_page', DEFAULT_PER_PAGE)

        db_result = db.Url.objects.paginate(page=page, per_page=per_page)
        return jsonify([apify(r) for r in db_result]), 200
    else:
        pass


@app.route('/api/urls/<url>', methods=['GET', 'PUT', 'DELETE'])
def url_by_string(url):
    method_type = request.method

    db_result = db.Url.objects(Q(short_url=url) || Q(long_url=url))
    if method_type == 'GET':

    else:

    return 'hey'
