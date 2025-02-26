"""Custom exceptions used by obfuscator"""


class NoFileToObfuscate(Exception):
    """Traps error when file_to_obfuscate is not provided."""
    pass


class InvalidFileToObfuscate(Exception):
    """Traps error when file_to_obfuscate not a valid S3 Location"""
    pass


class NoPIIFields(Exception):
    """Traps error when pii_fields are not provided."""
    pass
