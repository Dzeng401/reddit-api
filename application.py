from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from blueprints.loginblueprint import login_blue_print
from blueprints.redditblueprint import reddit_blueprint
from middleware.auth import authenticate
from flask_cors import CORS
from databases.database import db
from databases.tables.user import User

application = Flask(__name__)
CORS(application)
application.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://admin:Performapal1!@reddit-sql.c28qlcyh5j6n.us-east-1.rds.amazonaws.com:3306/reddit_database"
db.init_app(application)
# db = SQLAlchemy(app)
# print(db)


@application.route("/foo", methods = ['GET'])
def intro():
    return jsonify({"error": "error"})

application.register_blueprint(login_blue_print)
application.register_blueprint(reddit_blueprint)

with application.app_context():
        db.create_all()

if __name__ == "__main__":
    with application.app_context():
        db.create_all()
    application.run(debug = True)