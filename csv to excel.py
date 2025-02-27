# csv_to_excel.py

import csv
import openpyxl


def csv_to_excel(csv_file, excel_file):
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    with open(csv_file) as file_obj:
        reader = csv.reader(file_obj, delimiter='|')
        for row in reader:
            sheet.append(row)
    workbook.save(excel_file)

if __name__ == "__main__":
    csv_to_excel("ventes_smartphones.csv", "ventes_smartphones.xlsx")