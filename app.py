from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from blueprints.loginblueprint import login_blue_print
from blueprints.redditblueprint import reddit_blueprint
from middleware.auth import authenticate
from flask_cors import CORS
from databases.database import db
from databases.tables.user import User

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://admin:Performapal1!@reddit-sql.c28qlcyh5j6n.us-east-1.rds.amazonaws.com:3306/reddit_database"
db.init_app(app)
# db = SQLAlchemy(app)
# print(db)


@app.route("/foo", methods = ['GET'])
def intro():
    return jsonify({"error": "error"})

app.register_blueprint(login_blue_print)
app.register_blueprint(reddit_blueprint)

with app.app_context():
        db.create_all()

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug = True, port = 8080)