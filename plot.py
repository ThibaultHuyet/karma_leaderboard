from reddit_rankings import *
import praw
from pymongo import MongoClient
import pymongo
import datetime

# Settings file is created by the user
# Due to sensitive data, this is ignored by github
from settings import CI, CS, PW, UA, UN

def returnSorted(client, db, collection):
	subs, scores = [], []

	for post in collection.find({}, {"_id":1, "score":1}).sort("score", pymongo.DESCENDING):
		subs.append(str(post["_id"]))
		scores.append(str(post["score"]))

	return subs, scores

if __name__ == "__main__":
	reddit= praw.Reddit(client_id = CI,
	                    client_secret = CS,
	                    password = PW,
	                    user_agent = UA,
	                    username = UN
	                    )

	client = MongoClient()
	db = client.REDDIT_RANKINGS
	collection = db.karma_leaderboard

	posts = []
	subs = []
	ranking = {}

	subreddit = []
	scores = []

	posts, subs, ranking = check_database(client, db, collection)
	# posts, subs = add_to_collection(client, db, collection, posts, subs)
	subreddit, scores = returnSorted(client, db, collection)


	for _ in range(10):
		print(str(subreddit[_]) + ": " + str(scores[_]))