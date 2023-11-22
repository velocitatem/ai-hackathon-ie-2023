import pandas as pd
import difflib

def read_csv(file_path):
    return pd.read_csv(file_path)

def read_excel_as_csv(excel_path):
    return pd.read_excel(excel_path, engine='openpyxl').to_csv()

def compare_files(file1, file2):
    differences = list(difflib.unified_diff(
        file1.splitlines(), file2.splitlines(), 
        lineterm='', fromfile='file1', tofile='file2'
    ))
    return differences

def main():
    csv_file_path = 'path_to_your_csv_file.csv'
    excel_file_path = 'path_to_your_excel_file.xlsx'

    csv_content = read_csv(csv_file_path)
    converted_excel_content = read_excel_as_csv(excel_file_path)

    differences = compare_files(csv_content.to_csv(), converted_excel_content)

    if differences:
        print("Differences found:")
        for line in differences:
            print(line)
    else:
        print("No differences found.")



