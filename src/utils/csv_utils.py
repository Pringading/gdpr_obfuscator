import boto3
from io import StringIO
from csv import DictReader


def access_csv(bucket: str, key: str) -> list[dict]:
    """Function retrieves data from csv file in S3 bucket.

    Args:
        bucket(str): name of s3 bucket
        key(str): the key where the csv file is located

    Returns: data from the csv file as a list of dicitonaries."""

    client = boto3.client('s3')
    s3_object = client.get_object(
        Bucket=bucket,
        Key=key,
    )
    body = s3_object['Body'].read()
    buffer = StringIO(body.decode('utf-8'))
    reader = DictReader(buffer)
    return list(reader)


def obfuscate_fields(rows: list[dict], fields: list[str]) -> list[dict]:
    pass


def list_to_csv_streaming_object():
    pass
