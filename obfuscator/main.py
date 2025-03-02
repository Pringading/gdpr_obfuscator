"""obfuscator function and helper functions that can be used for any file type.
"""

import boto3
import json
import logging
from io import StringIO, BytesIO
from .csv_utils import (
    object_body_to_list,
    obfuscate_fields,
    list_to_csv_streaming_object,
)
from .exceptions import (
    NoFileToObfuscate,
    InvalidFileToObfuscate,
    NoPIIFields,
)


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def obfuscator(json_str: str) -> BytesIO:
    """Obfuscates file specified in json_str and returns as a Bytes object.

    Args: json_str(json string) with following keys:
        "file_to_obfuscate": s3 path to the file to be obfuscated.
        "pii_fields": fields to be obfuscated

    Accesses file_to_obfuscate and returns obfuscated csv Bytes object.

    Example:
        when invoked with the following json string:
        {
            "file_to_obfuscate": "s3://my_ingestion_bucket/new_data/file1.csv",
            "pii_fields": ["name", "email_address"]
        }

        new file will be saved here:
            "s3://my_ingestion_bucket/obfuscated/new_data/file1.csv"

        in the returned object all data on 'name' and 'email' fields will
        appear as:
            ***

        fields not included will be identical.
    """

    request = json.loads(json_str)

    if 'file_to_obfuscate' not in request:
        logger.error('Unable to process. Please provide file_to_obfuscate')
        raise NoFileToObfuscate

    if 'pii_fields' not in request:
        logger.error('Unable to process. Please provide pii_fields')
        raise NoPIIFields

    bucket, key, _ = get_bucket_and_key_from_string(
        request["file_to_obfuscate"]
    )
    obj_body = get_s3_object(bucket, key)
    data = object_body_to_list(obj_body)
    obfuscated_data = obfuscate_fields(data, request["pii_fields"])
    obj = list_to_csv_streaming_object(obfuscated_data)
    bytes_obj = BytesIO(obj.getvalue().encode("utf-8"))  # convert to Byte obj
    return bytes_obj


def get_bucket_and_key_from_string(filename: str) -> tuple[str]:
    """Obtains bucket name and key name for file at given S3 address.

    Args:
        filename (str): address of file in S3 bucket
        eg. 's3://my_ingestion_bucket/new_data/file1.csv'

    Returns: bucket name, key name and extension as a tuple.
        eg. ('my_ingestion_bucket', 'new_data/file1.csv', 'csv')"""

    # raise error if not s3 location
    if filename[:5] != 's3://':
        logger.error(
            'Unable to process. file_to_obfuscate should start with s3://'
        )
        raise InvalidFileToObfuscate

    # find where the keyname starts
    for key_start in range(5, len(filename)):
        if filename[key_start] == '/':
            break

    # raise error if '/' not found so no keyname
    if key_start == len(filename) - 1:
        logging.error('Unable to process. Invalid file_to_obfuscate.')
        raise InvalidFileToObfuscate

    # assign bucket & key variables
    bucket = filename[5:key_start]
    key = filename[key_start + 1:]

    # find where the file extension starts
    ext_start = len(filename) - 1
    while ext_start > key_start:
        ext_start -= 1
        if filename[ext_start] == '.':
            break

    extension = filename[ext_start + 1:].lower()

    if extension not in ['csv']:
        logging.error(
            f'Unable to process. Files with the extension {extension}' +
            ' are currently not supported.'
        )
        raise InvalidFileToObfuscate

    return bucket, key, extension


def get_s3_object(bucket: str, key: str) -> str:
    """Gets body of given S3 object.

    Args:
        bucket(str): bucket name
        key(str): key name

    Returns: Body of the given file in string format."""

    client = boto3.client("s3")
    s3_object = client.get_object(
        Bucket=bucket,
        Key=key,
    )
    body = s3_object["Body"].read()
    return body.decode("utf-8")


def save_streaming_obj_to_s3(obj: StringIO, bucket: str, key: str) -> None:
    """Saves streaming object as a file in S3 bucket.

    Args:
        obj (StringIO): Streaming object with data to be written to S3.
        bucket (str): name of bucket to be written to
        key (str): name of the key to save the file to."""

    bytes_obj = BytesIO(obj.getvalue().encode("utf-8"))  # convert to Byte obj
    client = boto3.client("s3")
    client.put_object(
        Bucket=bucket,
        Body=bytes_obj,
        Key=key,
    )
