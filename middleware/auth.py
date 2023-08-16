from functools import wraps
from flask import request, redirect, url_for, jsonify
import praw


def authenticate(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        headers = request.headers()
        if (not headers.get('Authorization')):
            return jsonify({"error": "error"}), 400
        return func(*args, **kwargs)
    return wrapper

def signinPRAW(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if (not request.args.get('refresh_token')):
            return jsonify({"error": "error"}), 400
        refresh_token = request.args.get('refresh_token')
        reddit = praw.Reddit(
            client_id="kiKAZSbJnL_BPMCNyhOHKw",
            client_secret= "1Z7i8dPCwkmwJHEr1NWUvkVQoWvO4A",
            refresh_token = refresh_token,
            user_agent = "user_reddit_api"
        )
        return func(reddit)
    return wrapper

