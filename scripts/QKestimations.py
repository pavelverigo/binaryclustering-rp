import matplotlib.pyplot as plt
import numpy as np

# Sample data (replace with your own points)
# data_points = [
#     [1432, 23433, 5.8, "Tongue"],
#     [1580, 23433, 6.4, "Thymus"],
#     [5355, 23433, 21.5, "Marrow"],
#     [2663, 23433, 10.7, "Mammary"],
#     # [1961, 23433, 8.0, "Pancreas"],
#     [981, 23433, 4.0, "Liver"],
#     [865, 23433, 3.5, "Kidney"],
#     [1718, 23433, 7.1, "Spleen"],
#     [2102, 23433, 8.5, "Muscle"],
#     [4149, 23433, 16.8, "Colon"],
#     [1923, 23433, 7.8, "Lung"],
#     [7115, 23433, 28.7, "Heart"],
#     [5799, 23433, 23.0, "Brain_Neurons"],
#     [4762, 23433, 19.2, "Brain_Microgolia"],
#     [5862, 23433, 23.4, "Fat"],
#     [2464, 23433, 10.0, "Skin"],
#     # [1638, 23433, 6.6, "Bladder"],
#     # [1391, 23433, 5.6, "Trachea"]
# ]

def draw(data_points, name, K, color):
    print(len(data_points))

    # Extract x, y, and labels from data points
    x = [point[0] for point in data_points]
    y = [point[1] for point in data_points]

    
    # Plot the points
    plt.scatter(x, y, s=15, color=color)

    # Find linear approximation
    coefficients = np.polyfit(x, y, 1)
    linear_approximation = np.poly1d(coefficients)
    pearson_coef = np.corrcoef(x, y)[0, 1]
    print("Pearson coefficient:", pearson_coef)
    print(linear_approximation[0], linear_approximation[1] * 1024 * 1024, linear_approximation[1] * 1024 * 1024 / K)
    x_line = np.linspace(min(x), max(x), 200)
    y_line = linear_approximation(x_line)

    # Plot the linear approximation
    plt.plot(x_line, y_line, color=color, label=name)

plt.figure(figsize=(9, 6)) 

data_points5 = [
    [540, 0.4],
    [1080, 1.0],
    [1620, 1.3],
    [2160, 1.8],
    [2700, 2.2],
]

draw(data_points5, "K = 5", 5, 'cyan')

data_points10 = [
    [540, 0.8],
    [1080, 1.5],
    [1620, 2.3],
    [2160, 3.2],
    [2700, 3.9],
]

draw(data_points10, "K = 10", 10, 'orange')

data_points15 = [
    [540, 1.0],
    [1080, 2.1],
    [1620, 3.3],
    [2160, 4.4],
    [2700, 5.8],
]

draw(data_points15, "K = 15", 15, 'green')

# Set labels and legend
plt.xlabel('Number of cells', fontsize=12)
plt.ylabel('Memory used (MiB)', fontsize=12)
plt.legend()

# Save the plot as an image
plt.savefig('kkplot.png', dpi=300, bbox_inches='tight', format='png')