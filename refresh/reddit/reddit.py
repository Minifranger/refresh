import os
import logging
import praw
import boto3

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

try:
    logger.info('Retrieving reddit secrets')
    secret = {s.get('Name'): s.get('Value')
              for s in boto3.client('ssm').get_parameters(Names=[os.environ['REDDIT_CLIENT_ID'], os.environ['REDDIT_CLIENT_SECRET']],
                                                          WithDecryption=True).get('Parameters')}
except Exception as e:
    raise ValueError('Could not retrieve reddit secrets')

reddit = praw.Reddit(client_id=secret.get(os.environ['REDDIT_CLIENT_ID']),
                     client_secret=secret.get(os.environ['REDDIT_CLIENT_SECRET']),
                     user_agent='refresh')
