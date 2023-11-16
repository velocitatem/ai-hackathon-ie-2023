
import pandas as pd
import os

# Define file paths for whoomever is using this script (future implementation will be to pass these in as arguments and get it from the model and ground truth)
true_values = "path/to/file.xlsx"
generated_values = "path/to/file.csv"
differences = "path/to/file.csv"


# Check if files exist
if os.path.isfile(true_values) and os.path.isfile(generated_values):
    # Read files into dataframes
    true_values_df = pd.read_excel(true_values)
    generated_values_df = pd.read_csv(generated_values)

    # Compare dataframes
    if true_values_df.equals(generated_values_df):
        print("The dataframes are equal.")
    else:
        # Calculate percentage of differences
        num_diff = (true_values_df != generated_values_df).sum().sum()
        total_elements = true_values_df.size
        percent_diff = num_diff / total_elements * 100

        # Output percentage of differences
        print(f"The dataframes are not equal. {percent_diff:.2f}% of elements are different.")

        # Output different elements of the csv as a new csv file and create that file
        diff_df = generated_values[true_values_df != generated_values].dropna(how="all")
        diff_df.to_csv(differences, index=False)
else:
    print("One or both files do not exist.")
