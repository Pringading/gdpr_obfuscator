import pytest
from src.obfuscator import get_bucket_and_key_from_string


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
    pass


class TestSaveStreamingObjToS3:
    pass
