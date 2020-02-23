import os
import json
import logging
import boto3
from refresh.utils import DecimalEncoder, success, failure

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

client = boto3.resource('dynamodb')


def batch_get(event, context):
    logger.info('event : {event}'.format(event=event))

    body = json.loads(event.get('body')) if isinstance(event.get('body'), str) else event.get('body')
    # id = event.get('pathParameters').get('id')
    # if not id:
    #     return failure(code=400, body='You should provide a name to your path parameters')
    print(body)
    params = {
        os.environ['REDDIT_TABLE']: {'Keys': body}
    }

    logger.info('Getting items {id}'.format(
        id=', '.join([b.get('id') for b in body])))

    try:
        result = client.Table(params.get('TableName')).batch_get_item()(**params)
        print(result)
    except Exception as e:
        return failure(body=e)

    return success(body=json.dumps(result.get('Item'), cls=DecimalEncoder))
