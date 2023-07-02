from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import render_template

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/xuanxue'

db = SQLAlchemy(app)

class Fu(db.Model):
    __tablename__ = 'shefu'
    idx = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.Date)
    description = db.Column(db.String(255))
    img_question = db.Column(db.String(255))
    img_answer = db.Column(db.String(255))
    source = db.Column(db.String(45))

def index():
    data = Fu.query.all()
    print(data)

index()