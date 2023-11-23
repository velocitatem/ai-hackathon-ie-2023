import pandas as pd
import difflib

dateCols = ["Launch Date", "Final Val. Day", "Maturity"]


def read_csv(file_path, columns_to_ignore):
    data = pd.read_csv(file_path)
    data = data.drop(columns=columns_to_ignore, errors='ignore')
    for col in dateCols:
        # force to be a date object
        # date is in dd/mm/yyyy format
        # some might be Nan (string) so we need to ignore those
        data[col] = data[col].apply(lambda x: pd.to_datetime(x, format='%d/%m/%Y', errors='coerce'))


        # force to be a string
    return data




def read_excel_as_csv(excel_path, columns_to_ignore):
    data = pd.read_excel(excel_path, engine='openpyxl')
    # remove file name from column names
    # make all dates strings
    return data.drop(columns=columns_to_ignore, errors='ignore')


def main():
    csv_file_path = './testingassistMIXv4.csv'
    excel_file_path = './ground_truth_0611_U.xlsx'
    columns_to_ignore = ['Issuer', 'Underlying(s)', "File name"]

    num_rows = 3

    csv_content = read_csv(csv_file_path, columns_to_ignore)
    converted_excel_content = read_excel_as_csv(excel_file_path, columns_to_ignore)


    columns_of_interest = ['Isin', "Ccy", "Barrier", "Launch Date", "Final Val. Day", "Maturity", "Cap", "Strike"]
    columns_accuracies = []
    for column in columns_of_interest:
        csv_column = csv_content.get(column)
        excel_column = converted_excel_content.get(column)
        accuracy = 0
        for i in range(len(csv_column)):
            # one can be Nan and the other can be nan
            # so we need to ignore those
            if csv_column[i] == "Nan" and pd.isna(excel_column[i]):
                accuracy += 1
                continue

            # if excel is a float make int and csv make int
            if column == "Barrier" or column == "Cap":
                # if both are not numbers
                if csv_column[i] == "nan" and excel_column[i] == "nan":
                    accuracy += 1
                    continue

                # make both floats
                csv_column[i] = float(csv_column[i])
                excel_column[i] = float(excel_column[i])
                if csv_column[i] == excel_column[i]:
                    accuracy += 1
                    continue


            # if pd in excel is a list
            if "[" in str(excel_column[i]):
                if csv_column[i] == "Nan":
                    continue
                # convert to list
                import json
                excel_column[i] = json.loads(excel_column[i])
                csv_column[i] = json.loads(csv_column[i])


                # sort lists
                csv_column[i].sort()
                excel_column[i].sort()
                # compare lists
                differences = [a for a in csv_column[i] if a not in excel_column[i]]
                print(differences)
                if len(differences) == 0:
                    accuracy += 1
                    continue

            if csv_column[i] == excel_column[i]:
                accuracy += 1
                continue

            # if either is a date and the other is a string make both strings
            # force both to be strings

            print(csv_column[i], excel_column[i])

        accuracy = accuracy / len(csv_column)
        columns_accuracies.append(accuracy)
    # avera
    average_accuracy = sum(columns_accuracies) / len(columns_accuracies)
    print(average_accuracy)


if __name__ == "__main__":
    main()
