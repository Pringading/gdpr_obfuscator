import pytest
import boto3
import json
from time import time
from csv import DictReader
from io import StringIO
from src.utils.csv_utils import (
    list_to_csv_streaming_object,
    object_body_to_list,
)
from src.obfuscator import (
    obfuscator,
    get_bucket_and_key_from_string,
    get_s3_object,
    save_streaming_obj_to_s3,
)


class TestObfuscator:
    @pytest.mark.it('Adds obfuscated file to S3 Bucket')
    def test_adds_obfuscated_file(self, mock_s3_bucket):
        test_request = {
            "file_to_obfuscate": "s3://test-bucket/students.csv",
            "pii_fields": ["name", "email_address"]
        }
        test_bucket = "test-bucket"
        obfuscated_key = "obfuscated/students.csv"
        json_request = json.dumps(test_request)
        obfuscator(json_request)
        result_body = get_s3_object(test_bucket, obfuscated_key)
        result_list = object_body_to_list(result_body)
        for row in result_list:
            assert row["name"] == "***"
            assert row["email_address"] == "***"

    @pytest.mark.it('processes 1MB file in less than 1 minute')
    def test_takes_less_than_1_min(self, s3_bucket_1MB):
        test_request = {
            "file_to_obfuscate": "s3://test-bucket/movies.csv",
            "pii_fields": ["Title", "Director", "Writer"]
        }
        test_bucket = "test-bucket"
        obfuscated_key = "obfuscated/movies.csv"
        json_request = json.dumps(test_request)
        start = time()
        obfuscator(json_request)
        result_body = get_s3_object(test_bucket, obfuscated_key)
        result_list = object_body_to_list(result_body)
        for row in result_list:
            assert row["Title"] == "***"
            assert row["Director"] == "***"
            assert row["Writer"] == "***"
        end = time()
        assert end - start < 60


class TestGetBucketAndKeyFromString:
    """Testing get_bucket_and_key_from_string function in src/obfuscator.py"""

    @pytest.mark.it('Obtains bucket and key name from s3 address.')
    def test_returns_bucket_name(self):
        test_file = "s3://my_ingestion_bucket/new_data/file1.csv"
        expected_bucket = "my_ingestion_bucket"
        expected_key = "new_data/file1.csv"
        result = get_bucket_and_key_from_string(test_file)
        assert result == (expected_bucket, expected_key)


class TestAccessS3Object:
    """Testing get_s3_object function in src/obfuscator.py"""

    @pytest.mark.it('Get S3 object returns string')
    def test_returns_str(self, mock_s3_bucket):
        """Uses mock s3 bucket defined in test/conftest.py"""

        test_bucket = 'test-bucket'
        test_key = 'students.csv'
        result = get_s3_object(test_bucket, test_key)
        assert isinstance(result, str)

    @pytest.mark.it('Get S3 object gets expected file contents')
    def test_returns_expected_file(self, mock_s3_bucket):
        """Uses mock s3 bucket defined in test/conftest.py"""

        test_bucket = 'test-bucket'
        test_key = 'students.csv'
        with open("test/test_data/students.csv") as c:
            expected = DictReader(c)
            result = get_s3_object(test_bucket, test_key)
            buffer = StringIO(result)
            reader = DictReader(buffer)
            assert list(reader) == list(expected)


class TestSaveStreamingObjToS3:
    """Testing save_streaming_obj_to_s3 function in src/obfuscator.py"""

    @pytest.mark.it('Adds file to s3 bucket at given key')
    def test_adds_file(self, mock_s3_bucket):
        test_bucket = "test-bucket"
        test_key = "obfuscated_students.csv"
        test_data = [
            {"name": "***", "email": "***", "message": "hello"},
            {"name": "***", "email": "***", "message": "world"},
        ]
        test_object = list_to_csv_streaming_object(test_data)
        save_streaming_obj_to_s3(test_object, test_bucket, test_key)
        client = boto3.client('s3')
        result = client.list_objects_v2(Bucket=test_bucket)
        keys = [obj['Key'] for obj in result['Contents']]
        assert test_key in keys

    @pytest.mark.it('File body contains expected data')
    def test_file_has_expected_contents(self, mock_s3_bucket):
        test_bucket = "test-bucket"
        test_key = "obfuscated_students.csv"
        test_data = [
            {"name": "***", "email": "***", "message": "hello"},
            {"name": "***", "email": "***", "message": "world"},
        ]
        test_object = list_to_csv_streaming_object(test_data)
        save_streaming_obj_to_s3(test_object, test_bucket, test_key)
        result_body = get_s3_object(test_bucket, test_key)
        result_list = object_body_to_list(result_body)
        assert result_list == test_data
