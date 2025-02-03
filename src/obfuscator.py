import boto3
from io import StringIO
from csv import DictReader

def access_csv(bucket: str, key: str) -> str:
    client = boto3.client('s3')
    s3_object = client.get_object(
        Bucket = bucket,
        Key = key,
    )
    body = s3_object['Body'].read()
    buffer = StringIO(body.decode('utf-8'))
    reader = DictReader(buffer)
    return list(reader)
