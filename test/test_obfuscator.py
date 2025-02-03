import pytest
from src.obfuscator import access_csv


class TestAccessS3CSV:

    @pytest.mark.it('Access csv returns dictionary')
    def test_returns_dictionary(self, mock_s3_bucket):
        test_path = 's3://test-bucket/students.csv'
        result = access_csv(test_path)
        assert isinstance(result, dict)
        