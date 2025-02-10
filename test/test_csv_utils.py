import pytest
import logging
from csv import DictReader
from io import StringIO
from obfuscator.main import get_s3_object
from obfuscator.csv_utils import (
    object_body_to_list,
    obfuscate_fields,
    list_to_csv_streaming_object,
)


class TestObjectBodyToList:
    """Tests object_body_to_list function in obfuscator/csv_utils.py"""

    @pytest.mark.it("Returns list")
    def test_returns_list(self, mock_s3_bucket):
        """Testing return value is a list.

        uses mock_s3_bucket fixture and accesses students.csv object inside
        test-bucket."""

        test_bucket = "test-bucket"
        test_key = "students.csv"
        test_object = get_s3_object(test_bucket, test_key)
        result = object_body_to_list(test_object)
        assert isinstance(result, list)

    @pytest.mark.it("Returns expected data")
    def test_returns_expected_data(self, mock_s3_bucket):
        """Testing return value contains same data as original file.

        uses mock_s3_bucket fixture and accesses students.csv object inside
        test-bucket. Compares data in students.csv file uploaded to
        test-bucket with local version of the same file."""

        test_bucket = "test-bucket"
        test_key = "students.csv"
        test_object = get_s3_object(test_bucket, test_key)
        result = object_body_to_list(test_object)
        print(result)
        with open("test/test_data/students.csv") as c:
            expected = DictReader(c)
            assert list(expected) == result


class TestObfuscateFields:
    """Tests obfuscate_fields function in obfuscator/csv_utils.py"""

    @pytest.mark.it("Returns list of dictioaries")
    def test_returns_list_of_dicts(self):
        """Tesing return value is a list of dictionaries."""

        test_list = [{"name": "name 1"}, {"name": "name 2"}]
        test_fields = ["name"]
        result = obfuscate_fields(test_list, test_fields)
        assert isinstance(result, list)
        for row in result:
            assert isinstance(row, dict)

    @pytest.mark.it("Obfuscates dictionaries with one field")
    def test_obfuscate_1_field(self):
        """Testing obfuscates dictionary with only one field"""

        test_list = [{"name": "name 1"}, {"name": "name 2"}]
        expected = [{"name": "***"}, {"name": "***"}]
        test_fields = ["name"]
        result = obfuscate_fields(test_list, test_fields)
        assert result == expected

    @pytest.mark.it("Obfuscates dictionaries with multiple fields")
    def test_obfuscates_multiple_fields(self):
        """Testing obfuscation of multiple fields. Only fields in list should
        be obfuscated."""

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

    @pytest.mark.it("Logs warning if given no data to obfuscate")
    def test_obfuscate_fields_empty_list(self, caplog):
        """Test warning is logged if no data passed as an argument."""

        expected_log = 'No data found to obfuscate.'
        with caplog.at_level(logging.WARNING):
            obfuscate_fields([], [])
        assert expected_log in caplog.text

    @pytest.mark.it('Logs warning if given no fields to obfuscate')
    def test_obfuscate_fields_empty_fields(self, caplog):
        """Test warning logged when fields list is empty."""

        expected_log = 'No fields found to obfuscate'
        test_list = [
            {"name": "name 1", "email": "1@email.com", "message": "hello"},
            {"name": "name 2", "email": "2@email.com", "message": "world"},
        ]
        with caplog.at_level(logging.WARNING):
            obfuscate_fields(test_list, [])
        assert expected_log in caplog.text

    @pytest.mark.it('Logs warning if none of the given fields found in data')
    def test_fields_not_found(self, caplog):
        """Test warning is logged if fields do not exist as keys on given
        data."""

        expected_log = 'No fields found to obfuscate'
        test_fields = ['address', 'course']
        test_list = [
            {"name": "name 1", "email": "1@email.com", "message": "hello"},
            {"name": "name 2", "email": "2@email.com", "message": "world"},
        ]
        with caplog.at_level(logging.WARNING):
            obfuscate_fields(test_list, test_fields)
        assert expected_log in caplog.text

    @pytest.mark.it('Logs warning if some fo the given fields missing in data')
    def test_logs_missing_fields(self, caplog):
        """Tests warning is logged if any of the fields in field list are
        not found in the given data."""

        expected_log = 'address, course fields not found in data.'
        test_fields = ['address', 'course', 'name']
        test_list = [
            {"name": "name 1", "email": "1@email.com", "message": "hello"},
            {"name": "name 2", "email": "2@email.com", "message": "world"},
        ]
        with caplog.at_level(logging.WARNING):
            obfuscate_fields(test_list, test_fields)
        assert expected_log in caplog.text

    @pytest.mark.it('Logs info about which fields have been obfuscated')
    def test_logs_info_about_obfuscated_fields(self, caplog):
        """Testing logs info stating which fields have been obfuscated."""

        expected_log = 'name, email fields have been successfully obfuscated'
        test_fields = ['address', 'course', 'name', 'email']
        test_list = [
            {"name": "name 1", "email": "1@email.com", "message": "hello"},
            {"name": "name 2", "email": "2@email.com", "message": "world"},
        ]
        with caplog.at_level(logging.INFO):
            obfuscate_fields(test_list, test_fields)
        assert expected_log in caplog.text


class TestListToCSVStreamingObject:
    """Tests save_streaming_obj_to_s3 function in obfuscator/csv_utils.py"""

    @pytest.mark.it("Returns streaming object")
    def test_returns_streaming_object(self):
        """Tesing return value is a StringIO streaming object."""

        test_data = [
            {"name": "***", "email": "***", "message": "hello"},
            {"name": "***", "email": "***", "message": "world"},
        ]
        result = list_to_csv_streaming_object(test_data)
        assert isinstance(result, StringIO)

    @pytest.mark.it("Outputted streaming object contains expected data")
    def test_object_contains_expected_data(self):
        """Testing returned object contains same data as originally given
        as an argument."""

        test_data = [
            {"name": "***", "email": "***", "message": "hello"},
            {"name": "***", "email": "***", "message": "world"},
        ]
        result = list_to_csv_streaming_object(test_data)
        reader = DictReader(result)
        assert list(reader) == test_data

    @pytest.mark.it("Returns empty StringIO object if no data given")
    def test_no_data(self):
        """Testing function can handle empty data as an input."""

        result = list_to_csv_streaming_object([])
        reader = DictReader(result)
        assert list(reader) == []
