from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask import render_template
from api import Page, get_page_index
from datetime import datetime
import os
from IPython import embed

app = Flask(__name__, static_folder='client/dist')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/xuanxue'
app.jinja_env.variable_start_string = r'{['
app.jinja_env.variable_end_string = r']}'

CORS(app, resources={r'/*': {'origins': '*'}})

db = SQLAlchemy(app)

class Fu(db.Model):
    __tablename__ = 'shefu'
    idx = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.Date)
    question = db.Column(db.String(255))
    img_question = db.Column(db.String(255))
    img_answer = db.Column(db.String(255))
    answer = db.Column(db.String(255))
    source = db.Column(db.String(45))
    sender = db.Column(db.String(45))

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

@app.route('/vue_test/<path:filename>')
def serve_static(filename):
    return send_from_directory('static/vue_test', filename)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        print(os.path.exists(app.static_folder + '/' + path))
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

@app.route('/api/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')

# @app.route('/')
# def index():
#     fus = Fu.query.limit(10).all()
#     # print(data)
#     # embed()
#     return render_template('index.html', data=fus)

@app.route('/<path:fallback>')
def fallback(fallback):       # Vue Router 的 mode 为 'hash' 时可移除该方法
    if fallback.startswith('css/') or fallback.startswith('js/')\
            or fallback.startswith('img/') or fallback == 'favicon.ico':
        return app.send_static_file(fallback)
    else:
        return app.send_static_file('index.html')

@app.route('/manage/blogs2')
def get(*,page='1'):
    return {
        '__template__':'manage_blogs2.html',
        'page_index':get_page_index(page)
    }

@app.route('/search', methods=['GET'])
def search(request):
    keyword = request.args.get('keyword')
    source = request.args.get('source')

    # 根据keyword和source进行数据库查询，获取查询结果result

    return render_template('search.html', keyword=keyword, source=source, result=result)

@app.route('/test')
def test():
    fus = Fu.query.limit(10).all()
    print(fus[0].as_dict())
    json_result = jsonify([item.as_dict() for item in fus])
    print('json',json_result)
    # embed()
    # return render_template('test.html', data=fus)
    # response_object['books'] = json_result
    return json_result

@app.route('/test2', methods=['GET', 'POST'])
def test2():
    response_object = {'status': 'success'}
    print(request)
    if request.method == 'POST':
        post_data = request.get_json()
        BOOKS.append({
            'title': post_data.get('title'),
            'author': post_data.get('author'),
            'read': post_data.get('read')
        })
        response_object['message'] = 'Book added!'
    else:
        fus = Fu.query.limit(10).all()
        print(fus[0].as_dict())
        fus_list = [item.as_dict() for item in fus]
        response_object['fus'] = fus_list
    return jsonify(response_object)

@app.route('/api/fus')
def api_fus():
    page = request.args.get('page', 1, type=int)
    timefrom = datetime.strptime(request.args.get('from'), "%Y-%m-%dT%H:%M:%S.%fZ")
    timeto = datetime.strptime(request.args.get('to'), "%Y-%m-%dT%H:%M:%S.%fZ")
    print("page:", page)
    print("datetime:", timefrom, timeto)
    response_object = {'status': 'success'}
    page_index=get_page_index(page)
    total_count = Fu.query.filter(Fu.source.startswith("东乾")).filter(Fu.time.between(timefrom, timeto)).count()
    print("--------------total------------", total_count)
    p=Page(total_count,page_index)
    response_object['total'] = p.page_count

    fus = Fu.query.filter(Fu.source.startswith("东乾")).filter(Fu.time.between(timefrom, timeto)).order_by("time").offset(p.offset).limit(p.limit).all()
    fus_list = [item.as_dict() for item in fus]
    response_object['fus'] = fus_list
    if len(fus)>0:
        print(fus[0].as_dict())
    return jsonify(response_object)


@app.route('/api/search', methods=['POST'])
def search_fu():
    data = request.get_json()  # 获取 POST 请求的 JSON 数据

    keyword = data.get('keyword')
    source = data.get('source')
    print(keyword, source)
    # 执行查询操作，根据 keyword 和 source 进行查询
    # 假设返回的结果为 result，是一个列表
    result = Fu.query.limit(10).all()
    result_list = [item.serialize() for item in result]

    return jsonify(result=result_list)


############################################## test ################################

BOOKS = [
    {
        'title': 'On the Road',
        'author': 'Jack Kerouac',
        'read': True
    },
    {
        'title': 'Harry Potter and the Philosopher\'s Stone',
        'author': 'J. K. Rowling',
        'read': False
    },
    {
        'title': 'Green Eggs and Ham',
        'author': 'Dr. Seuss',
        'read': True
    }
]

# @app.route('/books', methods=['GET'])
# def all_books():
#     return jsonify({
#         'status': 'success',
#         'books': BOOKS
#     })

@app.route('/books', methods=['GET', 'POST'])
def all_books():
    response_object = {'status': 'success'}
    print(request)
    if request.method == 'POST':
        post_data = request.get_json()
        BOOKS.append({
            'title': post_data.get('title'),
            'author': post_data.get('author'),
            'read': post_data.get('read')
        })
        response_object['message'] = 'Book added!'
    else:
        response_object['books'] = BOOKS
    return jsonify(response_object)

if __name__ == '__main__':
    app.run()
