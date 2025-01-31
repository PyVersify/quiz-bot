from typing import Annotated

def _json_file_validator(value: str) -> bool:
    """Checks if a string is a valid JSON file.
    
    Args:
        value (str): The string to check.
    
    Returns:
        bool: True if the string ends with '.json', False otherwise.
    """
    return value.endswith('.json')


JsonFileName = Annotated[str, _json_file_validator]


