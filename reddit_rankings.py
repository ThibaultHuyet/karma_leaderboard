import praw
from settings import CI, CS, PW, UA, UN

reddit= praw.Reddit(client_id = CI,
                    client_secret = CS,
                    password = PW,
                    user_agent = UA,
                    username = UN
                    )

for submission in reddit.subreddit('all').hot(limit = 25):
    print(str(submission.subreddit) + ":\t" +
          str(submission.score) + ":\t" +
          str(submission.id))
