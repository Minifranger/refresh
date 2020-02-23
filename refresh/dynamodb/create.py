import os
import json
import logging
import boto3
from refresh.utils import DecimalEncoder, success, failure

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

client = boto3.resource('dynamodb')


def create(event, context):
    logger.info('event : {event}'.format(event=event))

    body = json.loads(event.get('body')) if isinstance(event.get('body'), str) else event.get('body')
    if not body.get('id'):
        return failure(code=400, body='You should provide a submission id to your payload')

    params = {
        'TableName': os.environ['REDDIT_TABLE'],
        'Item': {'id': body.get('id'),
                 'title': body.get('title'),
                 'content': body.get('content')}
    }

    logger.info('Creating items {id}'.format(id=body.get('id')))

    try:
        client.Table(params.get('TableName')).put_item(**params)
    except Exception as e:
        return failure(body=e)

    return success(body=json.dumps(params['Item'], cls=DecimalEncoder))
