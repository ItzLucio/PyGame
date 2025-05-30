import pygame

from player import Player
from levels.levelsManager import LevelsManager

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
GROUND_HEIGHT = 220
GROUND_SIZE = (SCREEN_WIDTH, GROUND_HEIGHT)

WORLD = {
    "GROUND_HEIGHT": GROUND_HEIGHT,
    "GRAVITY": 800,
    "SCREEN_SIZE": SCREEN_SIZE,
    "VELOCITY_MULTIPLIER": 1.2,
    "TILE_SIZE": 100
}

running = True
points = 0

pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE, pygame.FULLSCREEN)
pygame.display.set_caption("Super PyRion")

clock = pygame.time.Clock()

bodyFont = pygame.font.Font("./assets/fonts/Jersey10-Regular.ttf", 55)
# bodyFont = pygame.font.SysFont("VGASYS", 50)

backgroundImage = pygame.image.load("./assets/Background.png")
backgroundImage = pygame.transform.scale(backgroundImage, SCREEN_SIZE)

groundImage = pygame.image.load("./assets/Ground.png")
groundImage = pygame.transform.scale(groundImage, GROUND_SIZE)

vignetteImage = pygame.image.load("./assets/Vignette.png")
vignetteImage = pygame.transform.scale(vignetteImage, SCREEN_SIZE)

player = Player("Lucio", "player", 200, WORLD)
levelsManager = LevelsManager(WORLD, "./levels/data")

levelsManager.loadLevel(0)

FPS = 60

while running:
    deltaTime = clock.tick(FPS) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]:
        player.setVelocityX(1)
    if keys[pygame.K_LEFT]:
        player.setVelocityX(-1)
    if keys[pygame.K_UP]:
        player.jump()
    
    player.update(deltaTime, levelsManager.collisionTiles)
    
    pointsText = bodyFont.render(f"Score: {points}", True, "white")
    
    screen.blit(backgroundImage, (0, 0))
    # screen.blit(groundImage, (0, SCREEN_HEIGHT-GROUND_HEIGHT))

    levelsManager.drawLevel(screen)

    player.draw(screen)

    screen.blit(vignetteImage, (0, 0))

    screen.blit(pointsText, (50, 50))

    pygame.display.flip()