import toml
from typing import Dict, Union


def read_toml_file(path:str, file_name:str) -> Dict[str, Union[str, int, float]]:
    """Function to read toml file based on specified path and file name
    Args:
        path (str): Path
        file_name (str): File Name

    Returns:

    """
    with open(path + file_name) as file:
        data = toml.load(file)
    return data
