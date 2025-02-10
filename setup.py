from setuptools import setup

setup(
    name="obfuscator",
    version="0.0.1",
    packages=["obfuscator"],
    install_requires=[
        'boto3==1.36.12',
        'botocore==1.36.12',
        'jmespath==1.0.1',
        'python-dateutil==2.9.0.post0',
        's3transfer==0.11.2',
        'six==1.17.0',
        'urllib3==2.3.0',
    ],
    entry_points={
        "console_scripts" :[
            "obfuscator_hello = obfuscator.main:hello",
        ]
    }
)