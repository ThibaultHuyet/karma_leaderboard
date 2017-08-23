from reddit_rankings import *
import praw
from pymongo import MongoClient
import datetime

# Settings file is created by the user
# Due to sensitive data, this is ignored by github
from settings import CI, CS, PW, UA, UN

def filterDictionary(d):
	"""
	Takes in a dictionary and returns a list with the top 10 subreddits
	in terms of karma count
	the sub associated with subs[0] should have the karma count of scores[0]
	"""

	subs = []
	scores = []

	for k, v in d.items():
		if len(subs) < 10 and len(scores) < 10:
			subs.append(k)
			scores.append(v)

		if len(subs) >= 10:
			for _ in range(10):
				if v > scores[_] and k not in subs:
					subs.pop(_)
					scores.pop(_)

					subs.append(k)
					scores.append(v)

	subs, scores = sort(subs, scores)

	return subs, scores

def sort(subs, scores):
	"""
	This quicksort algorithm sorts the scores list and sorts subs
	to make sure subs[0] and scores[0] refer to the same subreddit
	"""

	temSS = list(zip(subs, scores))
	temSS = sorted(temSS, key = lambda x: x[1])
	subs, scores = zip(*temSS)
	
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
	subreddit, scores = filterDictionary(ranking)


	for _ in range(10):
		print(str(subreddit[_]) + ": " + str(scores[_]))