import os
import json
import logging
import boto3
from refresh.utils import DecimalEncoder, success, failure, validate_params

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

client = boto3.resource('dynamodb')


def get(event, context):
    logger.info('event : {event}'.format(event=event))
    path, = validate_params(path=event.get('pathParameters'))

    id = path.get('id')
    if not id:
        return failure(code=400, body='You should provide a id to your path parameters')

    params = {
        'TableName': os.environ['REDDIT_TABLE'],
        'Key': {'id': id}
    }

    logger.info('Getting item {id}'.format(id=id))

    try:
        result = client.Table(params.get('TableName')).get_item(**params)
    except Exception as e:
        return failure(body=e)

    logger.info('Retrieved item {id}'.format(id=id))
    return success(body=json.dumps(result.get('Item'), cls=DecimalEncoder))
