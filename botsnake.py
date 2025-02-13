import pygame
import random
import traceback
import heapq

# Initialisation de Pygame
pygame.init()

# Définition des couleurs
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GRAY = (192, 192, 192)

# Taille de la fenêtre de jeu
WIDTH, HEIGHT = 600, 400

# Taille d'une cellule
CELL_SIZE = 20

# Définition des directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
DIRECTIONS = [UP, DOWN, LEFT, RIGHT]

# Classe du serpent
class Snake:
    def __init__(self):
        self.length = 1
        self.positions = [(WIDTH // 2, HEIGHT // 2)]
        self.direction = random.choice(DIRECTIONS)
        self.color = GREEN

    def get_head_position(self):
        return self.positions[0]

    def turn(self, direction):
        if self.length > 1 and (direction[0] * -1, direction[1] * -1) == self.direction:
            return
        self.direction = direction

    def move(self):
        cur = self.get_head_position()
        x, y = self.direction
        new = (((cur[0] + (x * CELL_SIZE)) % WIDTH), (cur[1] + (y * CELL_SIZE)) % HEIGHT)
        if len(self.positions) > 2 and new in self.positions[2:]:
            return True  # Indique que le serpent est mort
        else:
            self.positions.insert(0, new)
            if len(self.positions) > self.length:
                self.positions.pop()
            return False  # Indique que le serpent n'est pas mort

    def reset(self):
        self.length = 1
        self.positions = [(WIDTH // 2, HEIGHT // 2)]
        self.direction = random.choice(DIRECTIONS)

    def draw(self, screen):
        for pos in self.positions:
            pygame.draw.rect(screen, self.color, (pos[0], pos[1], CELL_SIZE, CELL_SIZE))

# Classe de la pomme
class Apple:
    def __init__(self):
        self.position = (0, 0)
        self.color = RED
        self.randomize_position()

    def randomize_position(self):
        self.position = (random.randint(0, (WIDTH - CELL_SIZE) // CELL_SIZE) * CELL_SIZE,
                         random.randint(0, (HEIGHT - CELL_SIZE) // CELL_SIZE) * CELL_SIZE)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (*self.position, CELL_SIZE, CELL_SIZE))

def avoid_collision(snake, direction):
    next_pos = ((snake.get_head_position()[0] + direction[0] * CELL_SIZE) % WIDTH,
                (snake.get_head_position()[1] + direction[1] * CELL_SIZE) % HEIGHT)
    if next_pos in snake.positions[1:]:
        return False
    return True

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def a_star_search(start, goal, snake):
    frontier = []
    heapq.heappush(frontier, (0, start))
    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0

    while frontier:
        current = heapq.heappop(frontier)[1]

        if current == goal:
            break

        for direction in DIRECTIONS:
            next_pos = ((current[0] + direction[0] * CELL_SIZE) % WIDTH,
                        (current[1] + direction[1] * CELL_SIZE) % HEIGHT)
            new_cost = cost_so_far[current] + 1
            if next_pos not in cost_so_far and next_pos not in snake.positions[1:]:
                cost_so_far[next_pos] = new_cost
                priority = new_cost + heuristic(goal, next_pos)
                heapq.heappush(frontier, (priority, next_pos))
                came_from[next_pos] = current

    path = []
    current = goal
    while current != start:
        path.append(current)
        current = came_from.get(current, start)
    path.reverse()
    return path

def check_safety(snake, direction):
    temp_snake = Snake()
    temp_snake.positions = snake.positions[:]
    temp_snake.length = snake.length
    temp_snake.direction = direction
    is_dead = temp_snake.move()
    if is_dead:
        return False

    return True

# Fonction principale du jeu
def main():
    try:
        # Création de la fenêtre
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Snake Game')

        # Initialisation du jeu
        snake = Snake()
        apple = Apple()
        score = 0
        clock = pygame.time.Clock()

        # Boucle principale du jeu
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            if apple.position in snake.positions:
                apple.randomize_position()

            path_to_apple = a_star_search(snake.get_head_position(), apple.position, snake)
            if path_to_apple and path_to_apple[0] != snake.positions[-1]:
                next_pos = path_to_apple[0]
                next_direction = (next_pos[0] - snake.get_head_position()[0],
                                  next_pos[1] - snake.get_head_position()[1])
                if next_direction == (CELL_SIZE, 0):
                    direction = RIGHT
                elif next_direction == (-CELL_SIZE, 0):
                    direction = LEFT
                elif next_direction == (0, CELL_SIZE):
                    direction = DOWN
                elif next_direction == (0, -CELL_SIZE):
                    direction = UP

                if check_safety(snake, direction):
                    snake.turn(direction)
                else:
                    # Si la direction trouvée n'est pas sûre, choisir une direction sûre
                    possible_directions = [UP, DOWN, LEFT, RIGHT]
                    random.shuffle(possible_directions)
                    for direction in possible_directions:
                        if avoid_collision(snake, direction):
                            snake.turn(direction)
                            break
            else:
                # Si aucun chemin n'est trouvé ou si la pomme est sur la queue, faire un mouvement aléatoire sûr
                possible_directions = [UP, DOWN, LEFT, RIGHT]
                random.shuffle(possible_directions)
                for direction in possible_directions:
                    if avoid_collision(snake, direction):
                        snake.turn(direction)
                        break

            is_dead = snake.move()
            if is_dead:
                snake.reset()  # Réinitialiser le serpent
                apple.randomize_position()
                score = 0  # Réinitialiser le score

            if snake.get_head_position() == apple.position:
                snake.length += 1  # Augmenter la longueur du serpent
                apple.randomize_position()
                score += 1

            screen.fill(BLACK)  # Mettre le fond en noir
            snake.draw(screen)
            apple.draw(screen)
            pygame.display.flip()
            clock.tick(10)

        pygame.quit()
    except Exception as e:
        traceback.print_exc()

# Démarrage du jeu
if __name__ == '__main__':
    main()
