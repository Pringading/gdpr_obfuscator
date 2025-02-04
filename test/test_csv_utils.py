import pytest
from src.obfuscator import get_s3_object
from csv import DictReader
from src.utils.csv_utils import (
    object_body_to_list,
    obfuscate_fields,
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

    @pytest.mark.skip
    @pytest.mark.it('Obfuscates dictionaries with one field')
    def test_obfuscate_1_field(self):
        test_list = [
            {"name": "name 1"},
            {"name": "name 2"}
        ]
        test_fields = ["name"]
        obfuscate_fields(test_list, test_fields)

    @pytest.mark.skip
    @pytest.mark.it('Obfuscates dictionaries with multiple fields')
    def test_obfuscates_multiple_fields(self):
        test_list = [
            {"name": "name 1", "email": "1@email.com", "message": "hello"},
            {"name": "name 2", "email": "2@email.com", "message": "world"},
        ]
        test_fields = ["name", "email"]
        obfuscate_fields(test_list, test_fields)


class TestListToCSVStreamingObject:
    pass
