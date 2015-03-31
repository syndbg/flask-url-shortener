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
        output = [apify(r) for r in db_result]
        status_code = 200

    elif db.Url.has_all_required_fields(data):
        db_result = db.Url(**data)
        db.save()
        output = apify(db_result)
        status_code = 200
    return jsonify(output), status_code


@app.route('/api/urls/<url>', methods=['GET', 'PUT', 'DELETE'])
def url_by_string(url):
    method_type = request.method
    data = request.json

    db_result = db.Url.objects.get_or_404(Q(short_url=url) | Q(long_url=url))
    if method_type != 'GET' and db.Url.has_any_required_fields(data):
        if method_type == 'DELETE':
            output = apify(db_result)
            db_result.delete()
        else:
            db_result.update_fields(data)
            output = apify(db_result)
    else:
        output = apify(db_result)
    return jsonify(output), 200
