import pytest
from csv import DictReader
from io import StringIO
from src.obfuscator import (
    get_bucket_and_key_from_string,
    get_s3_object,
)


class TestObfuscator:
    pass


class TestGetBucketAndKeyFromString:
    @pytest.mark.it('Obtains bucket and key name from s3 address.')
    def test_returns_bucket_name(self):
        test_file = "s3://my_ingestion_bucket/new_data/file1.csv"
        expected_bucket = "my_ingestion_bucket"
        expected_key = "new_data/file1.csv"
        result = get_bucket_and_key_from_string(test_file)
        assert result == (expected_bucket, expected_key)


class TestAccessS3Object:
    @pytest.mark.it('Get S3 object returns string')
    def test_returns_str(self, mock_s3_bucket):
        test_bucket = 'test-bucket'
        test_key = 'students.csv'
        result = get_s3_object(test_bucket, test_key)
        assert isinstance(result, str)

    @pytest.mark.it('Get S3 object gets expected file contents')
    def test_returns_expected_file(self, mock_s3_bucket):
        test_bucket = 'test-bucket'
        test_key = 'students.csv'
        with open("test/test_data/students.csv") as c:
            expected = DictReader(c)
            result = get_s3_object(test_bucket, test_key)
            buffer = StringIO(result)
            reader = DictReader(buffer)
            assert list(reader) == list(expected)


class TestSaveStreamingObjToS3:
    pass
