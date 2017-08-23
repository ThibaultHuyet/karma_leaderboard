from reddit_rankings import *
from settings import un, ak

import pymongo
from pymongo import MongoClient

import plotly.plotly as py
import plotly.graph_objs as go

# Settings file is created by the user
# Due to sensitive data, this is ignored by github

if __name__ == "__main__":
	client = MongoClient()
	db = client.REDDIT_RANKINGS
	collection = db.karma_leaderboard

	subreddit = []
	scores = []

	subreddit, scores = returnSorted(client, db, collection)

	data = [go.Bar(
					x = subreddit,
					y = scores
					)]

	py.plot(data, filename='updated')