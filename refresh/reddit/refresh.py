import json
import logging
import boto3
from prawcore.exceptions import ResponseException
from refresh.utils import DecimalEncoder, success, failure
from refresh.reddit.reddit import REDDIT

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

client = boto3.client('lambda')


def refresh(event, context):
    logger.info('event : {event}'.format(event=event))

    body = json.loads(event.get('body')) if isinstance(event.get('body'), str) else event.get('body')
    response = []

    logger.info('Invoking hot lambda')
    for b in body:
        try:
            result = client.invoke(FunctionName='refresh-dev-hot',
                                   Payload=json.dumps(hot_query(subreddit=b.get('subreddit'),
                                                                limit=b.get('limit'),
                                                                comments_threshold=b.get('comments_threshold'))))
            if result.get('FunctionError'):
                logger.warning(
                    'Could not retrieve hot submissions from {subreddit} : {e}'.format(subreddit=b.get('subreddit'),
                                                                                       e=result.get('Payload').read()))
                continue
            else:
                logger.info(result)
                response.append(result.get('Payload').read())
        except Exception as e:
            return failure(body=e)

    print(response)

    return


def hot_query(**kwargs):
    subreddit, limit, comments_threshold = kwargs.get('subreddit'), kwargs.get('limit'), kwargs.get(
        'comments_threshold')
    return {"pathParameters": {"subreddit": subreddit},
            "queryStringParameters": {"limit": limit, "comments_threshold": comments_threshold}}
