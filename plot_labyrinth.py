import numpy as np
import matplotlib.pyplot as plt

def create_colored_table(data, threshold,path):
    fig, ax = plt.subplots(figsize = (8,6))
    ax.set_axis_off()

    # Create a table and add data to it
    table = ax.table(cellText=data, loc='center', cellLoc="center", rowLoc='center', colWidths=[data.shape[1]/1500]*data.shape[1],bbox = [0.02,0.02,1,1])
    # Define color maps
    cmap_below_threshold = plt.get_cmap('Blues')
    cmap_above_threshold = plt.get_cmap('Reds')
    cmap_right_path = plt.get_cmap('Greens')

    # Set cell colors based on values and threshold
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            cell_value = data[i, j]

            # Choose colormap based on threshold
            if cell_value <= threshold:
                cell_color = cmap_below_threshold(cell_value / threshold)
            else:
                cell_color = cmap_above_threshold((cell_value - threshold) / (np.max(data) - threshold))

            table[(i, j)].set_facecolor(cell_color)

    for cell in path:
        table[(cell[0],cell[1])].set_facecolor(cmap_right_path(data[cell[0],cell[1]]/threshold))
    plt.show()
