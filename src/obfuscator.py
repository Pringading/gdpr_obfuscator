import boto3


def obfuscator(json_str: str) -> None:
    pass


def get_bucket_and_key_from_string(filename: str) -> tuple[str]:
    for i in range(5, len(filename)):
        if filename[i] == "/":
            break
    bucket = filename[5: i]
    key = filename[i + 1:]
    return bucket, key


def get_s3_object(bucket: str, key: str) -> str:
    client = boto3.client('s3')
    s3_object = client.get_object(
        Bucket=bucket,
        Key=key,
    )
    body = s3_object['Body'].read()
    return body.decode('utf-8')


def save_streaming_obj_to_s3(obj, bucket: str, key: str) -> None:
    pass
