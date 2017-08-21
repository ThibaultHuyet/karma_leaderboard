import praw
from pymongo import MongoClient
import datetime

# Settings file is created by the user
# Due to sensitive data, this is ignored by github
from settings import CI, CS, PW, UA, UN

reddit= praw.Reddit(client_id = CI,
                    client_secret = CS,
                    password = PW,
                    user_agent = UA,
                    username = UN
                    )

def add_to_collection(client, db, posts):
	for submission in reddit.subreddit('all').hot(limit = 50):
		post = {
				"subreddit" : str(submission.subreddit),
				"link_score" : int(submission.score),
				"post_id" : str(submission.id),
				"time" : datetime.datetime.utcnow()
				}
		post_id = posts.insert_one(post).inserted_id


client = MongoClient()
db = client.REDDIT_RANKINGS
posts = db.karma_leaderboard

add_to_collection(client, db, posts)