import os
import json
import logging
import boto3
from refresh.utils import DecimalEncoder, success, failure

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def get(event, context):
    logger.info('event : {event}'.format(event=event))

    id = event.get('pathParameters').get('id')
    if not id:
        return failure(code=400, body='You should provide a name to your path parameters')

    params = {
        'TableName': os.environ['REDDIT_TABLE'],
        'Key': {'id': id}
    }

    logger.info('Getting items {id}'.format(id=id))

    try:
        result = boto3.resource('dynamodb').Table(params.get('TableName')).get_item(**params)
    except Exception as e:
        return failure(body=e)

    return success(body=json.dumps(result.get('Item'), cls=DecimalEncoder))
