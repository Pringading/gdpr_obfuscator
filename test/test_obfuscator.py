import pytest
import boto3
from csv import DictReader
from io import StringIO
from src.utils.csv_utils import list_to_csv_streaming_object
from src.obfuscator import (
    get_bucket_and_key_from_string,
    get_s3_object,
    save_streaming_obj_to_s3,
)


class TestObfuscator:
    pass


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
        print(keys)
        assert test_key in keys


    @pytest.mark.skip
    @pytest.mark.it('File body contains expected data')
    def test_file_has_expected_contents(self):
        pass
