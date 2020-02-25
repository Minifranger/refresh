import json
import logging
import boto3
from refresh.utils import success, failure, validate_params

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

client = boto3.client('lambda')


def batch_get(event, context):
    logger.info('event : {event}'.format(event=event))
    body, = validate_params(body=event.get('body'))

    body = json.loads(body) if isinstance(body, str) else body
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

    """ remove duplicates and empty items """
    response = list({v['body']: v for v in [r for r in response if r.get('statusCode') == 200]}.values())
    return success(body=json.dumps([json.loads(b.get('body')) for b in response]))
