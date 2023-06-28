# Building using CMake

```
cmake -B out

cmake --build out
```

for clang++ use

```
cmake -DCMAKE_C_COMPILER=/usr/bin/clang -DCMAKE_CXX_COMPILER=/usr/bin/clang++ -GNinja -DCMAKE_BUILD_TYPE=Release -B out
```

# Running on dataset

```
./out/CmdRunner -SIM Jaccard -DATA data/hg19/expr.csv
```

# Valgrind

```
valgrind --tool=massif --time-unit=ms ./out/CmdRunner -SIM Jaccard -DATA data/hg19/expr.csv
```

for R

```
R -d "valgrind --tool=massif --time-unit=ms" --vanilla < your_script.R
```

# Datasets and scripts

Our binary takes datasets in binarized format, you can find under scripts/CSVmanip, different python scripts which will delete cells/genes names and binarize data