import boto3
from io import StringIO
from csv import DictReader


def object_body_to_list(body: str) -> list[dict]:
    buffer = StringIO(body)
    reader = DictReader(buffer)
    return list(reader)


def obfuscate_fields(rows: list[dict], fields: list[str]) -> list[dict]:
    return rows


def list_to_csv_streaming_object():
    pass
