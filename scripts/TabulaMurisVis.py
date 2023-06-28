import matplotlib.pyplot as plt
import numpy as np

# Sample data (replace with your own points)
data_points = [
    [1432, 23433, 5.8, "Tongue"],
    [1580, 23433, 6.4, "Thymus"],
    [5355, 23433, 21.5, "Marrow"],
    [2663, 23433, 10.7, "Mammary"],
    [1961, 23433, 8.0, "Pancreas"],
    [981, 23433, 4.0, "Liver"],
    [865, 23433, 3.5, "Kidney"],
    [1718, 23433, 7.1, "Spleen"],
    [2102, 23433, 8.5, "Muscle"],
    [4149, 23433, 16.8, "Colon"],
    [1923, 23433, 7.8, "Lung"],
    [7115, 23433, 28.7, "Heart"],
    [5799, 23433, 23.0, "Brain Neurons"],
    [4762, 23433, 19.2, "Brain Microgolia"],
    [5862, 23433, 23.4, "Fat"],
    [2464, 23433, 10.0, "Skin"],
    [1638, 23433, 6.6, "Bladder"],
    [1391, 23433, 5.6, "Trachea"]
]

print(len(data_points))

# Extract x, y, and labels from data points
x = [point[0] * point[1] for point in data_points]
y = [point[2] for point in data_points]
labels = [point[3] for point in data_points]

plt.figure(figsize=(9, 6)) 

# Plot the points


# Find linear approximation
coefficients = np.polyfit(x, y, 1)
linear_approximation = np.poly1d(coefficients)
pearson_coef = np.corrcoef(x, y)[0, 1]
print("Pearson coefficient:", pearson_coef)
print(linear_approximation[0], linear_approximation[1] * 1024 * 1024)
marg = (max(x) - min(x)) * 0.01
x_line = np.linspace(min(x) - marg, max(x) + marg, 200)
y_line = linear_approximation(x_line)

# Plot the linear approximation
plt.plot(x_line, y_line, color='blue', label='Linear Approximation')

plt.scatter(x, y, s=10, color='red', label='Datasets')

# Label each data point
label_xgap = marg * 0.8  # Adjust the gap as desired
label_ygap = 0.4

adjust = [
    [-10.5 * label_xgap, -1.3 * label_ygap],
    [label_xgap, 1.5 * label_ygap],
    [label_xgap, label_ygap],
    [1.5 * label_xgap, 0.5 * label_ygap],
    [-13 * label_xgap, -1.5 * label_ygap],

    [2.0 * label_xgap, 0.5 * label_ygap],
    [0.7 * label_xgap, 1.5 * label_ygap],
    [1.5 * label_xgap, 0.9 * label_ygap],
    [1.5 * label_xgap, 0.5 * label_ygap],
    [1.1 * label_xgap, 1.1 * label_ygap],

    [1.5 * label_xgap, 0.7 * label_ygap],
    [-9 * label_xgap, -0.5 * label_ygap],
    [0.9 * label_xgap, 1.3 * label_ygap],
    [1.1 * label_xgap, 1.1 * label_ygap],
    [-5 * label_xgap, -1.5 * label_ygap],

    [1.1 * label_xgap, 1.1 * label_ygap],
    [-11 * label_xgap, -1.5 * label_ygap],
    [0 * label_xgap, 1.9 * label_ygap],
]
for i in range(len(x)):
    plt.text(x[i] + adjust[i][0], y[i] - adjust[i][1], labels[i], ha='left', va='center')

# texts = []
# for i in range(len(x)):
#     texts.append(plt.text(x[i], y[i], labels[i]))

# # Adjust text positions to prevent overlap
# adjust_text(texts)


# Set labels and legend
plt.xlabel('Dataset size (C x G)', fontsize=12)
plt.ylabel('Memory used (MiB)', fontsize=12)
plt.legend()

# Save the plot as an image
plt.savefig('muris.png', dpi=300, bbox_inches='tight', format='png')