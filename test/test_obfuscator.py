import pytest
import boto3
import json
from time import time
from csv import DictReader
from io import StringIO, BytesIO
from obfuscator.csv_utils import (
    list_to_csv_streaming_object,
    object_body_to_list,
)
from obfuscator.main import (
    obfuscator,
    get_bucket_and_key_from_string,
    get_s3_object,
    save_streaming_obj_to_s3,
)


class TestObfuscator:
    """Integration tests for obfuscator function in src/obfuscator.py"""

    @pytest.mark.it("Returns BytesIO object")
    def test_returns_bytes_io_object(self, mock_s3_bucket):
        """Tests that BytesIO object is returned from function.

        Uses mock_s3_bucket fixture and students.csv object."""

        test_request = {
            "file_to_obfuscate": "s3://test-bucket/students.csv",
            "pii_fields": ["name", "email_address"],
        }
        json_request = json.dumps(test_request)
        result = obfuscator(json_request)

        # check file has been added at the new key in the bucket
        assert isinstance(result, BytesIO)

    @pytest.mark.it("Returned object has obfuscated expected fields")
    def test_fields_obfuscated(self, mock_s3_bucket):
        """Tests that returned BytesIO object has obfuscated fields.

        Uses mock_s3_bucket fixture and students.csv object."""

        test_request = {
            "file_to_obfuscate": "s3://test-bucket/students.csv",
            "pii_fields": ["name", "email_address"],
        }
        json_request = json.dumps(test_request)
        result = obfuscator(json_request)

        # check file has been added at the new key in the bucket
        buffer = StringIO(result.read().decode('utf-8'))
        reader = DictReader(buffer)
        for row in reader:
            assert row["name"] == "***"
            assert row["email_address"] == "***"

    @pytest.mark.it("processes 1MB file in less than 1 minute")
    def test_takes_less_than_1_min(self, s3_bucket_1MB):
        """Checks the obfuscator function processes 1MB file in < 1 minute

        Uses s3_bucket_1MB fixture from conftest.py which uploads the larger
        csv file movies.csv to the test-bucket. Uses time function from time
        module to measure how long the function takes to complete."""

        test_request = {
            "file_to_obfuscate": "s3://test-bucket/movies.csv",
            "pii_fields": ["Title", "Director", "Writer"],
        }
        json_request = json.dumps(test_request)

        start = time()
        result = obfuscator(json_request)
        buffer = StringIO(result.read().decode('utf-8'))
        reader = DictReader(buffer)
        for row in reader:
            assert row["Title"] == "***"
            assert row["Director"] == "***"
            assert row["Writer"] == "***"
        end = time()
        assert end - start < 60


class TestGetBucketAndKeyFromString:
    """Testing get_bucket_and_key_from_string function in src/obfuscator.py"""

    @pytest.mark.it("Obtains bucket and key name from s3 address.")
    def test_returns_bucket_name(self):
        """Testing returns the expected bucket and key name."""

        test_file = "s3://my_ingestion_bucket/new_data/file1.csv"
        expected_bucket = "my_ingestion_bucket"
        expected_key = "new_data/file1.csv"
        result = get_bucket_and_key_from_string(test_file)
        assert result == (expected_bucket, expected_key)


class TestAccessS3Object:
    """Testing get_s3_object function in src/obfuscator.py"""

    @pytest.mark.it("Get S3 object returns string")
    def test_returns_str(self, mock_s3_bucket):
        """Testing returns a string.

        Uses mock s3 bucket defined in test/conftest.py"""

        test_bucket = "test-bucket"
        test_key = "students.csv"
        result = get_s3_object(test_bucket, test_key)
        assert isinstance(result, str)

    @pytest.mark.it("Get S3 object gets expected file contents")
    def test_returns_expected_file(self, mock_s3_bucket):
        """Testing data returned matches data in original csv file.

        Uses mock_s3_bucket defined in test/conftest.py this bucket contains
        student.csv uploaded from test/test_data so this test confirms that
        the data returned by the function matches the data read from straight
        from the csv file."""

        test_bucket = "test-bucket"
        test_key = "students.csv"
        with open("test/test_data/students.csv") as c:
            expected = DictReader(c)
            result = get_s3_object(test_bucket, test_key)
            buffer = StringIO(result)  # convert result to streaming obj
            reader = DictReader(buffer)  # reads data in dictionary format
            assert list(reader) == list(expected)


class TestSaveStreamingObjToS3:
    """Testing save_streaming_obj_to_s3 function in src/obfuscator.py"""

    @pytest.mark.it("Adds file to s3 bucket at given key")
    def test_adds_file(self, mock_s3_bucket):
        """Testing file is added to bucket at the given key.

        uses mock_s3_bucket fixture from conftest.py to check if file is added
        to test-bucket"""

        test_bucket = "test-bucket"
        test_key = "obfuscated_students.csv"
        test_data = [
            {"name": "***", "email": "***", "message": "hello"},
            {"name": "***", "email": "***", "message": "world"},
        ]
        test_object = list_to_csv_streaming_object(test_data)
        save_streaming_obj_to_s3(test_object, test_bucket, test_key)
        client = boto3.client("s3")
        result = client.list_objects_v2(Bucket=test_bucket)
        keys = [obj["Key"] for obj in result["Contents"]]  # lists only keys
        assert test_key in keys

    @pytest.mark.it("File body contains expected data")
    def test_file_has_expected_contents(self, mock_s3_bucket):
        """Tests data in uploaded file is identical to test_data."""

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
