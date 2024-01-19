import numpy as np

class Agent:
    def __init__(self,maze,actions,epsilon=0.9,discount_factor=0.9,learning_rate=0.9,n_training_episodes=1000):
        self.maze = np.array(maze)
        self.maze_width = maze.shape[1] # number of columns
        self.maze_height = maze.shape[0] # number of rows
        self.epsilon = epsilon
        self.actions = actions
        self.discount_factor = discount_factor
        self.learning_rate = learning_rate
        self.n_training_episodes = n_training_episodes
        self.q_values = np.zeros((self.maze_height, self.maze_width, 4))
    def is_terminal_state(self,current_row_index, current_column_index):
        """
        Function to determine if the specified location is a terminal state
        """
        if self.maze[current_row_index, current_column_index] == 100:
            return True
        else:
            return False

    def get_next_action(self,current_row_index, current_column_index, epsilon):
        """
        Function to choose the next action, according to the epsilon value.
        """
        if np.random.random() < epsilon:
            return np.argmax(self.q_values[current_row_index, current_column_index])
        else:
            return np.random.randint(4)

    def get_next_location(self,current_row_index, current_column_index, action_index):
        """
        Function to get the next location based on the chosen action.
        """
        new_row_index = current_row_index
        new_column_index = current_column_index
        if self.actions[action_index] == 'up' and current_row_index > 0:
            new_row_index -= 1
        elif self.actions[action_index] == 'right' and current_column_index < self.maze_width - 1:
            new_column_index += 1
        elif self.actions[action_index] == 'down' and current_row_index < self.maze_height - 1:
            new_row_index += 1
        elif self.actions[action_index] == 'left' and current_column_index > 0:
            new_column_index -= 1
        return new_row_index, new_column_index

    def get_shortest_path(self,start_row_index, start_column_index):
        """
        Function that will get the shortest path between any location within the city
        that the postman is allowed to travel and the item packaging location.
        """
        if self.is_terminal_state(start_row_index, start_column_index):
            return []
        else:
            current_row_index, current_column_index = start_row_index, start_column_index
            shortest_path = []
            shortest_path.append([current_row_index, current_column_index])
            while not self.is_terminal_state(current_row_index, current_column_index):
                action_index = self.get_next_action(current_row_index, current_column_index, 1.)
                current_row_index, current_column_index = self.get_next_location(current_row_index, current_column_index,
                                                                            action_index)
                shortest_path.append([current_row_index, current_column_index])

        return shortest_path

    def resolve(self):

        for i in range(self.maze_width):
            if self.maze[0, i] == -1:
                starting_location_column = i

        for episode in range(self.n_training_episodes):

            row_index = 0
            column_index = starting_location_column
            while not self.is_terminal_state(row_index, column_index):
                action_index = self.get_next_action(row_index, column_index, self.epsilon)

                old_row_index, old_column_index = row_index, column_index
                row_index, column_index = self.get_next_location(row_index, column_index, action_index)

                gain = self.maze[row_index, column_index]
                old_q_value = self.q_values[old_row_index, old_column_index, action_index]
                temporal_difference = gain + (self.discount_factor * np.max(self.q_values[row_index, column_index])) - old_q_value

                new_q_values = old_q_value + self.learning_rate * temporal_difference
                self.q_values[old_row_index, old_column_index, action_index] = new_q_values

        path = self.get_shortest_path(0, starting_location_column)

        return path