cmake -DCMAKE_C_COMPILER=/usr/bin/clang -DCMAKE_CXX_COMPILER=/usr/bin/clang++ -GNinja -DCMAKE_BUILD_TYPE=Release -B out

# Building using CMake

cmake -B out

cmake --build out

./out/CmdRunner -THREADS 2 -SIM Jaccard

valgrind --tool=massif --time-unit=ms ./out/CmdRunner -THREADS 1 -SIM Jaccard

valgrind --tool=massif --time-unit=ms ./out/CmdRunner -THREADS 1 -SIM Jaccard -DATA data/hg19/expr.csv


R -d "valgrind --tool=massif --time-unit=ms" --vanilla < your_script.R