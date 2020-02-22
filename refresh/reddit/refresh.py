import json
import logging
import boto3
from prawcore.exceptions import ResponseException
from refresh.utils import DecimalEncoder, success, failure
from refresh.reddit.reddit import REDDIT

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def refresh(event, context):
    logger.info('event : {event}'.format(event=event))

    body = json.loads(event.get('body'))
    for b in body:
        print(b)
        print({"pathParameters": {"subreddit": b.get('subreddit')},
               "queryStringParameters": {"limit": b.get('limit'), "comments_threshold": b.get('comments_threshold')}})
    # result = boto3.client('lambda').invoke(FunctionName='refresh-dev-hot', Payload=json.dumps({'name': 'test'}))
    # print(result)

    return
