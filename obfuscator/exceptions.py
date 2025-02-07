class NoFileToObfuscate(Exception):
    """Throws error when file_to_obfuscate is not provided."""
    pass

class NoPIIFields(Exception):
    """Throws error when pii_fields are not provided."""
    pass