import pandas as pd
import difflib

def read_csv(file_path, columns_to_ignore):
    data = pd.read_csv(file_path)
    return data.drop(columns=columns_to_ignore, errors='ignore')

def read_excel_as_csv(excel_path, columns_to_ignore):
    data = pd.read_excel(excel_path, engine='openpyxl')
    return data.drop(columns=columns_to_ignore, errors='ignore').to_csv(index=False)

def compare_files(file1, file2):
    differences = list(difflib.unified_diff(
        file1.splitlines(), file2.splitlines(),
        lineterm='', fromfile='file1', tofile='file2'
    ))
    return differences

def main():
    csv_file_path = 'path_csv'
    excel_file_path = 'path_xlsx'
    columns_to_ignore = ['Issuer', 'Underlying(s)']

    csv_content = read_csv(csv_file_path, columns_to_ignore)
    converted_excel_content = read_excel_as_csv(excel_file_path, columns_to_ignore)

    differences = compare_files(csv_content.to_csv(index=False), converted_excel_content)

    diff_count = len(differences)
    if diff_count > 0:
        print(f"Differences found: {diff_count}")
    else:
        print("No differences found.")

if __name__ == "__main__":
    main()


