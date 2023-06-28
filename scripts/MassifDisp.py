import msparser
import matplotlib.pyplot as plt
import numpy as np

data = msparser.parse_file('seurat_new.out')

peak_index = data['peak_snapshot_index']

peak_snapshot = data['snapshots'][peak_index]

print(peak_snapshot['mem_heap'] / 1024 / 1024)


# cut = 0
cut = 21
cutted_data = data['snapshots'][cut:]
# regions = [0, 55, 70, len(cutted_data)]
regions = [0, 12, 23, len(cutted_data)]


colors = ['springgreen', 'lightskyblue', 'lightpink']
labels = [
    'Preprocessing input file',
    # 'Calculating neighborhood graph',
    'PCA + K-nearest neighbor graph construction',
    'Clustering'
]

x = []
y = []
m = cutted_data[0]['mem_heap'] / 1024 / 1024
for snapshot in cutted_data:
    x += [snapshot['time'] / 1000]
    y += [snapshot['mem_heap'] / 1024 / 1024 - m] 
    print(snapshot['time'] / 1000,  snapshot['mem_heap'] / 1024 / 1024)

fig, ax = plt.subplots(figsize=(9, 6))

for i in range(3):
    i1 = regions[i]
    i2 = regions[i + 1] + 1
    plt.fill_between(x[i1:i2], y[i1:i2], color=colors[i], alpha=0.7, label=labels[i])

off_x = 100
off_y = 0.1
# off_x = 1
# off_y = 0.1
# ax.set_ylim(bottom=off_y, top=y[-1] + off_x)

plt.plot(x, y, 'o', color='crimson', markersize=2)
plt.plot(x, y, '-', color='black')

# Set labels and legend
plt.xlabel('Elapsed Time (s)', fontsize=12)
plt.ylabel('Memory used (MiB)', fontsize=12)
ax.locator_params(axis='y', nbins=20)
ax.locator_params(axis='x', nbins=20)
# plt.legend()
ax.legend()

# Save the plot as an image
plt.savefig('memoryplot.png', dpi=300, bbox_inches='tight', format='png')