import pygame
import sys
import random

pygame.init()

WIDTH, HEIGHT = 800, 600
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 50, 70
ASTEROID_SIZE = 40
SPACESHIP_SPEED = 7
ASTEROID_SPEED_MIN = 3
ASTEROID_SPEED_MAX = 7
BACKGROUND_COLOR = (0, 0, 30)
SCORE_COLOR = (255, 255, 255)
TITLE_COLOR = (0, 255, 255)
INSTRUCTION_COLOR = (200, 200, 200)
BUTTON_COLOR = (50, 150, 50)
BUTTON_HOVER_COLOR = (70, 200, 70)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rocket Escape")
clock = pygame.time.Clock()

def load_image(name, size):
    image = pygame.Surface(size)
    if name == "spaceship":
        pygame.draw.polygon(image, (0, 255, 255), [(size[0]//2, 0), (0, size[1]), (size[0], size[1])])
    else:
        pygame.draw.circle(image, (150, 75, 0), (size[0]//2, size[1]//2), size[0]//2)
    image.set_colorkey((0, 0, 0))
    return image

spaceship_img = load_image("spaceship", (SPACESHIP_WIDTH, SPACESHIP_HEIGHT))
asteroid_img = load_image("asteroid", (ASTEROID_SIZE, ASTEROID_SIZE))

class Spaceship:
    def __init__(self):
        self.x = WIDTH // 2 - SPACESHIP_WIDTH // 2
        self.y = HEIGHT - SPACESHIP_HEIGHT - 20
        self.rect = pygame.Rect(self.x, self.y, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    def move(self, direction):
        if direction == "left" and self.x > 0:
            self.x -= SPACESHIP_SPEED
        if direction == "right" and self.x < WIDTH - SPACESHIP_WIDTH:
            self.x += SPACESHIP_SPEED
        self.rect.x = self.x
    def draw(self):
        screen.blit(spaceship_img, (self.x, self.y))

class Asteroid:
    def __init__(self):
        self.size = ASTEROID_SIZE
        self.x = random.randint(0, WIDTH - self.size)
        self.y = -self.size
        self.speed = random.uniform(ASTEROID_SPEED_MIN, ASTEROID_SPEED_MAX)
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)
    def update(self):
        self.y += self.speed
        self.rect.y = self.y
        return self.y > HEIGHT
    def draw(self):
        screen.blit(asteroid_img, (self.x, self.y))

def show_score(score):
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score:.1f}", True, SCORE_COLOR)
    screen.blit(score_text, (10, 10))

def show_game_over(score):
    font = pygame.font.Font(None, 72)
    game_over_text = font.render("GAME OVER", True, (255, 0, 0))
    screen.blit(game_over_text, (WIDTH//2 - game_over_text.get_width()//2, HEIGHT//2 - 50))
    score_font = pygame.font.Font(None, 48)
    final_score_text = score_font.render(f"Final Score: {score:.1f}", True, SCORE_COLOR)
    screen.blit(final_score_text, (WIDTH//2 - final_score_text.get_width()//2, HEIGHT//2 + 20))
    restart_font = pygame.font.Font(None, 36)
    restart_text = restart_font.render("Press R to restart or Q to quit", True, SCORE_COLOR)
    screen.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, HEIGHT//2 + 80))

def show_start_screen():
    title_font = pygame.font.Font(None, 72)
    instruction_font = pygame.font.Font(None, 28)
    start = False
    while not start:
        screen.fill(BACKGROUND_COLOR)
        title_text = title_font.render("ROCKET ESCAPE", True, TITLE_COLOR)
        screen.blit(title_text, (WIDTH//2 - title_text.get_width()//2, 80))
        instructions = [
            "Press SPACE to start the game",
            "Use LEFT and RIGHT arrows to move",
            "Avoid falling asteroids!"
        ]
        for i, line in enumerate(instructions):
            instruction_text = instruction_font.render(line, True, INSTRUCTION_COLOR)
            screen.blit(instruction_text, (WIDTH//2 - instruction_text.get_width()//2, 200 + i * 40))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    start = True
        clock.tick(60)

def main():
    show_start_screen()
    spaceship = Spaceship()
    asteroids = []
    score = 0
    frame_count = 0
    running = True
    while running:
        screen.fill(BACKGROUND_COLOR)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            spaceship.move("left")
        if keys[pygame.K_RIGHT]:
            spaceship.move("right")

        # Spawn asteroids
        if frame_count % 30 == 0:
            asteroids.append(Asteroid())

        # Update asteroids
        for asteroid in asteroids[:]:
            if asteroid.update():
                asteroids.remove(asteroid)
                score += 1

        # Check collisions
        for asteroid in asteroids:
            if spaceship.rect.colliderect(asteroid.rect):
                running = False

        spaceship.draw()
        for asteroid in asteroids:
            asteroid.draw()

        show_score(score)

        pygame.display.flip()
        clock.tick(60)
        frame_count += 1

    # Game over screen
    game_over = True
    while game_over:
        screen.fill(BACKGROUND_COLOR)
        show_game_over(score)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    main()  # Restart game
                    return
                if event.key == pygame.K_q:
                    game_over = False
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
