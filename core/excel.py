

from core.classes.excel.workbook import Workbook


def f_excel(inter, line, args, **kwargs):

 # automating Excel
 import openpyxl

 path = inter.parse(0, line, args)[2]
 # path must be str
 inter.type_err([(path, (str,))], line, kwargs["lines_ran"])
 # creates and returns a Workbook
 return Workbook(openpyxl.load_workbook(path), path)


EXCEL_DISPATCH = {
    "excel": f_excel,
}
