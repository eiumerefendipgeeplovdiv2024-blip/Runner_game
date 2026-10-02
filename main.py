import asyncio
import pygame
import random
import sys

# Инициализация
pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400
FPS = 60

COLOR_BG = (15, 10, 25)
COLOR_ROOFTOP = (40, 20, 50)
COLOR_NEON_PINK = (255, 20, 147)
COLOR_CYAN = (0, 240, 255)
COLOR_WHITE = (255, 255, 255)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Cyberpunk Ninja Runner")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Consolas", 24, bold=True)

class Ninja(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 50), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.bottom = 320
        self.gravity = 0.8
        self.velocity_y = 0
        self.is_jumping = False
        self.trail_positions = []

    def update(self):
        self.trail_positions.append((self.rect.x, self.rect.y))
        if len(self.trail_positions) > 6:
            self.trail_positions.pop(0)

        self.velocity_y += self.gravity
        self.rect.y += self.velocity_y

        if self.rect.bottom >= 320:
            self.rect.bottom = 320
            self.velocity_y = 0
            self.is_jumping = False

        self.image.fill((0, 0, 0, 0))
        pygame.draw.rect(self.image, COLOR_CYAN, (0, 0, 30, 50), border_radius=5)
        pygame.draw.rect(self.image, COLOR_WHITE, (5, 10, 20, 8))

    def jump(self):
        if not self.is_jumping:
            self.velocity_y = -14
            self.is_jumping = True

    def draw_trail(self, surface):
        for i, pos in enumerate(self.trail_positions):
            alpha = int(255 * ((i + 1) / len(self.trail_positions)) * 0.4)
            trail_surface = pygame.Surface((30, 50), pygame.SRCALPHA)
            trail_surface.fill((*COLOR_CYAN, alpha))
            surface.blit(trail_surface, pos)

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, speed):
        super().__init__()
        width = random.randint(20, 40)
        height = random.randint(30, 60)
        self.image = pygame.Surface((width, height))
        self.image.fill(COLOR_NEON_PINK)
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH + random.randint(0, 100)
        self.rect.bottom = 320
        self.speed = speed

    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.kill()

# Асинхронна основна функция за браузъра
async def main():
    ninja = Ninja()
    ninja_group = pygame.sprite.GroupSingle(ninja)
    obstacles = pygame.sprite.Group()

    game_speed = 7
    score = 0
    spawn_timer = 0
    game_over = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if game_over:
                        await main()
                        return
                    else:
                        ninja.jump()

        if not game_over:
            spawn_timer += 1
            if spawn_timer > random.randint(50, 90):
                obstacles.add(Obstacle(game_speed))
                spawn_timer = 0

            ninja_group.update()
            obstacles.update()

            score += 1
            if score % 500 == 0:
                game_speed += 1

            if pygame.sprite.spritecollide(ninja, obstacles, False):
                game_over = True

        screen.fill(COLOR_BG)
        pygame.draw.rect(screen, (25, 15, 35), (50, 80, 100, 240))
        pygame.draw.rect(screen, (20, 12, 30), (200, 120, 140, 200))
        pygame.draw.rect(screen, (30, 18, 40), (500, 50, 120, 270))

        pygame.draw.rect(screen, COLOR_ROOFTOP, (0, 320, SCREEN_WIDTH, 80))
        pygame.draw.line(screen, COLOR_NEON_PINK, (0, 320), (SCREEN_WIDTH, 320), 4)

        ninja.draw_trail(screen)
        ninja_group.draw(screen)
        obstacles.draw(screen)

        score_text = font.render(f"SCORE: {score}", True, COLOR_CYAN)
        screen.blit(score_text, (SCREEN_WIDTH - 200, 20))

        if game_over:
            over_text = font.render("GAME OVER - Press SPACE", True, COLOR_NEON_PINK)
            rect = over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(over_text, rect)

        pygame.display.flip()
        clock.tick(FPS)
        
        # Задължително за Pygbag / WebAssembly
        await asyncio.sleep(0)

# Стартиране
asyncio.run(main())
