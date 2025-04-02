import pygame
from queue import PriorityQueue
from pygame import mixer

''' CAN ADD A LOCAL MUSIC/SOUND FILE IF DESIRED

# Instantiate mixer
mixer.init()

# Load audio file
mixer.music.load('soundtrack.mp3')

# Set preferred volume
mixer.music.set_volume(1)

# Play the music
mixer.music.play()'

'''

pygame.init()
# RGB Color Codes
button_text_color = (2,255,20)
button_background_color = (0,0,0)
reset_button_text_color = (255,255,255)
reset_button_background_color = (255,0,0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
ORANGE = (255, 165 ,0)
GREEN = (57, 255, 20)
YELLOW = (255, 255, 51)
CYAN = (90, 229, 250)
PINK = (255, 16, 240)

def drawTextcenter(text,font,screen,x,y,color):
    textobj=font.render(text,True,color)
    textrect=textobj.get_rect(center=((int)(x),(int)(y)))
    screen.blit(textobj,textrect)

def drawText(text, font, surface, x, y,color):
    textobj=font.render(text, 1, color)
    textrect=textobj.get_rect()
    textrect.topleft=(x, y)
    surface.blit(textobj, textrect)

class Button(object):
    def __init__(self,x,y,width,height,text_color,background_color,text):
        self.rect=pygame.Rect(x,y,width,height)
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.text=text
        self.text_color=text_color
        self.background_color=background_color
        self.angle=0

    def check(self):
        return self.rect.collidepoint(pygame.mouse.get_pos())

    def draw(self, window):
        pygame.draw.rect(window, self.background_color, (self.rect), 0)
        drawTextcenter(self.text, pygame.font.SysFont('Sansfrontbold', 30), window, self.x + self.width / 2, self.y + self.height / 2, self.text_color)
        pygame.draw.rect(window, self.text_color, self.rect, 3)

# Creating button objects
button_bfs = Button(0, 715, 130, 50, PINK, BLACK, "BFS")
button_dfs = Button(140, 715, 130, 50, CYAN, BLACK, "DFS")
button_dijkstra = Button(280, 715, 130, 50, GREEN, BLACK, "DIJKSTRA")
button_astar = Button(420, 715, 130, 50, YELLOW, BLACK, "A STAR")
button_greedy = Button(560, 715, 130, 50, ORANGE, BLACK, "GREEDY")
button_reset = Button(700, 715, 99, 50,WHITE, RED, "RESET")

# Creating a window
window_height = 700
window_width = 800
window = pygame.display.set_mode((window_width, window_height+80))
pygame.display.set_caption("Pathfinding and Search Algorithms Visualizer")

# RGB Color Codes
start_color = (30, 144, 255)
end_color = (0, 206, 209)
visited_color = (200, 0, 0)
visiting_color = (0, 200, 0)
path_color = (255, 215, 0)
barrier_color = (110, 110, 110)
normal_color = (50, 50, 50)
line_color = (0, 0, 0)
bar_color = (165,155,155)

class Node:
    def __init__(self, row, column, height, width, total_rows):
        self.row = row
        self.column = column
        self.x = width * column
        self.y = height * row
        self.height = height
        self.width = width
        self.color = normal_color
        self.neighbors = []
        self.total_rows = total_rows

    def get_position(self):
        return self.row, self.column

    def is_open(self):
        return self.color == visited_color

    def is_close(self):
        return self.color == visiting_color

    def is_barrier(self):
        return self.color == barrier_color

    def is_start(self):
        return self.color == start_color

    def is_end(self):
        return self.color == end_color

    def set_open(self):
        self.color = visited_color

    def set_close(self):
        self.color = visiting_color

    def set_barrier(self):
        self.color = barrier_color

    def set_start(self):
        self.color = start_color

    def set_end(self):
        self.color = end_color

    def set_path(self):
        self.color = path_color

    def reset(self):
        self.color = normal_color

    def __lt__(self, other):
        return False

    def update_neighbors(self, grid):
        # Checking if the node above it is a neighbor
        if self.row > 0 and not grid[self.row - 1][self.column].is_barrier():
            self.neighbors.append(grid[self.row - 1][self.column])

        # Checking if the node below it is a neighbor
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.column].is_barrier():
            self.neighbors.append(grid[self.row + 1][self.column])

        # Checking if the node left to it is a neighbor
        if self.column > 0 and not grid[self.row][self.column - 1].is_barrier():
            self.neighbors.append(grid[self.row][self.column - 1])

        # Checking if the node right to it is a neighbor
        if self.column < self.total_rows - 1 and not grid[self.row][self.column + 1].is_barrier():
            self.neighbors.append(grid[self.row][self.column + 1])

    # Draws a node on the window
    def draw_node(self, window):
        pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.height))

# Draws a line on the window
def draw_line(window, window_height, window_width, rows, columns):
    node_height = window_height // rows
    node_width = window_width // columns
    # Draws horizontal lines
    for i in range(rows):
        pygame.draw.line(window, line_color, (0, i * node_height), (window_width, i * node_height))
    # Draws vertical lines
    for i in range(columns):
        pygame.draw.line(window, line_color, (i * node_width, 0), (i * node_width, window_height))

# Creates a grid and stores it through a data structure
def create_grid(window_height, window_width, rows, columns):
    grid = []
    node_height = window_height // rows
    node_width = window_width // columns
    for i in range(rows):
        grid.append([])
        for j in range(columns):
            node = Node(i, j, node_height, node_width, rows)
            grid[i].append(node)
    return grid

# Draws the grid on the window
def draw_grid(window, window_height, window_width, grid, rows, columns):
    # Draws all nodes
    for row in grid:
        for node in row:
            node.draw_node(window)
    # Draws all lines
    draw_line(window, window_height, window_width, rows, columns)
    pygame.display.update()

# Retrieves the position clicked by the user on the window
def get_clicked_position(window_height, window_width, rows, columns, position):
    node_height = window_height // rows
    node_width = window_width // columns
    x, y = position
    row = y // node_height
    col = x // node_width
    return row, col

# Constructs the shortest path between the start and end node
def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.set_path()
        draw()

# Manhattan distance
def h(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    return abs(x2 - x1) + abs(y2 - y1)

def A_Star_Search(draw, grid, start, end):
    count = 0
    visited = PriorityQueue()
    visited.put((0, count, start))
    path = {}
    g = {node: float("inf") for row in grid for node in row}
    g[start] = 0
    f = {node: float("inf") for row in grid for node in row}
    f[start] = h(start.get_position(), end.get_position())

    visited_hash = {start}
    while not visited.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = visited.get()[2]
        visited_hash.remove(current)

        if current == end:
            reconstruct_path(path, end, draw)
            return True

        for neighbor in current.neighbors:
            temp_g = g[current] + 1

            if temp_g < g[neighbor]:
                path[neighbor] = current
                g[neighbor] = temp_g
                f[neighbor] = temp_g + h(neighbor.get_position(), end.get_position())
                if neighbor not in visited_hash:
                    count += 1
                    visited.put((f[neighbor], count, neighbor))
                    visited_hash.add(neighbor)
                    neighbor.set_open()

        draw()

        if current != start:
            current.set_close()

    return False

def Dijkstra(draw, grid, start, end):
    visited = {node: False for row in grid for node in row}
    distance = {node: float("inf") for row in grid for node in row}
    distance[start] = 0
    came_from = {}
    priority_queue = PriorityQueue()
    priority_queue.put((0, start))
    while not priority_queue.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = priority_queue.get()[1]

        if visited[current]:
            continue

        visited[current] = True

        if current == end:
            reconstruct_path(came_from, end, draw)
            return True

        for neighbor in current.neighbors:
            weight = 1
            if distance[current] + weight < distance[neighbor]:
                came_from[neighbor] = current
                distance[neighbor] = distance[current] + weight
                priority_queue.put((distance[neighbor], neighbor))
            if neighbor != end and neighbor != start and not visited[neighbor]:
                neighbor.set_open()

        draw()

        if current != start:
            current.set_close()

    return False

def Greedy_Best_First_Search(draw, grid, start, end):
    count = 0
    priority_queue = PriorityQueue()
    priority_queue.put((0, count, start))
    came_from = {}
    f_score = {spot: float("inf") for row in grid for spot in row}
    f_score[start] = h(start.get_position(), end.get_position())
    priority_queue_hash = {start}

    while not priority_queue.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = priority_queue.get()[2]
        priority_queue_hash.remove(current)

        if current == end:
            reconstruct_path(came_from, end, draw)
            end.set_end()
            start.set_start()
            return True

        for neighbor in current.neighbors:
            temp_f_score = h(neighbor.get_position(), end.get_position())
            if temp_f_score < f_score[neighbor]:
                came_from[neighbor] = current
                f_score[neighbor] = temp_f_score

                if neighbor not in priority_queue_hash:
                    count += 1
                    priority_queue.put((f_score[neighbor], count, neighbor))
                    priority_queue_hash.add(neighbor)
                    neighbor.set_open()

        draw()

        if current != start:
            current.set_close()

    return False

def Breadth_First_Search(draw, start, end):
    visited = [start]
    queue = [start]
    path = {}
    while queue:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = queue.pop(0)

        if current == end:
            reconstruct_path(path, end, draw)
            return True

        for neighbor in current.neighbors:
            if neighbor not in visited:
                path[neighbor] = current
                visited.append(neighbor)
                queue.append(neighbor)
                neighbor.set_open()

        draw()

        if current != start:
            current.set_close()

    return False

def Depth_First_Search(draw, start, end):
    visited = {start}
    stack = [start]
    path = {}
    while stack:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = stack.pop()

        if current == end:
            reconstruct_path(path, end, draw)
            return True

        if current not in visited:
            visited.add(current)
            if current != start:
                current.set_open()

        for neighbor in current.neighbors:
            if neighbor not in visited:
                stack.append(neighbor)
                path[neighbor] = current

        draw()

        if current != start:
            current.set_close()

    return False

def main(window, window_width):
    window.fill(bar_color);
    rows = 50
    columns = 50
    grid = create_grid(window_height, window_width, rows, columns)

    # Tells if the start node is placed and points to the start node
    start = None
    # Tells if the end node is placed and points to the end node
    end = None

    # Tells if the window is still running
    run = True
    # Tells if the visualizing tool has started
    started = None

    while run:


        draw_grid(window, window_height, window_width, grid, rows, columns)
        button_astar.draw(window)
        button_greedy.draw(window)
        button_bfs.draw(window)
        button_dijkstra.draw(window)
        button_dfs.draw(window)
        button_reset.draw(window)

        for event in pygame.event.get():
            # User clicks the quit button on the window
            if event.type == pygame.QUIT:
                run = False

            # User clicks left mouse
            if pygame.mouse.get_pressed()[0] and not started:
                position = pygame.mouse.get_pos()    # Returns the x and y position of the mouse button clicked
                row, col = get_clicked_position(window_height, window_width, rows, columns, position)
                # User clicks on grid
                if row <= (rows - 1):
                    node = grid[row][col]
                # Creating a start node
                    if not start and node != end:
                        start = node
                        start.set_start()

                # Creating an end node
                    elif not end and node != start:
                        end = node
                        end.set_end()

                # Creating barrier nodes
                    elif node != end and node != start:
                        node.set_barrier()

            # User clicks right mouse
            elif pygame.mouse.get_pressed()[2] and not started:
                position = pygame.mouse.get_pos()  # Returns the x and y position of the mouse click
                row, col = get_clicked_position(window_height, window_width, rows, columns, position)
                # User click on grid
                if row <= (rows - 1):
                    node = grid[row][col]
                    node.reset()
                    if node == start:
                        start = None
                    elif node == end:
                        end = None

            # User clicks right mouse
            if event.type == pygame.MOUSEBUTTONDOWN:
                # User clicks A star button
                if button_astar.check() == True and start and end and not started:
                    started = True
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)

                    found = A_Star_Search(lambda: draw_grid(window, window_height, window_width, grid, rows, columns), grid, start, end)
                    start.set_start()
                    end.set_end()
                    if not found:
                        pass

                # User clicks Dijkstra button
                elif button_dijkstra.check() == True and start and end and not started:
                    started = True
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)

                    found = Dijkstra(lambda: draw_grid(window, window_height, window_width, grid, rows, columns), grid, start, end)
                    start.set_start()
                    end.set_end()
                    if not found:
                        pass

                # User clicks Greedy button
                elif button_greedy.check() == True and start and end and not started:
                    started = True
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)

                    found = Greedy_Best_First_Search(lambda: draw_grid(window, window_height, window_width, grid, rows, columns), grid, start, end)
                    start.set_start()
                    end.set_end()
                    if not found:
                        pass

                # User clicks Breadth first search button
                elif button_bfs.check() == True and start and end and not started:
                    started = True
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)

                    found = Breadth_First_Search(lambda: draw_grid(window, window_height, window_width, grid, rows, columns), start, end)
                    start.set_start()
                    end.set_end()
                    if not found:
                        pass

                # User presses clicks Depth first search button
                elif button_dfs.check() == True and start and end and not started:
                    started = True
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)

                    found = Depth_First_Search(lambda: draw_grid(window, window_height, window_width, grid, rows, columns), start, end)
                    start.set_start()
                    end.set_end()
                    if not found:
                        pass

                # User clicks Reset button
                if button_reset.check() == True:
                    start = None
                    end = None
                    started = None
                    grid = create_grid(window_height, window_width, rows, columns)

        pygame.display.update()

    # Closes the window
    pygame.quit()

main(window, window_width)