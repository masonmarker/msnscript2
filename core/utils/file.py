"""File based functions."""


import os
import uuid

# creates a temporary directory
def create_temp_dir():
    """Create a temporary directory and return the path."""
    new_folder_path = os.getcwd().replace('\\', '/') + "/tmp/" + uuid.uuid4().hex
    os.makedirs(new_folder_path)
    return new_folder_path