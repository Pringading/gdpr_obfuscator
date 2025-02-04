import pytest
from src.utils.csv_utils import access_csv


class TestAccessS3CSV:
    """Tests for access_csv function within src/obfuscator.py"""

    @pytest.mark.it('Access csv returns list')
    def test_returns_list(self, mock_s3_bucket):
        test_bucket = 'test-bucket'
        test_key = 'students.csv'
        result = access_csv(test_bucket, test_key)
        assert isinstance(result, list)

    @pytest.mark.it('Access csv returns list of dictionaries')
    def test_returns_list_of_dictionaries(self, mock_s3_bucket):
        test_bucket = 'test-bucket'
        test_key = 'students.csv'
        result = access_csv(test_bucket, test_key)
        for item in result:
            assert isinstance(item, dict)

    @pytest.mark.it('Access csv returns expected values')
    def test_returns_expected_values(self, mock_s3_bucket):
        test_bucket = 'test-bucket'
        test_key = 'students.csv'
        expected_names = ['Person 1', 'Person 2', 'Person 3']
        result = access_csv(test_bucket, test_key)
        print([row['name'] for row in result])
        assert [row['name'] for row in result] == expected_names
