# gdpr_obfuscator

[![gdpr-obfuscator](https://github.com/Pringading/gdpr_obfuscator/actions/workflows/checks.yml/badge.svg)](https://github.com/Pringading/gdpr_obfuscator/actions/workflows/checks.yml)
![Coverage Badge](https://img.shields.io/badge/coverage-99%25-forestgreen)
![version](https://img.shields.io/badge/version-0.0.1-blue)
[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)

A general-purpose tool to process data being ingested to AWS and intercept personally identifiable information.

**Table of Contents**

- [Installation](#installation)
- [Execution / Usage](#execution--usage)
- [Technologies](#technologies)
- [Features](#features)
- [Contributors](#contributors)
- [Change log](#change-log)
- [License](#license)


## Installation
The package can be installed by running the following code in the terminal:

```bash
$ pip install <path to repo>/gdpr_obfuscator/dist/obfuscator-0.0.1-py3-none-any.whl
```
.

## Execution / Usage

To run the obfuscator, import it into a python library. It can be called with a json string providing the s3 location of the file to be obfuscated (file_to_obfuscate) and a list of the fields to be obfuscated (pii_fields).

Example input:
```json
{
    "file_to_obfuscate": "s3://my_ingestion_bucket/new_data/file1.csv",
    "pii_fields": ["name", "email_address"]
}
```

After installing, the function can be imported into a python project and called with a JSON string.

The function returns a byte object that can be added to an aws bucket using the put-object aws api call.

Example Usage:
```py
from obfuscator import obfuscator
import boto3

json_str =  '{"file_to_obfuscate": "s3://my_ingestion_bucket/new_data/file1.csv", "pii_fields": ["name", "email_address"]}'

obfuscated_data = obfuscator(json_str)

s3client = boto3.client('s3')
client.put_object(
    Bucket='name-of-bucket',
    Key='key-name-to-save-obfuscated-file.csv',
    Body=obfuscated_data,
)
```


## Used Technologies

GDPR obfuscator uses the following technologies and tools:

[![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](https://www.python.org/)

[![Boto3](https://img.shields.io/badge/boto3-yellow?style=for-the-badge)](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/quickstart.html)


**Testing Libraries**

[![moto](https://img.shields.io/badge/moto-red?style=for-the-badge)](http://docs.getmoto.org/en/latest/index.html)

[![pytest](https://img.shields.io/badge/pytest-%230A9EDC?style=for-the-badge&logo=pytest&logoColor=white)](https://docs.pytest.org/en/stable/)

**DevOps**

[![Makefile](https://img.shields.io/badge/makefile-orange?style=for-the-badge)](https://img.shields.io/badge/makefile-orange?style=for-the-badge)

[![Github Actions](https://img.shields.io/badge/githubactions-%232088FF?style=for-the-badge&logo=githubactions&logoColor=white)](https://docs.github.com/en/actions)


## Features

GDPR Obfuscator is currently able to obfuscate CSV files.

Potentially support for JSON and parquet files may be offered in the future.
.

## Contributors

Project for Northcoders:

[![Northcoders](https://www.northcodersgroup.com/include/images/logo.svg)](https://northcoders.com/)

## Change log

- 0.1.0
    - First working version
- 0.0.1
    - Work in progress

## License

GDPR Obfuscator is distributed under the MIT license. See [`LICENSE`](LICENSE) for more details.

