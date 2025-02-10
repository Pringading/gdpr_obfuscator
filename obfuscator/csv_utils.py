import logging
from io import StringIO
from csv import DictReader, DictWriter


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def object_body_to_list(body: str) -> list[dict]:
    """Takes csv string from the body of a S3 object and returns as a list

    Args:
        body(str): csv string from Body property of an S3 object.

    Returns: Data from body formatted as a list of dictionaries."""

    buffer = StringIO(body)
    reader = DictReader(buffer)
    return list(reader)


def obfuscate_fields(data: list[dict], fields: list[str]) -> list[dict]:
    """Takes a list of dictionaries and obfuscates all fields from given list

    Args:
        data (list[dict]): data as a list of dictionaries
        fields(list): list of fields that should be obfuscated.

    Returns: Identical dictionary with all values on given fields to be
    obfuscated equal to ***"""

    # log warning and return if given no data to obfuscate
    if len(data) == 0:
        logger.warning('No data found to obfuscate.')
        return []

    # check which fields are present in given data
    not_found = [field for field in fields if field not in data[0]]
    found = [field for field in fields if field in data[0]]

    # log warning if any of the fields are not in given data
    if not_found:
        logger.warning(', '.join(not_found) + ' fields not found in data.')

    # log warning and return original data if no fields to obfuscate
    if len(found) == 0:
        logger.warning('No fields found to obfuscate')
        return data

    # obfuscate data
    obfuscated_list = []
    for row in data:
        new_dict = {}
        for key, value in row.items():
            if key in fields:
                new_dict[key] = "***"
            else:
                new_dict[key] = value
        obfuscated_list.append(new_dict)

    # log obfuscated fields & return obfuscated data
    logger.info(', '.join(found) + ' fields have been successfully obfuscated')
    return obfuscated_list


def list_to_csv_streaming_object(data: list[str]) -> StringIO:
    """Converts list of dictionaries to streaming object with csv data.

    Args: data(list[str]): data to be saved to streaming object
    Returns: StringIO with data in csv format"""

    buffer = StringIO()
    fieldnames = list(data[0].keys())
    writer = DictWriter(buffer, fieldnames=fieldnames)
    writer.writeheader()
    for row in data:
        writer.writerow(row)
    buffer.seek(0)  # goes to the start of StringIO object to read contents
    return buffer
