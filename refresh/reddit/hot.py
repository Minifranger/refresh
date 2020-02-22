import json
import logging
from prawcore.exceptions import ResponseException
from refresh.utils import DecimalEncoder, success, failure
from refresh.reddit.reddit import REDDIT

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def hot(event, context):
    logger.info('event : {event}'.format(event=event))

    subreddit = event.get('pathParameters').get('subreddit')
    if not subreddit:
        return failure(code=400, body='You should provide a subreddit to your path parameters')

    logger.info('Getting hot items from {subreddit}'.format(subreddit=subreddit))

    try:
        hots = [submission for submission in REDDIT.subreddit(subreddit).hot(limit=event.get('limit', 20))
                if submission.num_comments > event.get('min_comments', 100)]
    except ResponseException as e:
        return failure(code=e.response.status_code, body=e)
    except Exception as e:
        return failure(body=e)

    return success(body=json.dumps([dict(id=s.id, title=s.title, content=s.selftext) for s in hots], cls=DecimalEncoder))
