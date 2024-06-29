from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# MySQLデータベースのURI設定
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://user:password@db/mydatabase'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = app.config['SECRET_KEY']

db = SQLAlchemy(app)

# モデルのインポート
from app.models import Problem, Submission, Answer

# ルートのインポート
from app import routes
