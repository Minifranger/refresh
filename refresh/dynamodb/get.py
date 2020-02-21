import os
import json
import logging
from refresh.utils import DecimalEncoder, dynamodb_table

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def get(event, context):
    logger.info('event : {event}'.format(event=event))

    id = event.get('pathParameters').get('id')
    if not id:
        raise ValueError('You should provide a name to your path parameters')

    params = {
        'TableName': os.environ['REDDIT_TABLE'],
        'Key': {'id': id}
    }

    logger.info('Getting items {name}'.format(name=id))
    result = dynamodb_table(**params).get_item(**params)
    logger.info('Response {code}'.format(code=result.get('ResponseMetadata').get('HTTPStatusCode')))

    response = {
        "statusCode": result.get('ResponseMetadata').get('HTTPStatusCode'),
        "body": json.dumps(result.get('Item'), cls=DecimalEncoder)
    }
    return response

