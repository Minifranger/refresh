import json
import logging
import praw

logger = logging.getLogger(__name__)


def get(event, context):
    logger.info('event : {event}'.format(event=event))

    reddit = praw.Reddit(client_id='QWqKrzibZE-P8Q',
                         client_secret='mI81L4VkzZfA5IpO7Yru0eTRpf0',
                         user_agent='my user agent')

    for submission in reddit.subreddit('learnpython').hot(limit=10):
        print(reddit.subreddit('learnpython').hot(limit=10))
        print(type(submission))
        print(submission.title)

    response = {
        "statusCode": 200,
        "body": json.dumps('test')
    }

    return response
