import os
import logging
import praw
import boto3

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def reddit():
    names = [os.environ['REDDIT_CLIENT_ID'], os.environ['REDDIT_CLIENT_SECRET']]
    logger.info('Retrieving reddit secrets')
    secrets = {s.get('Name'): s.get('Value')
               for s in boto3.client('ssm').get_parameters(Names=names, WithDecryption=True).get('Parameters')}
    assert all(name in secrets for name in names)
    return praw.Reddit(client_id=secrets.get(os.environ['REDDIT_CLIENT_ID']),
                       client_secret=secrets.get(os.environ['REDDIT_CLIENT_SECRET']),
                       user_agent='refresh')


REDDIT = reddit()
