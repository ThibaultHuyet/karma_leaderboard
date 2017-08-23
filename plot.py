from reddit_rankings import *
import praw
import pymongo
import datetime

# Settings file is created by the user
# Due to sensitive data, this is ignored by github
from settings import CI, CS, PW, UA, UN

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

	subreddit = []
	scores = []

	subreddit, scores = returnSorted(client, db, collection)


	for _ in range(10):
		print(str(subreddit[_]) + ": " + str(scores[_]))