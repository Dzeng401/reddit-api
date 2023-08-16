from flask import Blueprint, request, jsonify, redirect
from middleware.auth import signinPRAW
import time
import praw
import threading as thread

reddit_blueprint = Blueprint('reddit_blueprint', __name__)

@reddit_blueprint.route("/user", methods = ['GET'])
def userInfo():
    subreddit = request.args.get('subreddit')
    refresh_token = request.args.get('refresh_token')
    reddit = praw.Reddit(
        client_id="kiKAZSbJnL_BPMCNyhOHKw",
        client_secret= "1Z7i8dPCwkmwJHEr1NWUvkVQoWvO4A",
        refresh_token = refresh_token,
        user_agent = "user_reddit_api"
    )
    user = reddit.user.me()
    return jsonify({"user": user.name}), 200

@reddit_blueprint.route("/comments", methods = ['GET'])
@signinPRAW
def comments(reddit):
    data = request.get_json()
    subreddit = request.args.get('subreddit')
    comments = reddit.subreddit(subreddit)
    comment_list = []
    for i in comments.search(data['comment'], limit = int(data['limit'])):
        comment_list.append({
            "id": i.id,
            "author": i.author.name,
            "time": i.created_utc,
            "upvotes": i.score,
            "comment": i.title
        })
    print(comment_list)
    return jsonify({"comments": comment_list}), 200

@reddit_blueprint.route("/inbox", methods = ['GET'])
@signinPRAW
def inbox(reddit):
    data = request.get_json()
    inbox_list = []
    for item in reddit.inbox.all(limit = int(data['limit'])):
        inbox_list.append({
            'author': item.author.name,
            'id': item.id,
            'time': item.created_utc,
            'body': item.body,
            'subreddit': item.subreddit.name,
            'original_thread': item.submission.name
        })
        print(item.body)
    return jsonify({"success": inbox_list}), 200

@reddit_blueprint.route("/redditor", methods = ['GET'])
@signinPRAW
def redditor(reddit):
    redditor_name = request.args.get('redditor')
    redditor_instance = reddit.redditor(redditor_name)
    info = {
        "id": redditor_instance.id,
        'karma': redditor_instance.comment_karma,
        "subreddit_name": redditor_instance.subreddit['name'],
        "subreddit_title": redditor_instance.subreddit['title']
    }
    return jsonify({"redditor_info": info}), 200


@reddit_blueprint.route("/watchredditor", methods = ['GET'])
@signinPRAW
def watch_redditor(reddit):
    redditor_name = request.args.get('redditor')
    redditor_instance = reddit.redditor(redditor_name)
    data = request.get_json()
    t_sleep = data['time']
    comment_list = []

    def run_bot():
        for comment in redditor_instance.comments.new(limit = 5):
            comment_list.append(comment.body)
    
        for comment in redditor_instance.stream.comments():
            print(comment.body)

    timer = thread.Thread(target = run_bot)
    timer.start()
    time.sleep(int(t_sleep))
    return jsonify({"success": comment_list}), 200

@reddit_blueprint.route("/submissionreplybot", methods = ['GET'])
@signinPRAW
def submission_reply_bot(reddit):
    data = request.get_json()
    reply_text = data['reply_text']
    keywords = data['keywords']
    t_sleep = int(data["time"])
    print(keywords)
    subreddit = reddit.subreddit(request.args.get('subreddit'))
    
    def run_submission_bot():
        for submission in subreddit.stream.submissions():
            process_submission(submission)
    
    def process_submission(submission):
        normalized_title = submission.title.lower()
        for word in keywords:
            if word in normalized_title:
                comment = f"Replying to {submission.title} by author {submission.author}:\n{reply_text}"
                submission.reply(comment)
                break
    
    timer = thread.Thread(target = run_submission_bot)
    timer.start()
    time.sleep(t_sleep)
    return jsonify({"success": "success"}), 200

@reddit_blueprint.route("/submissionupvotebot", methods = ['GET'])
@signinPRAW
def submission_upvote_bot(reddit):
    data = request.get_json()
    reply_text = data['reply_text']
    keywords = data['keywords']
    t_sleep = int(data["time"])
    print(keywords)
    subreddit = reddit.subreddit(request.args.get('subreddit'))
    
    def run_submission_bot():
        for submission in subreddit.stream.submissions():
            for comments in submission.comments:
                process_comments(comments)
                
    
    def process_comments(comment):
        text = comment.body
        for word in keywords:
            if word in text:
                comment.upvote()
        for reply in comment.replies:
            for word in keywords:
                if word in reply.body:
                    reply.upvote()
    
    timer = thread.Thread(target = run_submission_bot)
    timer.start()
    time.sleep(t_sleep)
    return jsonify({"success": "success"}), 200
        

