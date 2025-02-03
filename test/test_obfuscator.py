import pytest
from src.obfuscator import access_csv


class TestAccessS3CSV:

    @pytest.mark.it('Access csv returns dictionary')
    def test_returns_dictionary(self, mock_s3_bucket):
        test_bucket = 'test-bucket'
        test_key = 'students.csv'
        result = access_csv(test_bucket, test_key)
        assert isinstance(result, list)
    
    @pytest.mark.it('Access csv returns expected values')
    def test_returns_expected_values(self, mock_s3_bucket):
        test_bucket = 'test-bucket'
        test_key = 'students.csv'
        expected_names = ['Person 1', 'Person 2', 'Person 3']
        result = access_csv(test_bucket, test_key)
        print([row['name'] for row in result])
        assert [row['name'] for row in result] == expected_names
