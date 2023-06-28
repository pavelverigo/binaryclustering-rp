library(Rcpp)

Sys.setenv(CXX = "/usr/bin/g++")
Sys.setenv(PKG_CXXFLAGS = "-fdiagnostics-color=always -Ofast",
           PKG_CPPFLAGS = "-I/home/m/Downloads/vcpkg/installed/x64-linux/include -I/usr/local/include -I/usr/share/R/include -I/home/m/R/x86_64-pc-linux-gnu-library/4.3/Rcpp/include",
           PKG_LIBS = "-L/home/m/Downloads/vcpkg/installed/x64-linux/lib -L/usr/local/lib /home/m/R/x86_64-pc-linux-gnu-library/4.3/Rcpp/libs/Rcpp.so -ligraph -lboost_system -lboost_thread -lR -pthread")

currentDir <- "/home/m/rp/workspace/binary_clustering_v2/binaryclustering/Binary clustering/"

sourceCpp(file.path(currentDir, "BinaryClustering.cpp"))

dataPath <- file.path(currentDir, "data/Brain/brain.csv")
outputPath <- file.path(currentDir, "output/comparing_metrics/brain")
metrics <- c("Bray-Curtis", "Ochiai", "Dice", "Euclidean", "Manhattan", "Jaccard", "Kulsinski", "Pearson", "YuleQ", "Zero")

sampleSize <- 10

run_binary <- function(dataPath, sampleSize, outputPath, metrics, write = TRUE) {

    # Read file for binary algorithm
    read(dataPath)

    runtimes_binary <- numeric(sampleSize)

    randomMetrics <- sample(metrics)

    for (i in 1:length(metrics)) {
        startTime <- Sys.time()

        binaryClusters <- clusterBinary(randomMetrics[i], "Louvain", 30, 0.2)

        endTime <- Sys.time()

        runtimes_binary[i] <- executionTime <- difftime(endTime, startTime, units = "secs")
        if(write) {
            write(executionTime, file = file.path(outputPath, paste(randomMetrics[i], ".txt")), append = TRUE)
        }
    }
    
}

for (i in 1:2) {
    run_binary(dataPath, sampleSize, outputPath, metrics, write = FALSE)
}

for (i in 1:sampleSize) {
    if (!dir.exists(outputPath)) {
        dir.create(outputPath, recursive = TRUE)
    }
    run_binary(dataPath, sampleSize, outputPath, metrics)
    print(paste("iteration: ", i))
    print("==================================================")
}