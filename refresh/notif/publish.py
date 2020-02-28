import os
import json
import logging
import boto3
from refresh.utils import DecimalEncoder, success, failure, validate_params

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

client = boto3.client('sns')


def publish(event, context):
    logger.info('event : {event}'.format(event=event))
    body, = validate_params(body=event.get('body'))

    body = json.loads(body) if isinstance(body, str) else body
    if not body.get('message'):
        return failure(code=400, body='You should provide a message to your payload')

    params = {
        'TopicArn': os.environ['REDDIT_TOPIC'],
        'Subject': body.get('subject', 'refresh'),
        'Message': body.get('message')
    }

    logger.info('Publishing message to {topic}'.format(topic=params.get('TopicArn')))

    try:
        response = client.publish(**params)
    except Exception as e:
        return failure(body=e)

    logger.info('Published message to {topic}'.format(topic=params.get('TopicArn')))
    return success(body=json.dumps(response.get('MessageId')))
