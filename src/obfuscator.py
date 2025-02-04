import boto3
from io import StringIO, BytesIO


def obfuscator(json_str: str) -> None:
    pass


def get_bucket_and_key_from_string(filename: str) -> tuple[str]:
    """Obtains bucket name and key name for file at given S3 address.

    Args:
        filename (str): address of file in S3 bucket
        eg. 's3://my_ingestion_bucket/new_data/file1.csv'

    Returns: bucket name and key name as a tuple.
        eg. 'my_ingestion_bucket', 'new_data/file1.csv'"""

    for i in range(5, len(filename)):
        if filename[i] == "/":
            break

    bucket = filename[5: i]
    key = filename[i + 1:]
    return bucket, key


def get_s3_object(bucket: str, key: str) -> str:
    """Gets body of given S3 object.

    Args:
        bucket(str): bucket name
        key(str): key name

    Returns: Body of the given file in string format."""

    client = boto3.client('s3')
    s3_object = client.get_object(
        Bucket=bucket,
        Key=key,
    )
    body = s3_object['Body'].read()
    return body.decode('utf-8')


def save_streaming_obj_to_s3(obj: StringIO, bucket: str, key: str) -> None:
    bytes_obj = BytesIO(obj.getvalue().encode('utf-8'))
    client = boto3.client('s3')
    client.put_object(
        Bucket=bucket,
        Body=bytes_obj,
        Key=key,
    )
