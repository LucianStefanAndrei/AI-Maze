import numpy as np
def is_terminal_state(current_row_index, current_column_index):
  """
  Function to determine if the specified location is a terminal state
  """
  if maze[current_row_index][current_column_index] == 100:
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
