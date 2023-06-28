import pandas as pd
import sys
import os

output_directory = "bitmuris"

def do_transform(csv_file_path):
    # Load the CSV file into a pandas DataFrame
    df = pd.read_csv(csv_file_path)

    # Print specific values
    print("0, 0 -", df.iloc[0, 0])
    print("0, 1 -", df.iloc[0, 1])
    print("1, 0 -", df.iloc[1, 0])
    print("1, 1 -", df.iloc[1, 1])

    # Remove the first column
    df = df.iloc[:, 1:]

    # Get the number of columns and rows
    num_columns = df.shape[1]
    num_rows = df.shape[0]

    # Print column size
    print("Number of columns:", num_columns)

    # Print row size
    print("Number of rows:", num_rows)

    # Replace non-zero values with 1
    df[df != 0] = 1

    # Save the modified DataFrame to a new CSV file
    file_name = os.path.basename(file_path)
    output_filename = os.path.join(output_directory, file_name)
    df.to_csv(output_filename, header=False, index=False)
    print("Output file saved as:", output_filename)

# Check if a directory is provided as a command-line argument
if len(sys.argv) > 1:
    target_directory = sys.argv[1]

    for filename in os.listdir(target_directory):
        if filename.endswith('.csv'):
            file_path = os.path.join(target_directory, filename)
            print("File found:", file_path)
            do_transform(file_path)
else:
    print("Please provide a directory path as a command-line argument.")