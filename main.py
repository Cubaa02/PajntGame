import pygame
import random

# Inicializace Pygame
pygame.init()

# Nastavení obrazovky
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fruit Ninja - Základní verze")

# Barvy
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BROWN_BACKGROUND = (120, 85, 55)

# Načtení obrázků
fruit_images = [
    pygame.transform.scale(pygame.image.load("img/apple.png"), (50, 50)),
    pygame.transform.scale(pygame.image.load("img/banana.png"), (50, 50)),
    pygame.transform.scale(pygame.image.load("img/watermelon.png"), (50, 50))
]

slash_effect = pygame.image.load("img/slash.png")
slash_effect = pygame.transform.scale(slash_effect, (60, 60))

sliced_fruit_images = [
    (pygame.transform.scale(pygame.image.load("img/apple_left.png"), (50, 50)),
     pygame.transform.scale(pygame.image.load("img/apple_right.png"), (50, 50))),
    (pygame.transform.scale(pygame.image.load("img/banana_left.png"), (50, 50)),
     pygame.transform.scale(pygame.image.load("img/banana_right.png"), (50, 50))),
    (pygame.transform.scale(pygame.image.load("img/watermelon_left.png"), (50, 50)),
     pygame.transform.scale(pygame.image.load("img/watermelon_right.png"), (50, 50)))
]

bomb_image = pygame.transform.scale(pygame.image.load("img/bomb.png"), (50, 50))
explosion_image = pygame.transform.scale(pygame.image.load("img/explosion.png"), (60, 60))

class Fruit:
    def __init__(self, is_bomb=False):
        self.x = random.randint(100, WIDTH - 100)
        self.y = HEIGHT
        self.speed = random.uniform(5, 8)  # Zvýšení rychlosti ovoce
        self.caught = False
        self.is_bomb = is_bomb
        if self.is_bomb:
            self.image = bomb_image
            self.explosion_timer = 0
        else:
            self.image_index = random.randint(0, len(fruit_images) - 1)
            self.image = fruit_images[self.image_index]
            self.sliced_images = sliced_fruit_images[self.image_index]
        self.sliced = False
        self.slice_timer = 0
        self.slice_speed_left = [random.uniform(-3, -1), random.uniform(1, 3)]
        self.slice_speed_right = [random.uniform(1, 3), random.uniform(1, 3)]
        self.alpha = 255

    def update(self):
        if not self.caught:
            self.y -= self.speed
            self.speed -= 0.05  # Mírné zpomalení pro větší hratelnost
            if self.y < -50:
                self.caught = True
                if not self.is_bomb:
                    global lives
                    lives -= 1
        elif self.sliced and not self.is_bomb:
            self.slice_timer += 1
            self.x += self.slice_speed_left[0]
            self.y += self.slice_speed_left[1]
            self.alpha = max(0, self.alpha - 5)
        elif self.is_bomb and self.sliced:
            self.explosion_timer += 1
            self.alpha = max(0, self.alpha - 5)
            if self.explosion_timer > 30:
                self.caught = True

    def draw(self):
        if not self.caught:
            screen.blit(self.image, (self.x, self.y))
        elif self.sliced and not self.is_bomb:
            sliced_left = self.sliced_images[0].copy()
            sliced_right = self.sliced_images[1].copy()
            sliced_left.set_alpha(self.alpha)
            sliced_right.set_alpha(self.alpha)
            screen.blit(sliced_left, (self.x, self.y))
            screen.blit(sliced_right, (self.x + 25, self.y))
            if self.slice_timer < 10:
                screen.blit(slash_effect, (self.x, self.y))
        elif self.is_bomb and self.sliced:
            explosion = explosion_image.copy()
            explosion.set_alpha(self.alpha)
            screen.blit(explosion, (self.x, self.y))

    def check_collision(self, pos):
        if self.x < pos[0] < self.x + 50 and self.y < pos[1] < self.y + 50:
            self.caught = True
            self.sliced = True
            return True
        return False

def main():
    global lives
    clock = pygame.time.Clock()
    fruits = [Fruit()]
    score = 0
    lives = 3  # Počet životů
    fruit_spawn_timer = 0  # Časovač pro generování nového ovoce
    base_spawn_interval = 55  # Počáteční interval pro generování ovoce (100 snímků)
    min_spawn_interval = 25  # Minimální interval pro generování ovoce
    
    font = pygame.font.Font(None, 36)
    running = True
    while running:
        screen.fill(BROWN_BACKGROUND)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for fruit in fruits:
                    if fruit.check_collision(pos):
                        if fruit.is_bomb:
                            lives -= 1
                            score -= 5
                        else:
                            score += 1
        
        # Dynamické zkracování intervalu podle skóre (každých 5 bodů snížit o 5)
        spawn_interval = max(min_spawn_interval, base_spawn_interval - (score // 5) * 5)
        
        # Generování ovoce a bomb
        fruit_spawn_timer += 1
        if fruit_spawn_timer > spawn_interval:  # Nové ovoce podle intervalu
            fruits.append(Fruit(is_bomb=random.random() < 0.3))  # 30% šance na bombu
            fruit_spawn_timer = 0
        
        # Progresivní zkracování intervalu pro generování ovoce
        for fruit in fruits:
            fruit.update()
            fruit.draw()

        score_text = font.render(f"Score: {score}", True, WHITE)
        lives_text = font.render(f"Lives: {lives}", True, RED)
        screen.blit(score_text, (10, 10))
        screen.blit(lives_text, (10, 50))
        
        pygame.display.flip()
        clock.tick(60)
        
        if lives <= 0:
            running = False
    
    pygame.quit()

if __name__ == "__main__":
    main()
