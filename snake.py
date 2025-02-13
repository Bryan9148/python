import pygame
import random
import traceback

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

# Classe du serpent
class Snake:
    def __init__(self):
        self.length = 1
        self.positions = [(WIDTH / 2, HEIGHT / 2)]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
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
        self.positions = [(WIDTH / 2, HEIGHT / 2)]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])

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
        print("Randomizing apple position...")  # Ajout du print statement
        self.position = (random.randint(0, (WIDTH - CELL_SIZE) // CELL_SIZE) * CELL_SIZE,
                         random.randint(0, (HEIGHT - CELL_SIZE) // CELL_SIZE) * CELL_SIZE)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (*self.position, CELL_SIZE, CELL_SIZE))


# Fonction pour afficher l'écran de démarrage
def show_start_screen(screen):
    font_title = pygame.font.Font("freesansbold.ttf", 64)
    font_button = pygame.font.Font("freesansbold.ttf", 32)
    title_text = font_title.render("Snake", True, WHITE)
    start_text = font_button.render("Start", True, WHITE)

    screen.fill(BLACK)
    screen.blit(title_text, ((WIDTH - title_text.get_width()) // 2, 50))
    button_rect = pygame.Rect((WIDTH - start_text.get_width()) // 2, (HEIGHT - start_text.get_height()) // 2,
                              start_text.get_width(), start_text.get_height())
    pygame.draw.rect(screen, BLACK, button_rect)
    screen.blit(start_text, button_rect.topleft)
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                waiting = False

# Fonction pour afficher le score, le compteur de morts et le meilleur score
def show_scores(screen, score, deaths, best_score):
    font = pygame.font.Font("freesansbold.ttf", 24)
    score_text = font.render("Score: " + str(score), True, WHITE)
    deaths_text = font.render("Deaths: " + str(deaths), True, WHITE)
    best_score_text = font.render("Best Score: " + str(best_score), True, WHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(deaths_text, (10, 40))
    screen.blit(best_score_text, (10, 70))

# Fonction pour afficher l'écran de fin de jeu
def show_game_over_screen(screen):
    font_title = pygame.font.Font("freesansbold.ttf", 64)
    font_button = pygame.font.Font("freesansbold.ttf", 32)
    game_over_text = font_title.render("Game Over", True, WHITE)
    restart_text = font_button.render("Restart", True, BLACK)
    exit_text = font_button.render("Exit", True, BLACK)

    # Filtre rouge
    red_filter = pygame.Surface((WIDTH, HEIGHT))
    red_filter.set_alpha(128)  # Transparence
    red_filter.fill(RED)
    screen.blit(red_filter, (0, 0))

    # Texte de game over
    screen.blit(game_over_text, ((WIDTH - game_over_text.get_width()) // 2, 50))

    # Bouton Restart
    restart_rect = pygame.Rect((WIDTH - restart_text.get_width()) // 2, (HEIGHT - restart_text.get_height()) // 2,
                               restart_text.get_width(), restart_text.get_height())
    screen.blit(restart_text, restart_rect.topleft)

    # Bouton Exit
    exit_rect = pygame.Rect((WIDTH - exit_text.get_width()) // 2, (HEIGHT - exit_text.get_height()) // 2 + 50,
                            exit_text.get_width(), exit_text.get_height())
    screen.blit(exit_text, exit_rect.topleft)

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return True  # Restart
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if restart_rect.collidepoint(x, y):
                    return True  # Restart
                elif exit_rect.collidepoint(x, y):
                    pygame.quit()
                    quit()
    return False

# Fonction pour afficher l'écran de pause
def show_pause_screen(screen):
    font_button = pygame.font.Font("freesansbold.ttf", 32)
    resume_text = font_button.render("Resume", True, BLACK)

    # Filtre gris
    gray_filter = pygame.Surface((WIDTH, HEIGHT))
    gray_filter.set_alpha(128)  # Transparence
    gray_filter.fill(GRAY)
    screen.blit(gray_filter, (0, 0))

    # Bouton Resume
    resume_rect = pygame.Rect((WIDTH - resume_text.get_width()) // 2, (HEIGHT - resume_text.get_height()) // 2,
                              resume_text.get_width(), resume_text.get_height())
    screen.blit(resume_text, resume_rect.topleft)

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if resume_rect.collidepoint(x, y):
                    return

# Fonction principale du jeu
def main():
    try:
        # Création de la fenêtre
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Snake Game')

        show_start_screen(screen)

        # Initialisation du jeu
        snake = Snake()
        apple = Apple()
        # score, deaths et best_score initialisés ici
        global score, deaths, best_score
        score = 0
        deaths = 0
        best_score = 0
        clock = pygame.time.Clock()

        # Variables pour la pause du jeu
        paused = False

        # Boucle principale du jeu
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        snake.turn(UP)
                    elif event.key == pygame.K_DOWN:
                        snake.turn(DOWN)
                    elif event.key == pygame.K_LEFT:
                        snake.turn(LEFT)
                    elif event.key == pygame.K_RIGHT:
                        snake.turn(RIGHT)
                    if event.key == pygame.K_z:
                        snake.turn(UP)
                    elif event.key == pygame.K_s:
                        snake.turn(DOWN)
                    elif event.key == pygame.K_q:
                        snake.turn(LEFT)
                    elif event.key == pygame.K_d:
                        snake.turn(RIGHT)
                    elif event.key == pygame.K_p:  # Pause avec la touche P
                        paused = not paused
                        if paused:
                            show_pause_screen(screen)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    pause_button_rect = pygame.Rect(WIDTH - 100, 10, 90, 30)
                    if pause_button_rect.collidepoint(x, y):
                        paused = True
                        show_pause_screen(screen)
                        paused = False

            if not paused:
                is_dead = snake.move()
                if is_dead:
                    if score > best_score:
                        best_score = score
                    if not show_game_over_screen(screen):
                        running = False
                        break
                    snake.reset()  # Redémarrer le serpent
                    apple = Apple()
                    score = 0  # Réinitialiser le score

                if snake.get_head_position() == apple.position:
                    snake.length += 1
                    score += 1
                    apple.randomize_position()

            screen.fill(BLACK)  # Mettre le fond en noir
            snake.draw(screen)
            apple.draw(screen)

            # Afficher le score, le compteur de morts et le meilleur score
            show_scores(screen, score, deaths, best_score)

            # Bouton de pause
            pause_button_rect = pygame.Rect(WIDTH - 100, 10, 90, 30)
            pygame.draw.rect(screen, WHITE, pause_button_rect)
            pause_text = pygame.font.Font("freesansbold.ttf", 24).render("Pause", True, BLACK)
            screen.blit(pause_text, (WIDTH - 95, 15))

            pygame.display.flip()
            # Déplacer le serpent moins fréquemment pour réduire la vitesse
            clock.tick(7)

        pygame.quit()
    except Exception as e:
        traceback.print_exc()

# Démarrage du jeu
if __name__ == '__main__':
    main()

