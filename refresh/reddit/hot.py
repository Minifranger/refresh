import json
import logging
from prawcore.exceptions import NotFound
from refresh.utils import DecimalEncoder
from refresh.reddit.reddit import reddit

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def hot(event, context):
    logger.info('event : {event}'.format(event=event))

    subreddit = event.get('pathParameters').get('subreddit')
    if not subreddit:
        raise ValueError('You should provide a subreddit to your path parameters')

    logger.info('Getting hot items from {subreddit}'.format(subreddit=subreddit))

    try:
        hots = [submission for submission in reddit().subreddit(subreddit).hot(limit=event.get('limit', 20))
                if submission.num_comments > event.get('min_comments', 100)]
    except NotFound as e:
        return {"statusCode": e.response.status_code,
                "body": json.dumps("Subreddit {subreddit} doesn't exist".format(subreddit=subreddit))}
    except Exception as e:
        return {"statusCode": e.response.status_code, "body": json.dumps(str(e), cls=DecimalEncoder)}

    response = {
        "statusCode": 200,
        "body": json.dumps({s.name: dict(title=s.title, content=s.selftext) for s in hots}, cls=DecimalEncoder)
    }
    return response
