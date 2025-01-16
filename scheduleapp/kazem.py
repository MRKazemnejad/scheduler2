import os
from pathlib import Path


def change_extension(file_path, new_extension):
    base_name, _ = os.path.splitext(file_path)
    new_file_path = base_name +'.'+ new_extension
    os.rename(file_path, new_file_path)

BASE_DIR = Path(__file__).resolve().parent.parent /'Storage'/'1403-10-18'/'56'
# Example usage:
change_extension(BASE_DIR,'jpg')
print('Successfully Changed!')