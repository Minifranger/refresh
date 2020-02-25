import json
import logging
import boto3
from refresh.utils import success, failure, validate_params

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

client = boto3.client('lambda')


def batch_create(event, context):
    logger.info('event : {event}'.format(event=event))
    body, = validate_params(body=event.get('body'))

    body = json.loads(body) if isinstance(body, str) else body
    response = []

    logger.info('Creating items {id}'.format(id=', '.join([b.get('id') for b in body])))

    for b in body:
        id = b.get('id')
        try:
            result = client.invoke(FunctionName='refresh-dev-create', Payload=json.dumps({'body': b}))
            if result.get('FunctionError'):
                logger.warning('Could not create item {id} : {e}'.format(id=id, e=result.get('Payload').read()))
                continue
            else:
                logger.info('Created item {id}'.format(id=id))
                response.append(json.loads(result.get('Payload').read()))
        except Exception as e:
            return failure(body=e)

    return success(body=json.dumps([json.loads(b.get('body')) for b in response]))
