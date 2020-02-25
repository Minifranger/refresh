import json
import logging
import boto3
from itertools import chain
from refresh.utils import success, failure, validate_params

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

client = boto3.client('lambda')


def batch_hot(event, context):
    logger.info('event : {event}'.format(event=event))
    body, = validate_params(body=event.get('body'))

    body = json.loads(body) if isinstance(body, str) else body
    response = []

    logger.info('Getting hot submissions from {subreddit}'.format(
        subreddit=', '.join([b.get('pathParameters').get('subreddit') for b in body])))

    for b in body:
        subreddit = b.get('pathParameters').get('subreddit')
        try:
            result = client.invoke(FunctionName='refresh-dev-hot', Payload=json.dumps(b))
            if result.get('FunctionError'):
                logger.warning('Could not retrieve hot submissions from {subreddit} : {e}'.format(subreddit=subreddit,
                                                                                                  e=result.get(
                                                                                                      'Payload').read()))
                continue
            else:
                logger.info('Retrieved hot submissions from {subreddit}'.format(subreddit=subreddit))
                response.append(json.loads(result.get('Payload').read()))
        except Exception as e:
            return failure(body=e)

    return success(body=json.dumps(list(chain(*[json.loads(b.get('body')) for b in response]))))
