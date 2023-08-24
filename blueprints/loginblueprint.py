from flask import Blueprint, request, jsonify, redirect
from databases.database import db
from databases.tables.user import User
import webbrowser
import praw

reddit = praw.Reddit(
    client_id="kiKAZSbJnL_BPMCNyhOHKw",
    client_secret= "1Z7i8dPCwkmwJHEr1NWUvkVQoWvO4A",
    redirect_uri = "http://zengreddit.us-east-1.elasticbeanstalk.com/redirect",
    user_agent = "user_reddit_api"
)

login_blue_print = Blueprint('login_blue_print', __name__)

@login_blue_print.route("/login", methods = ['GET'])
def get_access_token():
    data = request.get_json()
    print(data)
    username = data['username']
    password = data['password']
    if (not username or not password):
        return jsonify({'error': "error"}), 400
    url = reddit.auth.url(scopes=["identity", "account", "edit", "history","privatemessages", "read", "submit"], state="...", duration="permanent")
    # webbrowser.open_new_tab(url)
    return jsonify({"url": url}), 200

@login_blue_print.route("/redirect", methods = ["GET"])
def redirect_route():
    try:
        code = request.args.get('code')
        request_token = reddit.auth.authorize(code)
        new_token = User(request_token)
        db.session.add(new_token)
        db.session.commit()
        return jsonify({'token': request_token}), 200
    except Exception as error:
        print(error)
        return jsonify({'error': "error"}), 400
    


