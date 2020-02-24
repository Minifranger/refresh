import os
import json
import logging
import boto3
from refresh.utils import DecimalEncoder, success, failure

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

client = boto3.client('lambda')


def batch_get(event, context):
    logger.info('event : {event}'.format(event=event))

    body = json.loads(event.get('body')) if isinstance(event.get('body'), str) else event.get('body')
    response = []

    logger.info('Getting items {id}'.format(id=', '.join([b.get('pathParameters').get('id') for b in body])))

    for b in body:
        id = b.get('pathParameters').get('id')
        try:
            result = client.invoke(FunctionName='refresh-dev-get', Payload=json.dumps(b))
            if result.get('FunctionError'):
                logger.warning('Could not get item {id} : {e}'.format(id=id, e=result.get('Payload').read()))
                continue
            else:
                logger.info('Retrieved item {id}'.format(id=id))
                response.append(json.loads(result.get('Payload').read()))
        except Exception as e:
            return failure(body=e)

    return success(body=json.dumps([json.loads(b.get('body')) for b in response]))
