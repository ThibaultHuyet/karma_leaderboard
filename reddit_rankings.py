import praw

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
Submission id's is used to assure no duplicates
Submission score is the karma associated with the post
Submission subreddit is the subreddit the score goes towards
"""

for submission in reddit.subreddit('all').hot(limit = 25):
    print(str(submission.subreddit) + ":\t" +
          str(submission.score) + ":\t" +
          str(submission.id))
