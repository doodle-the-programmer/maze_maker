# ASCII maze generator and solver program with GUI using pygame

import random
from time import sleep
import os
import time
import pygame

class Maze:
    def __init__(self, width=50, length=50):
        self.generated = False
        self.maze_wall = "#"
        self.maze_pwall = "$"  # uncrossable walls
        self.maze_path = " "
        self.maze_start = "S"
        self.maze_end = "E"
        self.width = width
        self.length = length
        self.iteration_limit = self.width * self.length * 10  # Adjusted iteration limit
        if self.iteration_limit > 1000000:
            self.iteration_limit = 1000000
            print("Iteration limit set to 1000000")
        self.iteration = 0
        self.restart_limit = 10  # Increased restart limit
        self.restart_count = 0
        self.maze = []
        self.start_x, self.start_y = random.randrange(1, self.width, 2), random.randrange(1, self.length, 2)
        self.end_x, self.end_y = random.randrange(1, self.width, 2), random.randrange(1, self.length, 2)

    def check_direction_is_good(self, x, y, dir):
        if dir == 0 and x - 2 >= 0 and self.maze[y][x-1] == self.maze_wall and self.maze[y][x-2] == self.maze_wall:
            return True
        elif dir == 1 and x + 2 < self.width and self.maze[y][x+1] == self.maze_wall and self.maze[y][x+2] == self.maze_wall:
            return True
        elif dir == 2 and y - 2 >= 0 and self.maze[y-1][x] == self.maze_wall and self.maze[y-2][x] == self.maze_wall:
            return True
        elif dir == 3 and y + 2 < self.length and self.maze[y+1][x] == self.maze_wall and self.maze[y+2][x] == self.maze_wall:
            return True
        else:
            return False

    def check_direction_end(self, x, y, dir):
        if dir == 0 and x - 1 >= 0 and self.maze[y][x-1] == self.maze_end: return True
        elif dir == 1 and x + 1 < self.width and self.maze[y][x+1] == self.maze_end: return True
        elif dir == 2 and y - 1 >= 0 and self.maze[y-1][x] == self.maze_end: return True
        elif dir == 3 and y + 1 < self.length and self.maze[y+1][x] == self.maze_end: return True
        else: return False

    def generate_maze_path(self):
        while not self.generated and self.restart_count < self.restart_limit:
            x, y = random.randrange(1, self.width, 2), random.randrange(1, self.length, 2)
            self.create_maze()
            stack = [(x, y)]
            self.iteration = 0

            while stack:
                self.iteration += 1
                x, y = stack[-1]
                directions = [0, 1, 2, 3]
                random.shuffle(directions)
                moved = False

                for dir in directions:
                    if self.check_direction_is_good(x, y, dir):
                        if dir == 0:
                            self.maze[y][x-1] = self.maze_path
                            self.maze[y][x-2] = self.maze_path
                            stack.append((x-2, y))
                            moved = True
                        elif dir == 1:
                            self.maze[y][x+1] = self.maze_path
                            self.maze[y][x+2] = self.maze_path
                            stack.append((x+2, y))
                            moved = True
                        elif dir == 2:
                            self.maze[y-1][x] = self.maze_path
                            self.maze[y-2][x] = self.maze_path
                            stack.append((x, y-2))
                            moved = True
                        elif dir == 3:
                            self.maze[y+1][x] = self.maze_path
                            self.maze[y+2][x] = self.maze_path
                            stack.append((x, y+2))
                            moved = True
                        break

                if not moved:
                    stack.pop()

                if self.check_direction_end(x, y, dir):
                    self.generated = True
                    break

                if self.iteration > self.iteration_limit:
                    self.restart_count += 1
                    self.iteration = 0  # Reset iteration counter
                    print(f"Restarting maze generation (attempt {self.restart_count})")
                    break

            if not self.generated:
                print(f"Failed attempt {self.restart_count}, restarting. Iterations: {self.iteration}")
                self.iteration = 0

    def create_maze(self):
        self.maze = [[self.maze_wall for i in range(self.width)] for j in range(self.length)]
        for i in range(self.length):
            for j in range(self.width):
                if i == 0 or i == self.length-1 or j == 0 or j == self.width-1:
                    self.maze[i][j] = self.maze_pwall
                else:
                    self.maze[i][j] = self.maze_wall
        self.maze[self.start_y][1] = self.maze_start
        self.maze[self.end_y][self.width-2] = self.maze_end

    def print_maze(self):
        print("Maze iteration: ", self.iteration, " Maze restarts: ", self.restart_count)
        for i in range(self.length):
            for j in range(self.width):
                print(self.maze[i][j], end=" ")
            print()

    def save_maze_to_file(self, filename):
        with open(filename, 'w') as f:
            for i in range(self.length):
                for j in range(self.width):
                    f.write(self.maze[i][j])
                f.write('\n')

    def load_maze_from_file(self, filename):
        with open(filename, 'r') as f:
            self.maze = [list(line.strip()) for line in f.readlines()]
        self.length = len(self.maze)
        self.width = len(self.maze[0]) if self.length > 0 else 0

    def display_maze(self):
        pygame.init()
        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.display.set_caption("Maze")

        screen_width, screen_height = screen.get_size()
        cell_width = screen_width // self.width
        cell_height = screen_height // self.length

        colors = {
            self.maze_wall: (0, 0, 0),
            self.maze_pwall: (255, 0, 0),
            self.maze_start: (0, 255, 0),
            self.maze_end: (0, 0, 255),
            self.maze_path: (255, 255, 255)
        }

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            screen.fill((255, 255, 255))

            for y in range(self.length):
                for x in range(self.width):
                    color = colors.get(self.maze[y][x], (255, 255, 255))
                    pygame.draw.rect(screen, color, (x * cell_width, y * cell_height, cell_width, cell_height))

            pygame.display.flip()

        pygame.quit()

# Main loop to take user inputs and generate the maze
if not os.path.exists('mazes'):
    os.makedirs('mazes')

while True:
    print('Maze algorithm running...')
    print('1. Create a new maze')
    print('2. Open an existing maze')
    print('3. Quit')
    choice = input("Enter your choice (1, 2, or 3): ")

    if choice == '1':
        width = int(input("Enter width of maze: "))
        length = int(input("Enter length of maze: "))
        maze = Maze(width, length)
        maze.generate_maze_path()
        if maze.generated:
            os.system('cls' if os.name == 'nt' else 'clear')
            filename = f"mazes/maze_{width}x{length}_{int(time.time())}.txt"
            maze.save_maze_to_file(filename)
            print(f"Maze saved to {filename}")
            maze.display_maze()
        else:
            print(f"Failed to generate maze in {maze.iteration} iterations and {maze.restart_count} resets.")
            sleep(3)
            os.system('cls' if os.name == 'nt' else 'clear')
    elif choice == '2':
        maze_files = [f for f in os.listdir('mazes') if os.path.isfile(os.path.join('mazes', f))]
        if maze_files:
            print("Available mazes:")
            for i, file in enumerate(maze_files):
                print(f"{i + 1}. {file}")
            file_choice = int(input("Enter the number of the maze to open: ")) - 1
            if 0 <= file_choice < len(maze_files):
                filename = os.path.join('mazes', maze_files[file_choice])
                maze = Maze()
                maze.load_maze_from_file(filename)
                maze.display_maze()
            else:
                print("Invalid choice. Returning to main menu.")
                sleep(3)
                os.system('cls' if os.name == 'nt' else 'clear')
        else:
            print("No maze files found. Returning to main menu.")
            sleep(3)
            os.system('cls' if os.name == 'nt' else 'clear')
    elif choice == '3':
        print("Exiting program.")
        break
    else:
        print("Invalid choice. Please enter 1, 2, or 3.")
        sleep(3)
        os.system('cls' if os.name == 'nt' else 'clear')
