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
output_filename = os.path.splitext(os.path.basename(csv_file_path))[0] + "-b.csv"
df.to_csv(output_filename, header=False, index=False)

print("Output file saved as:", output_filename)
