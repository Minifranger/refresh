import json
import logging
import boto3
from refresh.utils import success, failure

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

client = boto3.client('lambda')


def refresh_hot(event, context):
    logger.info('event : {event}'.format(event=event))

    body = json.loads(event.get('body')) if isinstance(event.get('body'), str) else event.get('body')
    # response = []

    logger.info('Getting batch hot submissions')

    try:
        response = client.invoke(FunctionName='refresh-dev-batch_hot', Payload=json.dumps(body))
        if response.get('FunctionError'):
            logger.warning('Could not retrieve batch hot submissions : {e}'.format(e=result.get('Payload').read()))
    except Exception as e:
        return failure(body=e)

    logger.info('Retrieved batch hot submissions')
    print(response)
    return response
