import praw
from pymongo import MongoClient
import datetime

# Settings file is created by the user
# Due to sensitive data, this is ignored by github
from settings import CI, CS, PW, UA, UN

"""reddit= praw.Reddit(client_id = CI,
                    client_secret = CS,
                    password = PW,
                    user_agent = UA,
                    username = UN
                    )"""

def add_to_collection(client, db, collection, posts, subs):

	"""
	This function adds posts to a database
	It also updates lists that it takes in
	"""

	for submission in reddit.subreddit('all').hot(limit = 500):
		"""
		I need to add a conditional that prevents adding repeat posts
		However, under certain circumstances, these repeats should be updated
		"""

		if str(submission.subreddit) not in subs:
			post = {
					"_id" : str(submission.subreddit),
					"post": [{
							"_id" : str(submission.id),
							"link_score" : int(submission.score),
							"time" : datetime.datetime.utcnow()
							}],
					"score" : int(submission.score)
					}

			result = collection.insert_one(post).inserted_id

			subs.append(str(submission.subreddit))
			posts.append(submission.id)
			

		elif str(submission.subreddit) in subs and str(submission.id) not in posts:
			"""
			Subreddit is in the list but submission is not
			This is where the update logic should occur
			It is needed to update the posts in the subreddit area
			"""
			collection.update_one({"_id" : str(submission.subreddit)},
									{'$addToSet':
										{ "post" :
											{'$each' :
											[{"_id" : str(submission.id),
											"link_score" : int(submission.score),
											"time" : datetime.datetime.utcnow() }]
											}
										}
									}
								)
					
			collection.update_one({"_id" : str(submission.subreddit)},
									{'$inc' : {'score' : +int(submission.score)}}
									)

			posts.append(submission.id)
					
		else:
			"""
			The only situation left would be that the subreddit and post are in the database
			Thus, I do not care
			"""
			pass

	return posts, subs

def check_database(client, db, collection):

	"""
	This function returns two lists.
	one list has a list of all submissions
	other has a list of all subreddits
	"""

	posts = []
	subs = []
	ranking = {}

	for post in collection.find({}, {"_id":1, "post":1, "score":1}):
		subs.append(str(post["_id"]))
		ranking[str(post["_id"])] = int(post["score"])
		for _ in post['post']:
			k = str(_["_id"])
			posts.append(k)

	return posts, subs, ranking


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

	posts, subs, ranking = check_database(client, db, collection)
	posts, subs = add_to_collection(client, db, collection, posts, subs)