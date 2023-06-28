import pandas as pd
import os
import sys

def delete_fraction_and_save(df, size, new_filename):
    new_df = df.iloc[:, :size]
    
    new_df.to_csv(new_filename, index=False, header=False)

def delete_fraction_and_save_repeatedly(csv_filepath, folder_name):
    # Read the initial CSV file into a pandas DataFrame
    df = pd.read_csv(csv_filepath)
    
    # Iterate until the dataset size is equal to 0
    cells = df.shape[1]

    for i in range(1, 6):
        size = int(cells * i / 5)
        print(f"Creating with size {size}")
        filename = os.path.basename(csv_filepath)
        new_filename = os.path.join(folder_name, f"modified_{i}_{size}_" + filename)
        delete_fraction_and_save(df, size, new_filename)

# Example usage
if len(sys.argv) != 3:
    print("Usage: python script.py csv_filepath folder_name")
    sys.exit(1)

csv_filepath = sys.argv[1]
folder_name = sys.argv[2]

delete_fraction_and_save_repeatedly(csv_filepath, folder_name)