import json
import logging
import boto3
from refresh.utils import success, failure, validate_params

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

client = boto3.client('lambda')


def refresh_hot(event, context):
    logger.info('event : {event}'.format(event=event))
    body, = validate_params(body=event.get('body'))

    body = json.loads(body) if isinstance(body, str) else body

    logger.info('Getting hot submissions')

    try:
        response = client.invoke(FunctionName='refresh-dev-batch_hot', Payload=json.dumps({'body': body}))
        if response.get('FunctionError'):
            logger.warning('Could not retrieve batch hot submissions : {e}'.format(e=response.get('Payload').read()))
    except Exception as e:
        return failure(body=e)

    logger.info('Retrieved hot submissions')

    hot_submissions = json.loads(json.loads(response.get('Payload').read()).get('body'))
    """ prepare body for batch_get """
    body = [{'pathParameters': {'id': h.get('id')}} for h in hot_submissions]

    logger.info('Getting seen hot submissions')

    try:
        response = client.invoke(FunctionName='refresh-dev-batch_get', Payload=json.dumps({'body': body}))
        if response.get('FunctionError'):
            logger.warning('Could not get batch items : {e}'.format(e=response.get('Payload').read()))
    except Exception as e:
        return failure(body=e)

    logger.info('Retrieved seen hot submissions')

    hot_submissions_seen = json.loads(json.loads(response.get('Payload').read()).get('body'))

    """ prepare body for batch_create """
    body = [d for d in hot_submissions if d not in hot_submissions_seen]

    logger.info('Creating not seen hot submissions')

    try:
        response = client.invoke(FunctionName='refresh-dev-batch_create', Payload=json.dumps({'body': body}))
        if response.get('FunctionError'):
            logger.warning('Could not create batch items : {e}'.format(e=response.get('Payload').read()))
    except Exception as e:
        return failure(body=e)

    logger.info('Created not seen hot submissions')

    return success(body=json.loads(response.get('Payload').read()).get('body'))
