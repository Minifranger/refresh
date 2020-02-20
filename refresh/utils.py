import decimal
import json
import boto3


class DecimalEncoder(json.JSONEncoder):
    """ makes json serialize decimal (for boto3) """
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return str(o)
        return super(DecimalEncoder, self).default(o)


def dynamodb_table(**kwargs):
    return boto3.resource('dynamodb').Table(kwargs.get('TableName', None))
