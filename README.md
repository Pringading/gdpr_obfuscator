# gdpr_obfuscator
work in progress

A general-purpose tool to process data being ingested to AWS and intercept personally identifiable information.

[![gdpr-obfuscator](https://github.com/Pringading/gdpr_obfuscator/actions/workflows/checks.yml/badge.svg)](https://github.com/Pringading/gdpr_obfuscator/actions/workflows/checks.yml)

## Project Description
An obfuscation tool that can be integrated as a library module into a Python codebase.

The tool will be supplied with the S3 location of a file containing sensitive information, and the names of the affected fields. It will create a new file or byte-stream object containing an exact copy of the input file but with the sensitive data replaced with obfuscated strings. The calling procedure will handle saving the output to its destination. It is expected that the tool will be deployed within the AWS account.

## Installation
The package can be installed by running the following code within the terminal:

```bash
pip install <path to repo>/gdpr_obfuscator/dist/obfuscator-0.1.0-py3-none-any.whl
```

## Execution and Usage
The obfuscator takes one argument json_str, which provides the S3 location of the file to be obfuscated (file_to_obfuscate) and a list of the fields to be obfuscated (pii_fields).

Example input:
```json
{
    "file_to_obfuscate": "s3://my_ingestion_bucket/new_data/file1.csv",
    "pii_fields": ["name", "email_address"]
}
```

After installing, the function can be imported into a python project and called with a JSON string.

```py
from obfuscator import obfuscator

json_str =  '{"file_to_obfuscate": "s3://my_ingestion_bucket/new_data/file1.csv", "pii_fields": ["name", "email_address"]}'

obfuscator(json_str)
```

## Used Technologies
- python
- boto3

**Testing**
- moto
- pytest
- Makefile

