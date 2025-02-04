from io import StringIO
from csv import DictReader, DictWriter


def object_body_to_list(body: str) -> list[dict]:
    buffer = StringIO(body)
    reader = DictReader(buffer)
    return list(reader)


def obfuscate_fields(rows: list[dict], fields: list[str]) -> list[dict]:
    obfuscated_list = []
    for row in rows:
        new_dict = {}
        for key, value in row.items():
            if key in fields:
                new_dict[key] = "***"
            else:
                new_dict[key] = value
        obfuscated_list.append(new_dict)
    return obfuscated_list


def list_to_csv_streaming_object(data: list[str]) -> StringIO:
    buffer = StringIO()
    fieldnames = list(data[0].keys())
    writer = DictWriter(buffer, fieldnames=fieldnames)
    writer.writeheader()
    for row in data:
        writer.writerow(row)
    buffer.seek(0) # goes to the start of StringIO object to read contents
    return buffer
