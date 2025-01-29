import os
from pathlib import Path

#
# def change_extension(file_path, new_extension):
#     base_name, _ = os.path.splitext(file_path)
#     new_file_path = base_name +'.'+ new_extension
#     os.rename(file_path, new_file_path)
#
# BASE_DIR = Path(__file__).resolve().parent.parent /'Storage'/'1403-10-18'/'56'
# # Example usage:
# change_extension(BASE_DIR,'jpg')
# print('Successfully Changed!')



# import OS module
import os
# Get the list of all files and directories
file_name=str(18)
path = "C:\\Users\\M.kazemnezhad\\Desktop\\New folder (7)"


dir_list = os.listdir(path)
print(dir_list)
k=0
for data in dir_list:
    if file_name in data:
        pythonfile=data
        newpath=os.path.abspath(pythonfile)






