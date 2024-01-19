import random
from termcolor import colored


class MazeGenerator:
    def __init__(self, wall_value="-100", cell_value="-1", maze_width=20, maze_height=15, exit="100", seed=None):
        self.reward = str(exit)
        random.seed(seed)
        self.length_of_penalty = len(str(wall_value)) + 2
        self.c = str(cell_value)
        self.w = str(wall_value)
        self.b = "u"
        self.maze_width = maze_width
        self.maze_height = maze_height
        self.maze = self.init_maze(self.maze_width, self.maze_height)
        self.starting_width = int(random.random() * self.maze_width)
        self.starting_height = int(random.random() * self.maze_height)
        if self.starting_height == 0:
            self.starting_height += 1
        if self.starting_height == self.maze_height - 1:
            self.starting_height -= 1
        if self.starting_width == 0:
            self.starting_width += 1
        if self.starting_width == self.maze_width - 1:
            self.starting_width -= 1
        self.maze[self.starting_height][self.starting_width] = self.c
        self.walls = []
        self.walls.append([self.starting_height - 1, self.starting_width])
        self.walls.append([self.starting_height, self.starting_width - 1])
        self.walls.append([self.starting_height, self.starting_width + 1])
        self.walls.append([self.starting_height + 1, self.starting_width])

        self.maze[self.starting_height - 1][self.starting_width] = self.w
        self.maze[self.starting_height][self.starting_width - 1] = self.w
        self.maze[self.starting_height][self.starting_width + 1] = self.w
        self.maze[self.starting_height + 1][self.starting_width] = self.w

    def init_maze(self, width, height):
        maze = []
        for i in range(0, height):
            line = []
            for j in range(0, width):
                line.append(self.b)
            maze.append(line)
        return maze

    # colorama needs to be initialized in order to be used
    def print_maze(self):
        for i in range(0, len(self.maze)):
            for j in range(0, len(self.maze[0])):
                if self.maze[i][j] == self.c:
                    print(colored(self.maze[i][j].center(self.length_of_penalty), "white"), end="")
                elif self.maze[i][j] == self.reward:
                    print(colored(self.maze[i][j].center(self.length_of_penalty), "green"), end="")
                elif self.maze[i][j] == "0":
                    print(colored(self.maze[i][j].center(self.length_of_penalty), "blue"), end="")
                else:
                    print(colored(self.maze[i][j].center(self.length_of_penalty), "red"), end="")
            print('\n')

    def surroundingCells(self, rand_wall):
        s_cells = 0
        if self.maze[rand_wall[0] - 1][rand_wall[1]] == self.c:
            s_cells += 1
        if (self.maze[rand_wall[0] + 1][rand_wall[1]] == self.c):
            s_cells += 1
        if (self.maze[rand_wall[0]][rand_wall[1] - 1] == self.c):
            s_cells += 1
        if (self.maze[rand_wall[0]][rand_wall[1] + 1] == self.c):
            s_cells += 1
        return s_cells

    def delete_wall(self, rand_wall):
        for wall in self.walls:
            if (wall[0] == rand_wall[0] and wall[1] == rand_wall[1]):
                self.walls.remove(wall)

    def make_walls(self, width, height):
        for i in range(0, height):
            for j in range(0, width):
                if (self.maze[i][j] == self.b):
                    self.maze[i][j] = self.w

    def create_entrance_exit(self, width, height):
        for i in range(0, width):
            if (self.maze[1][i] == self.c):
                self.maze[0][i] = "-1"
                break
        for i in range(width - 1, 0, -1):
            if (self.maze[height - 2][i] == self.c):
                self.maze[height - 1][i] = self.reward
                break

    def generate_walls(self):
        while (self.walls):
            # Pick a random wall
            rand_wall = self.walls[int(random.random() * len(self.walls)) - 1]

            # Check if it is a left wall
            if (rand_wall[1] != 0):
                if (self.maze[rand_wall[0]][rand_wall[1] - 1] == self.b and self.maze[rand_wall[0]][
                    rand_wall[1] + 1] == self.c):
                    # Find the number of surrounding cells
                    s_cells = self.surroundingCells(rand_wall)

                    if (s_cells < 2):
                        # Denote the new path
                        self.maze[rand_wall[0]][rand_wall[1]] = self.c

                        # Mark the new walls
                        # Upper cell
                        if (rand_wall[0] != 0):
                            if (self.maze[rand_wall[0] - 1][rand_wall[1]] != self.c):
                                self.maze[rand_wall[0] - 1][rand_wall[1]] = self.w
                            if ([rand_wall[0] - 1, rand_wall[1]] not in self.walls):
                                self.walls.append([rand_wall[0] - 1, rand_wall[1]])

                        # Bottom cell
                        if (rand_wall[0] != self.maze_height - 1):
                            if (self.maze[rand_wall[0] + 1][rand_wall[1]] != self.c):
                                self.maze[rand_wall[0] + 1][rand_wall[1]] = self.w
                            if ([rand_wall[0] + 1, rand_wall[1]] not in self.walls):
                                self.walls.append([rand_wall[0] + 1, rand_wall[1]])

                        # Leftmost cell
                        if (rand_wall[1] != 0):
                            if (self.maze[rand_wall[0]][rand_wall[1] - 1] != self.c):
                                self.maze[rand_wall[0]][rand_wall[1] - 1] = self.w
                            if ([rand_wall[0], rand_wall[1] - 1] not in self.walls):
                                self.walls.append([rand_wall[0], rand_wall[1] - 1])

                    # Delete wall
                    for wall in self.walls:
                        if (wall[0] == rand_wall[0] and wall[1] == rand_wall[1]):
                            self.walls.remove(wall)

                    continue

            # Check if it is an upper wall
            if (rand_wall[0] != 0):
                if (self.maze[rand_wall[0] - 1][rand_wall[1]] == self.b and self.maze[rand_wall[0] + 1][
                    rand_wall[1]] == self.c):

                    s_cells = self.surroundingCells(rand_wall)
                    if (s_cells < 2):
                        # Denote the new path
                        self.maze[rand_wall[0]][rand_wall[1]] = self.c

                        # Mark the new walls
                        # Upper cell
                        if (rand_wall[0] != 0):
                            if (self.maze[rand_wall[0] - 1][rand_wall[1]] != self.c):
                                self.maze[rand_wall[0] - 1][rand_wall[1]] = self.w
                            if ([rand_wall[0] - 1, rand_wall[1]] not in self.walls):
                                self.walls.append([rand_wall[0] - 1, rand_wall[1]])

                        # Leftmost cell
                        if (rand_wall[1] != 0):
                            if (self.maze[rand_wall[0]][rand_wall[1] - 1] != self.c):
                                self.maze[rand_wall[0]][rand_wall[1] - 1] = self.w
                            if ([rand_wall[0], rand_wall[1] - 1] not in self.walls):
                                self.walls.append([rand_wall[0], rand_wall[1] - 1])

                        # Rightmost cell
                        if (rand_wall[1] != self.maze_width - 1):
                            if (self.maze[rand_wall[0]][rand_wall[1] + 1] != self.c):
                                self.maze[rand_wall[0]][rand_wall[1] + 1] = self.w
                            if ([rand_wall[0], rand_wall[1] + 1] not in self.walls):
                                self.walls.append([rand_wall[0], rand_wall[1] + 1])

                    # Delete wall
                    for wall in self.walls:
                        if (wall[0] == rand_wall[0] and wall[1] == rand_wall[1]):
                            self.walls.remove(wall)

                    continue

            # Check the bottom wall
            if (rand_wall[0] != self.maze_height - 1):
                if (self.maze[rand_wall[0] + 1][rand_wall[1]] == self.b and self.maze[rand_wall[0] - 1][
                    rand_wall[1]] == self.c):

                    s_cells = self.surroundingCells(rand_wall)
                    if (s_cells < 2):
                        # Denote the new path
                        self.maze[rand_wall[0]][rand_wall[1]] = self.c

                        # Mark the new walls
                        if (rand_wall[0] != self.maze_height - 1):
                            if (self.maze[rand_wall[0] + 1][rand_wall[1]] != self.c):
                                self.maze[rand_wall[0] + 1][rand_wall[1]] = self.w
                            if ([rand_wall[0] + 1, rand_wall[1]] not in self.walls):
                                self.walls.append([rand_wall[0] + 1, rand_wall[1]])
                        if (rand_wall[1] != 0):
                            if (self.maze[rand_wall[0]][rand_wall[1] - 1] != self.c):
                                self.maze[rand_wall[0]][rand_wall[1] - 1] = self.w
                            if ([rand_wall[0], rand_wall[1] - 1] not in self.walls):
                                self.walls.append([rand_wall[0], rand_wall[1] - 1])
                        if (rand_wall[1] != self.maze_width - 1):
                            if (self.maze[rand_wall[0]][rand_wall[1] + 1] != self.c):
                                self.maze[rand_wall[0]][rand_wall[1] + 1] = self.w
                            if ([rand_wall[0], rand_wall[1] + 1] not in self.walls):
                                self.walls.append([rand_wall[0], rand_wall[1] + 1])

                    # Delete wall
                    for wall in self.walls:
                        if (wall[0] == rand_wall[0] and wall[1] == rand_wall[1]):
                            self.walls.remove(wall)

                    continue

            # Check the right wall
            if rand_wall[1] != self.maze_width - 1:
                if (self.maze[rand_wall[0]][rand_wall[1] + 1] == self.b and self.maze[rand_wall[0]][
                    rand_wall[1] - 1] == self.c):

                    s_cells = self.surroundingCells(rand_wall)
                    if s_cells < 2:
                        # Denote the new path
                        self.maze[rand_wall[0]][rand_wall[1]] = self.c

                        # Mark the new walls
                        if rand_wall[1] != self.maze_width - 1:
                            if self.maze[rand_wall[0]][rand_wall[1] + 1] != self.c:
                                self.maze[rand_wall[0]][rand_wall[1] + 1] = self.w
                            if [rand_wall[0], rand_wall[1] + 1] not in self.walls:
                                self.walls.append([rand_wall[0], rand_wall[1] + 1])
                        if (rand_wall[0] != self.maze_height - 1):
                            if self.maze[rand_wall[0] + 1][rand_wall[1]] != self.c:
                                self.maze[rand_wall[0] + 1][rand_wall[1]] = self.w
                            if ([rand_wall[0] + 1, rand_wall[1]] not in self.walls):
                                self.walls.append([rand_wall[0] + 1, rand_wall[1]])
                        if (rand_wall[0] != 0):
                            if (self.maze[rand_wall[0] - 1][rand_wall[1]] != self.c):
                                self.maze[rand_wall[0] - 1][rand_wall[1]] = self.w
                            if ([rand_wall[0] - 1, rand_wall[1]] not in self.walls):
                                self.walls.append([rand_wall[0] - 1, rand_wall[1]])

                    # Delete wall
                    for wall in self.walls:
                        if (wall[0] == rand_wall[0] and wall[1] == rand_wall[1]):
                            self.walls.remove(wall)

                    continue

            # Delete the wall from the list anyway
            for wall in self.walls:
                if (wall[0] == rand_wall[0] and wall[1] == rand_wall[1]):
                    self.walls.remove(wall)

        self.make_walls(self.maze_width, self.maze_height)
        self.create_entrance_exit(self.maze_width, self.maze_height)

    def get_maze(self):
        new_maze = []
        for row in self.maze:
            r = []
            for column in row:
                r.append(int(column))
            new_maze.append(r)
        return new_maze