import xlsxwriter
import io

def write(worksheet, formater):
    worksheet.write("A1", "Hello", formater)

# output = io.BytesIO()
workbook = xlsxwriter.Workbook("example.xlsx")
worksheet  = workbook.add_worksheet()
border_format = workbook.add_format({"border": True})
write(worksheet, border_format)

# Clean up
workbook.close()