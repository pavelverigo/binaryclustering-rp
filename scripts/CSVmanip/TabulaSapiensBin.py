import scanpy as sc
import numpy as np
import pandas as pd


# Provide the path to your H5AD file
h5ad_file = "TS_Skin.h5ad"

# Read the H5AD file
adata = sc.read_h5ad(h5ad_file)

num_cells = adata.shape[0]
num_genes = adata.shape[1]

# Print the number of cells and genes
print("Number of cells:", num_cells)
print("Number of genes:", num_genes)

gene_expression_matrix = adata.raw.X

cell_index = 0
gene_index = 0
count = gene_expression_matrix[cell_index, gene_index]

# Print the count
print("Count for cell", cell_index, "and gene", gene_index, ":", count)


df = pd.DataFrame(gene_expression_matrix.toarray(), 
                  index=adata.raw.obs_names, 
                  columns=adata.raw.var_names)

# # Print the resulting Pandas DataFrame
# print(df)
# print(df.shape)
# num_rows = (df.iloc[:, 3] > 0.0).sum()
# print(num_rows)

df = df.iloc[:4000]

df = df.T

df[df > 0.0] = 1

print(df.sum().sum())

df = df.astype('int8')

print(df.sum().sum())

print("done", df.shape)

# Save the modified DataFrame to a new CSV file
file_name = "output.csv"
df.to_csv(file_name, header=False, index=False, chunksize=500)
print("Output file saved as:", file_name)