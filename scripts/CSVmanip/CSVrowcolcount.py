import pandas as pd
import os
import sys

def count_rows_cols(file_path):
    df = pd.read_csv(file_path)
    rows, cols = df.shape
    return rows, cols

def count_rows_cols_in_directory(directory):
    total_rows = 0
    total_cols = 0
    for filename in os.listdir(directory):
        if filename.endswith('.csv'):
            file_path = os.path.join(directory, filename)
            rows, cols = count_rows_cols(file_path)
            total_rows += rows
            total_cols += cols
            print(f"{filename}: Rows={rows}, Cols={cols}")
    print(f"\nTotal Rows: {total_rows}")
    print(f"Total Cols: {total_cols}")

# Check if a directory is provided as a command-line argument
if len(sys.argv) > 1:
    target_directory = sys.argv[1]
    count_rows_cols_in_directory(target_directory)
else:
    print("Please provide a directory path as a command-line argument.")