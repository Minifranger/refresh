import os
import json
import logging
import boto3
from refresh.utils import DecimalEncoder, success, failure

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

client = boto3.client('dynamodb')


def batch_get(event, context):
    logger.info('event : {event}'.format(event=event))

    body = json.loads(event.get('body')) if isinstance(event.get('body'), str) else event.get('body')

    params = {
        'RequestItems': {os.environ['REDDIT_TABLE']: {'Keys': body}}
    }

    logger.info('Getting items {id}'.format(id=', '.join([b.get('id').get('S') for b in body])))

    try:
        result = client.batch_get_item(**params)
        if result.get('UnprocessedKeys'):
            logger.info('Unprocessed keys {items}'.format(items=', '.join(result.get('UnprocessedKeys').keys())))
    except Exception as e:
        return failure(body=e)

    result = [{k: t.get(k).get('N') if t.get(k).get('N') else t.get(k).get('S')
               for k in t.keys()} for t in result.get('Responses').get(os.environ['REDDIT_TABLE'])]
    return success(body=json.dumps(result, cls=DecimalEncoder))
