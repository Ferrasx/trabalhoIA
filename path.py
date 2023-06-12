import pygame
import time
import queue

# Dimensões da janela do jogo
WIDTH = 250
HEIGHT = 250

# Cores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Tamanho do labirinto
MAZE_WIDTH = 10
MAZE_HEIGHT = 10
CELL_SIZE = 25

# Algoritmos de busca
ALGORITHM_ASTAR = "A*"
ALGORITHM_BFS = "Busca em Largura"
ALGORITHM_DFS = "Busca em Profundidade"

# Inicialização do Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Classe para representar o labirinto
class Maze:
    def __init__(self):
        self.maze = [[0] * MAZE_HEIGHT for _ in range(MAZE_WIDTH)]
        self.start = (0, 0)
        self.end = (MAZE_WIDTH - 1, MAZE_HEIGHT - 1)
        self.path = []
        self.algorithm = ALGORITHM_ASTAR

    def generate_maze(self):
        # Gera o labirinto aleatoriamente (para fins de demonstração, vamos deixar tudo em branco)
        for x in range(MAZE_WIDTH):
            for y in range(MAZE_HEIGHT):
                self.maze[x][y] = 0

    def draw(self):
        # Desenha o labirinto na tela
        screen.fill(BLACK)
        for x in range(MAZE_WIDTH):
            for y in range(MAZE_HEIGHT):
                rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                if self.maze[x][y] == 0:
                    pygame.draw.rect(screen, WHITE, rect)
                elif self.maze[x][y] == 1:
                    pygame.draw.rect(screen, BLACK, rect)
                elif self.maze[x][y] == 2:
                    pygame.draw.rect(screen, RED, rect)
                elif self.maze[x][y] == 3:
                    pygame.draw.rect(screen, GREEN, rect)
                elif self.maze[x][y] == 4:
                    pygame.draw.rect(screen, BLUE, rect)

    def set_wall(self, x, y):
        # Define uma parede no labirinto
        if self.start != (x, y) and self.end != (x, y):
            self.maze[x][y] = 1

    def remove_wall(self, x, y):
        # Remove uma parede do labirinto
        if self.start != (x, y) and self.end != (x, y):
            self.maze[x][y] = 0

    def set_start(self, x, y):
        # Define a posição inicial do personagem
        self.start = (x, y)

    def set_end(self, x, y):
        # Define a posição final do personagem
        self.end = (x, y)

    def set_algorithm(self, algorithm):
        # Define o algoritmo de busca a ser utilizado
        self.algorithm = algorithm

    def reset_path(self):
        # Reseta o caminho percorrido pelo personagem
        self.path = []

    def solve_maze(self):
        if self.algorithm == ALGORITHM_ASTAR:
            self.path = self.astar_search()
        elif self.algorithm == ALGORITHM_BFS:
            self.path = self.bfs_search()
        elif self.algorithm == ALGORITHM_DFS:
            self.path = self.dfs_search()

    def bfs_search(self):
        # Implementação do algoritmo de busca em largura (BFS)
        node = 0
        processed_nodes = 0
        visited = set()
        queue = [(self.start, [])]

        while queue:
            current, path = queue.pop(0)
            processed_nodes += 1
            
            x, y = current
            if current == self.end:
                print(node, "nós visitados")
                print(processed_nodes, "nós processados")
                return path

            if current not in visited:
                visited.add(current)
                node += 1
                # Checa os vizinhos
                if x > 0 and self.maze[x - 1][y] == 0:
                    queue.append(((x - 1, y), path + [(x - 1, y)]))
                if x < MAZE_WIDTH - 1 and self.maze[x + 1][y] == 0:
                    queue.append(((x + 1, y), path + [(x + 1, y)]))
                if y > 0 and self.maze[x][y - 1] == 0:
                    queue.append(((x, y - 1), path + [(x, y - 1)]))
                if y < MAZE_HEIGHT - 1 and self.maze[x][y + 1] == 0:
                    queue.append(((x, y + 1), path + [(x, y + 1)]))
        
        return []

    def dfs_search(self):
        # Implementação do algoritmo de busca em profundidade (DFS)
        node = 0
        processed_nodes = 0
        visited = set()
        stack = [(self.start, [])]

        while stack:
            current, path = stack.pop()
            x, y = current
            processed_nodes += 1

            if current == self.end:
                print(node, "nós visitados")
                print(processed_nodes, "nós processados")
                return path

            if current not in visited:
                visited.add(current)
                node += 1


                # Checa os vizinhos
                if x > 0 and self.maze[x - 1][y] == 0:
                    stack.append(((x - 1, y), path + [(x - 1, y)]))
                if x < MAZE_WIDTH - 1 and self.maze[x + 1][y] == 0:
                    stack.append(((x + 1, y), path + [(x + 1, y)]))
                if y > 0 and self.maze[x][y - 1] == 0:
                    stack.append(((x, y - 1), path + [(x, y - 1)]))
                if y < MAZE_HEIGHT - 1 and self.maze[x][y + 1] == 0:
                    stack.append(((x, y + 1), path + [(x, y + 1)]))

        return []

    def astar_search(self):
        # Implementação do algoritmo A*
        processed_nodes = 0
        node = 0
        start = self.start
        end = self.end

        open_list = [(start, 0)]
        came_from = {}
        g_score = {start: 0}
        f_score = {start: self.heuristic(start, end)}

        while open_list:
            current, _ = min(open_list, key=lambda x: f_score[x[0]])
            open_list = [x for x in open_list if x[0] != current]
            processed_nodes += 1

            if current == end:
                print(node, "nós visitados")
                print(processed_nodes, "nós processados")
                return self.reconstruct_path(came_from, current)

            neighbors = self.get_neighbors(current)
            for neighbor in neighbors:
                tentative_g_score = g_score[current] + 1
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + self.heuristic(neighbor, end)
                    if (neighbor, 0) not in open_list:
                        node += 1
                        open_list.append((neighbor, 0))

        return []

    def heuristic(self, current, end):
        # Heurística (distância de Manhattan) utilizada no A*
        return abs(current[0] - end[0]) + abs(current[1] - end[1])

    def get_neighbors(self, current):
        # Obtém os vizinhos válidos de uma posição no labirinto
        neighbors = []
        x, y = current

        if x > 0 and self.maze[x - 1][y] == 0:
            neighbors.append((x - 1, y))
        if x < MAZE_WIDTH - 1 and self.maze[x + 1][y] == 0:
            neighbors.append((x + 1, y))
        if y > 0 and self.maze[x][y - 1] == 0:
            neighbors.append((x, y - 1))
        if y < MAZE_HEIGHT - 1 and self.maze[x][y + 1] == 0:
            neighbors.append((x, y + 1))

        return neighbors

    def reconstruct_path(self, came_from, current):
        # Reconstrói o caminho percorrido pelo personagem
        path = []
        while current in came_from:
            path.append(current)
            current = came_from[current]
        path.append(current)
        path.reverse()
        return path

# Função principal do jogo
def game_loop():
    maze = Maze()
    maze.generate_maze()

    running = True
    dragging_start = False
    dragging_end = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                cell_x = mouse_pos[0] // CELL_SIZE
                cell_y = mouse_pos[1] // CELL_SIZE

                # Clique esquerdo para adicionar/remover parede
                if event.button == 1:
                    if maze.maze[cell_x][cell_y] == 0:
                        maze.set_wall(cell_x, cell_y)
                    else:
                        maze.remove_wall(cell_x, cell_y)

                # Clique direito para definir posição inicial/final
                elif event.button == 3:
                    if maze.start == (cell_x, cell_y):
                        dragging_start = True
                    elif maze.end == (cell_x, cell_y):
                        dragging_end = True

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 3:
                    dragging_start = False
                    dragging_end = False

            elif event.type == pygame.MOUSEMOTION:
                if dragging_start:
                    mouse_pos = pygame.mouse.get_pos()
                    cell_x = mouse_pos[0] // CELL_SIZE
                    cell_y = mouse_pos[1] // CELL_SIZE
                    maze.set_start(cell_x, cell_y)
                elif dragging_end:
                    mouse_pos = pygame.mouse.get_pos()
                    cell_x = mouse_pos[0] // CELL_SIZE
                    cell_y = mouse_pos[1] // CELL_SIZE
                    maze.set_end(cell_x, cell_y)

            elif event.type == pygame.KEYDOWN:
                executionTime = time.time()
                if event.key == pygame.K_a:
                    maze.set_algorithm(ALGORITHM_ASTAR)
                elif event.key == pygame.K_b:
                    maze.set_algorithm(ALGORITHM_BFS)
                elif event.key == pygame.K_d:
                    maze.set_algorithm(ALGORITHM_DFS)
                elif event.key == pygame.K_SPACE:
                    print("----------------------------------")
                    print("Algoritmo:", maze.algorithm)
                    maze.solve_maze()
                    finalTime = time.time() - executionTime
                    print("Tempo de execução: ", round(finalTime * 1000, 4), "ms")


        maze.draw()

        # Desenha o caminho percorrido pelo personagem
        for x, y in maze.path:
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, BLUE, rect)

        # Desenha a posição inicial e final
        start_rect = pygame.Rect(maze.start[0] * CELL_SIZE, maze.start[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, RED, start_rect)
        end_rect = pygame.Rect(maze.end[0] * CELL_SIZE, maze.end[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, GREEN, end_rect)

        pygame.display.update()
        clock.tick(60)

    pygame.quit()

# Executa o jogo
game_loop()
