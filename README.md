# Reddit Bot REST API

## Tech Stack
- Flask
- AWS RDS
- Python PRAW API
- Elastic Beanstalk

## API Endpoints

**http://zengreddit.us-east-1.elasticbeanstalk.com/login**
- Allows user to retrieve authentication url
```
// body params
{
 username: "yourusername",
 password: "yourpassword
}
```

**http://zengreddit.us-east-1.elasticbeanstalk.com/user/?subreddit={}&refresh_token={}**
- Allows you to retrieve user info


**http://zengreddit.us-east-1.elasticbeanstalk.com/comments/?subreddit={}&refresh_token={}**
- Allows you to retrieve user's recent comments

**http://zengreddit.us-east-1.elasticbeanstalk.com/redditors/?refresh_token={}&redditor={}**
- Allows you to retrieve other redditor's info

**http://zengreddit.us-east-1.elasticbeanstalk.com/watchredditor/?refresh_token={}&redditor={}**
- Runs stream for x amount of time to listen on other user's accounts for updates
```
// body params
{
 time: "10" // amount of time to run bot
}
```

**http://zengreddit.us-east-1.elasticbeanstalk.com/submissionreplybot?subreddit={}**
- Runs stream for x amount of time on subreddit to listen for keywords on new comments and posts and responds with reply text
```
// body params
{
 time: "10" // amount of time to run bot
 reply_text: "x" // what you want to reply with
 keywords: "x" // list of keywords to listen to
}
```

**http://zengreddit.us-east-1.elasticbeanstalk.com/submissionupbotebot?subreddit={}**
- Runs stream for x amount of time on subreddit to listen for keywords on new comments and posts and upvotes them
```
// body params
{
 time: "10" // amount of time to run bot
 reply_text: "x" // what you want to reply with
 keywords: "x" // list of keywords to listen to
}
```








