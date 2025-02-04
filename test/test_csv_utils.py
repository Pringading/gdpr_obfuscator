import pytest
from csv import DictReader
from io import StringIO
from src.obfuscator import get_s3_object
from src.utils.csv_utils import (
    object_body_to_list,
    obfuscate_fields,
    list_to_csv_streaming_object,
)


class TestObjectBodyToList:
    @pytest.mark.it('Returns list')
    def test_returns_list(self, mock_s3_bucket):
        test_bucket = 'test-bucket'
        test_key = 'students.csv'
        test_object = get_s3_object(test_bucket, test_key)
        result = object_body_to_list(test_object)
        assert isinstance(result, list)

    @pytest.mark.it('Returns expected data')
    def test_returns_expected_data(self, mock_s3_bucket):
        test_bucket = 'test-bucket'
        test_key = 'students.csv'
        test_object = get_s3_object(test_bucket, test_key)
        result = object_body_to_list(test_object)
        print(result)
        with open("test/test_data/students.csv") as c:
            expected = DictReader(c)
            assert list(expected) == result


class TestObfuscateFields:
    @pytest.mark.it('Returns list of dictioaries')
    def test_returns_list_of_dicts(self):
        test_list = [
            {"name": "name 1"},
            {"name": "name 2"}
        ]
        test_fields = ["name"]
        result = obfuscate_fields(test_list, test_fields)
        assert isinstance(result, list)
        for row in result:
            assert isinstance(row, dict)

    @pytest.mark.it('Obfuscates dictionaries with one field')
    def test_obfuscate_1_field(self):
        test_list = [
            {"name": "name 1"},
            {"name": "name 2"}
        ]
        expected = [
            {"name": "***"},
            {"name": "***"}
        ]
        test_fields = ["name"]
        result = obfuscate_fields(test_list, test_fields)
        assert result == expected

    @pytest.mark.it('Obfuscates dictionaries with multiple fields')
    def test_obfuscates_multiple_fields(self):
        test_list = [
            {"name": "name 1", "email": "1@email.com", "message": "hello"},
            {"name": "name 2", "email": "2@email.com", "message": "world"},
        ]
        expected = [
            {"name": "***", "email": "***", "message": "hello"},
            {"name": "***", "email": "***", "message": "world"},
        ]
        test_fields = ["name", "email"]
        result = obfuscate_fields(test_list, test_fields)
        assert result == expected


class TestListToCSVStreamingObject:
    @pytest.mark.it('Returns streaming object')
    def test_returns_streaming_object(self):
        test_data = [
            {"name": "***", "email": "***", "message": "hello"},
            {"name": "***", "email": "***", "message": "world"},
        ]
        result = list_to_csv_streaming_object(test_data)
        assert isinstance(result, StringIO)

    @pytest.mark.skip
    @pytest.mark.it('Outputted streaming object contains expected data')
    def test_object_contains_expected_data(self):
        pass
