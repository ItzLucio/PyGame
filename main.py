import pygame

from player import Player
from debug.debugManager import DebugManager
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
canPlay = True
paused = False
showDebugInfo = False

pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE, pygame.FULLSCREEN)
pygame.display.set_caption("Super PyRion")

clock = pygame.time.Clock()

bodyFont = pygame.font.Font("./assets/fonts/04B_03__.ttf", 55)

backgroundImage = pygame.image.load("./assets/Background.png")
backgroundImage = pygame.transform.scale(backgroundImage, SCREEN_SIZE)

vignetteImage = pygame.image.load("./assets/Vignette.png")
vignetteImage = pygame.transform.scale(vignetteImage, SCREEN_SIZE)

player = Player("Lucio", "player", 200, WORLD)
levelsManager = LevelsManager(WORLD, "./levels/data")
debugManager = DebugManager(screen, WORLD)

levelsManager.loadLevel(0)

FPS = 24

while running:
    deltaTime = clock.tick(FPS) / 1000.0

    if not canPlay or paused:
        continue

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_F3:
                showDebugInfo = not showDebugInfo
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_d]:
        player.setVelocityX(1)
    if keys[pygame.K_a]:
        player.setVelocityX(-1)
    if keys[pygame.K_SPACE]:
        player.jump()
    
    player.update(deltaTime, levelsManager.collisionTiles)
    
    pointsText = bodyFont.render(f"Score: {player.score}", True, "white")
    
    screen.blit(backgroundImage, (0, 0))

    levelsManager.drawLevel(screen)

    player.draw(screen)

    screen.blit(vignetteImage, (0, 0))

    screen.blit(pointsText, (50, 50))

    if showDebugInfo:
        debugManager.showDebugInfo(FPS, deltaTime)

    pygame.display.flip()