from maze import MazeGenerator
import numpy as np
from Agent import Agent
from plot_labyrinth import create_colored_table

maze_width = 20
maze_height = 20
exit = 100
seed = 24
wall_value = -100
cell_value = -1
starting_location_column = -1

q_values = np.zeros((maze_height, maze_width, 4))
maze_generator = MazeGenerator(wall_value=wall_value, cell_value=cell_value, maze_width=maze_width,
                               maze_height=maze_height, exit=exit, seed=seed)
maze_generator.generate_walls()
maze_generator.print_maze()
maze = maze_generator.get_maze()
maze = np.array(maze)

maze_solve =  Agent(maze)
path = maze_solve.resolve()
# Example usage
threshold_value = wall_value/2  # Set your threshold value here
create_colored_table(maze, threshold_value,path)