import json
import logging
from refresh.utils import DecimalEncoder, dynamodb_table

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def get(event, context):
    logger.info('event : {event}'.format(event=event))

    name = event.get('pathParameters').get('name')
    if not name:
        raise ValueError('You should provide a name to your path parameters')

    params = {
        'TableName': 'seen-reddit-submission',
        'Key': {'name': name}
    }

    logger.info('Getting items {name}'.format(name=name))
    result = dynamodb_table(**params).get_item(**params)
    logger.info('Response {code}'.format(code=result.get('ResponseMetadata').get('HTTPStatusCode')))

    response = {
        "statusCode": result.get('ResponseMetadata').get('HTTPStatusCode'),
        "body": json.dumps(result.get('Item'), cls=DecimalEncoder)
    }
    return response

