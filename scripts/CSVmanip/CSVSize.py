import pandas as pd
import sys
import os

# Check if a CSV file path is provided as a command-line argument
if len(sys.argv) > 1:
    csv_file_path = sys.argv[1]
else:
    print("Please provide the path to the CSV file as a command-line argument.")
    sys.exit(1)

# Load the CSV file into a pandas DataFrame
df = pd.read_csv(csv_file_path)

print("0, 0 -", df.iloc[0, 0])
print("0, 1 -", df.iloc[0, 1])
print("0, 2 -", df.iloc[0, 2])
print("1, 0 -", df.iloc[1, 0])

print(df.shape)
