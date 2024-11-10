
from core.classes.excel.workbook import Workbook

# sheet class


class Sheet(Workbook):
    def __init__(self, sheet, title, workbook, path) -> None:
        super().__init__(workbook, path)
        self.sheet = sheet
        self.title = title
