def obfuscator(json_str: str) -> None:
    pass


def get_bucket_and_key_from_string(filename: str) -> tuple[str]:
    for i in range(5, len(filename)):
        if filename[i] == "/":
            break
    bucket = filename[5: i]
    key = filename[i + 1:]
    return bucket, key


def access_s3_object(bucket: str, key: str) -> str:
    pass


def save_streaming_obj_to_s3(obj, bucket: str, key: str) -> None:
    pass
