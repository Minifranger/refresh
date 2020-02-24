import json
import logging
from prawcore.exceptions import ResponseException
from refresh.utils import success, failure
from refresh.reddit.reddit import REDDIT

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def hot(event, context):
    logger.info('event : {event}'.format(event=event))

    subreddit = event.get('pathParameters').get('subreddit')
    query_parameters = event.get('queryStringParameters', dict())
    if not subreddit:
        return failure(code=400, body='You should provide a subreddit to your path parameters')

    logger.info('Getting hot submissions from {subreddit}'.format(subreddit=subreddit))

    try:
        response = [submission for submission in REDDIT.subreddit(subreddit).hot(limit=query_parameters.get('limit', 20))
                if submission.num_comments > query_parameters.get('comments_threshold', 50)]
    except ResponseException as e:
        return failure(code=e.response.status_code, body=e)
    except Exception as e:
        return failure(body=e)

    logger.info('Retrieved hot submissions from {subreddit}'.format(subreddit=subreddit))
    return success(body=json.dumps([dict(subreddit=subreddit, id=s.id, title=s.title) for s in response]))
