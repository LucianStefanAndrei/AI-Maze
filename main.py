from maze import MazeGenerator
import numpy as np


maze_width = 35
maze_height = 30
exit = 100
seed = 24
wall_value = -100
cell_value = -1
starting_location_column = -1

actions = ["up","down","left","right"]

epsilon = 0.9
discount_factor = 0.9
learning_rate = 0.9
n_training_episodes = 1000


q_values = np.zeros((maze_height, maze_width, 4))
maze_generator = MazeGenerator(wall_value=wall_value, cell_value=cell_value, maze_width=maze_width,
                               maze_height=maze_height, exit=exit, seed=seed)
maze_generator.generate_walls()
maze_generator.print_maze()
maze = maze_generator.get_maze()
maze = np.array(maze)

def is_terminal_state(current_row_index, current_column_index):
  """
  Function to determine if the specified location is a terminal state
  """
  if maze[current_row_index, current_column_index] == 100:
    return True
  else:
    return False

def get_next_action(current_row_index, current_column_index, epsilon):
  """
  Function to choose the next action, according to the epsilon value.
  """
  if np.random.random() < epsilon:
    return np.argmax(q_values[current_row_index, current_column_index])
  else:
    return np.random.randint(4)

def get_next_location(current_row_index, current_column_index, action_index):
  """
  Function to get the next location based on the chosen action.
  """
  new_row_index = current_row_index
  new_column_index = current_column_index
  if actions[action_index] == 'up' and current_row_index > 0:
    new_row_index -= 1
  elif actions[action_index] == 'right' and current_column_index < maze_width - 1:
    new_column_index += 1
  elif actions[action_index] == 'down' and current_row_index < maze_height - 1:
    new_row_index += 1
  elif actions[action_index] == 'left' and current_column_index > 0:
    new_column_index -= 1
  return new_row_index, new_column_index


def get_shortest_path(start_row_index, start_column_index):
  """
  Function that will get the shortest path between any location within the city
  that the postman is allowed to travel and the item packaging location.
  """
  if is_terminal_state(start_row_index, start_column_index):
    return []
  else:
    current_row_index, current_column_index = start_row_index, start_column_index
    shortest_path = []
    shortest_path.append([current_row_index, current_column_index])
    while not is_terminal_state(current_row_index, current_column_index):
      action_index = get_next_action(current_row_index, current_column_index, 1.)
      current_row_index, current_column_index = get_next_location(current_row_index, current_column_index, action_index)
      shortest_path.append([current_row_index, current_column_index])

  return shortest_path


for i in range(maze_width):
    if maze[0,i] == -1:
        starting_location_column = i


for episode in range(n_training_episodes):

    row_index = 0
    column_index = starting_location_column
    while not is_terminal_state(row_index,column_index):
        action_index = get_next_action(row_index,column_index, epsilon)

        old_row_index, old_column_index = row_index, column_index
        row_index, column_index = get_next_location(row_index,column_index, action_index)

        gain = maze[row_index, column_index]
        old_q_value = q_values[old_row_index, old_column_index, action_index]
        temporal_difference = gain + (discount_factor * np.max(q_values[row_index,column_index])) - old_q_value

        new_q_values = old_q_value + learning_rate * temporal_difference
        q_values[old_row_index, old_column_index, action_index] = new_q_values


path = get_shortest_path(0,starting_location_column)


import matplotlib.pyplot as plt

def create_colored_table(data, threshold,save_path=None):
    fig, ax = plt.subplots(figsize = (8,6))
    ax.set_axis_off()

    # Create a table and add data to it
    table = ax.table(cellText=data, loc='center', cellLoc="center", rowLoc='center', colWidths=[1/1500]*data.shape[1],bbox = [0.02,0.02,1,1])
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

    if save_path:
        plt.savefig(save_path, format='jpg', dpi=300, bbox_inches='tight')
        plt.close()  # Close the plot to prevent it from being displayed
    else:
        plt.show()

# Example usage
save_path = 'labyrinth/table_plot.jpg'
threshold_value = wall_value/2  # Set your threshold value here
create_colored_table(maze, threshold_value,save_path=save_path)