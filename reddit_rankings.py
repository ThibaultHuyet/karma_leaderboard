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

"""
Currently there is a problem in the add_to_collection function
It does not add new posts correctly under a subreddit.
It also does not properly update the score of each subreddit
"""

def add_to_collection(client, db, posts, checked, subs):

	"""
	This function adds posts to a database
	"""

	for submission in reddit.subreddit('all').hot(limit = 500):
		"""
		I need to add a conditional that prevents adding repeat posts
		However, under certain circumstances, these repeats should be updated
		"""
		if str(submission.subreddit) not in subs:
			post = {
					"_id" : str(submission.subreddit),
					"post": {
							"link_score" : int(submission.score),
							"post_id" : str(submission.id),
							"time" : datetime.datetime.utcnow()
							},
					"score" : int(submission.score) # <---- Something is wrong with this. 
													# I need to find a way to update this with each new subreddit
					}

			result = posts.insert_one(post).inserted_id

			subs.append(str(submission.subreddit))
			checked[str(submission.id)] = int(submission.score) 

		elif str(submission.subreddit) in subs and str(submission.id) not in checked:
			"""
			Subreddit is in the list but submission is not
			This is where the update logic should occur
			It is needed to update the posts in the subreddit area
			"""
			posts.update_one({"_id" : str(submission.subreddit)},
							{'$set':{
									"post.post_id" : str(submission.id),
									"post.link_score" : int(submission.score),
									"post.time" : datetime.datetime.utcnow()
									}
							},
							upsert = False)

			# Take a look at this part of the code as this is probably where the error is
			posts.update_one({"_id" : str(submission.subreddit)},
							{'$inc' : {'score' : +int(submission.score), "score":1}}
							)
			
			checked[str(submission.id)] = int(submission.score)

		else:
			"""
			The only situation left would be that the subreddit and post are in the database
			Thus, I do not care
			"""
			pass

	return checked, subs

def check_database(client, db, posts):

	"""
	This function returns a dictionary of every post in the database
	The dictionary is of the submission_id and the link_score
	The list is a list of all the subreddits
	"""

	d = {}
	l = []


	for post in posts.find({}, {"_id":1, "post.post_id":1, "post.link_score":1}):
		d[post["post"]["post_id"]] = post["post"]["link_score"]
		l.append(post["_id"])

	return d, l

client = MongoClient()
db = client.REDDIT_RANKINGS
posts = db.karma_leaderboard

checked = {}
subs = []

checked, subs = check_database(client, db, posts)
checked, subs = add_to_collection(client, db, posts, checked, subs)