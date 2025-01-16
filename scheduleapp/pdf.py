# Import Module
from win32com import client

# Open Microsoft Excel
excel = client.Dispatch("Excel.Application")

# Read Excel File
sheets = excel.Workbooks.Open('C:\\Users\\Mohammad Reza\\Downloads\\details.xlsx')
work_sheets = sheets.Worksheets[0]

# Convert into PDF File
work_sheets.ExportAsFixedFormat(0, 'C:\\Users\\Mohammad Reza\\Downloads\\test.pdf')
