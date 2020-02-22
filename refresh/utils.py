import decimal
import json


class DecimalEncoder(json.JSONEncoder):
    """ makes json serialize decimal (for boto3) """

    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return str(o)
        return super(DecimalEncoder, self).default(o)


def success(**kwargs):
    status_code, body = kwargs.get('status_code', 200), kwargs.get('body')
    return {"statusCode": status_code, "body": body}


def failure(**kwargs):
    status_code, body = kwargs.get('status_code', 500), kwargs.get('body')
    return {"statusCode": status_code, "body": body}
