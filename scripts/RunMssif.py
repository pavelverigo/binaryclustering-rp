import os
import sys

# Check if the directory argument is provided
if len(sys.argv) < 2:
    print("Please provide the directory path as an argument.")
    sys.exit(1)

directory = sys.argv[1]

K = 15

for filename in os.listdir(directory):
    if filename.endswith('.csv'):
        file_path = os.path.join(directory, filename)
        # edit
        log_file = f'--massif-out-file="./pavel/pbmcfractioned/{filename}_{K}_.%p.out"'
        cmd = f"valgrind --tool=massif {log_file} --max-snapshots=15 ./out/CmdRunner -THREADS 1 -K {K} -SIM Jaccard -DATA {file_path}"
        print("Exec:", cmd)
        os.system(cmd)