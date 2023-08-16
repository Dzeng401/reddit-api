import praw

reddit = praw.Reddit(
    client_id="kiKAZSbJnL_BPMCNyhOHKw",
    client_secret= "1Z7i8dPCwkmwJHEr1NWUvkVQoWvO4A",
    redirect_uri = "https://youtube.com",
    user_agent = "user_reddit_api"
    )

print(reddit.auth.url(scopes=["identity"], state="...", implicit=True))


