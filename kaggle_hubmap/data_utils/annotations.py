import json
import logging
import os
import typing as t


def read_json_file(file_path: os.PathLike) -> t.List[t.Dict[str, t.Any]]:
    """
    Reads a JSON file and returns a list of dictionaries.
    """
    json_data = []
    with open(file_path, 'r') as file:
        for line in file:
            # Skip empty lines or lines containing only whitespace
            if line.strip():
                json_obj = json.loads(line)
                json_data.append(json_obj)
        
    return json_data
