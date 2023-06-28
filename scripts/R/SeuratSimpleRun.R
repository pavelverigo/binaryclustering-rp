library(Seurat)

# Sys.sleep(30)

pbmc.data <- Read10X(data.dir = "./data/hg19/")
pbmc <- CreateSeuratObject(counts = pbmc.data, project = "pbmc3k", min.cells = 3, min.features = 200)
pbmc <- NormalizeData(pbmc)
all.genes <- rownames(pbmc)
pbmc <- ScaleData(pbmc, features = all.genes)
pbmc <- RunPCA(pbmc, features = all.genes)
pbmc <- FindNeighbors(pbmc, features = all.genes)
pbmc <- FindClusters(pbmc, resolution = 0.2)

# Access the cluster assignments
cluster_assignment <- pbmc$seurat_clusters

# Print the clusters
print(table(cluster_assignment))