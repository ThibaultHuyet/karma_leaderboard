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

	"""
	This function adds posts to a database
	"""

	for submission in reddit.subreddit('all').hot(limit = 50):
		post = {
				"subreddit" : str(submission.subreddit),
				"link_score" : int(submission.score),
				"post_id" : str(submission.id),
				"time" : datetime.datetime.utcnow()
				}
		post_id = posts.insert_one(post).inserted_id

def check_database(client, db, posts):

	"""
	This function returns a dictionary of every post in the database
	The dictionary is of the submission_id and the link_score
	"""

	d = {}

	for post in posts.find({}, {"post_id":1, "_id":0, "link_score":1}):
		d[post["post_id"]] = post["link_score"]

	return d

client = MongoClient()
db = client.REDDIT_RANKINGS
posts = db.karma_leaderboard

# add_to_collection(client, db, posts)

checked = check_database(client, db, posts)