import pytest
from moto import mock_aws
import boto3
import os


@pytest.fixture
def aws_credentials():
    """mock credentials for moto"""
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "eu-west-2"


@pytest.fixture
def mock_s3_bucket(aws_credentials):
    with mock_aws():
        client = boto3.client("s3")
        client.create_bucket(
            Bucket="test-bucket",
            CreateBucketConfiguration={"LocationConstraint": "eu-west-2"},
        )
        client.upload_file(
            Filename='test/test_data/students.csv',
            Bucket='test-bucket',
            Key='students.csv',
        )
        yield client


@pytest.fixture
def s3_bucket_1MB(aws_credentials):
    with mock_aws():
        client = boto3.client("s3")
        client.create_bucket(
            Bucket="test-bucket",
            CreateBucketConfiguration={"LocationConstraint": "eu-west-2"},
        )
        client.upload_file(
            Filename='test/test_data/IMDB_Movies_Dataset.csv',
            Bucket='test-bucket',
            Key='movies.csv',
        )
        yield client
