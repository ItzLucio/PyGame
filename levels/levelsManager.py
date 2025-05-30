import os
import pygame

from levels.utilities import loadLevelFromPath

tilesData = {
    "G": pygame.transform.scale(pygame.image.load("./assets/Grass.png"), (100, 100)),
    "M": pygame.transform.scale(pygame.image.load("./assets/Ground.png"), (100, 100)),
    "B": pygame.transform.scale(pygame.image.load("./assets/Ground.png"), (100, 100)),
    " ": None
}

class LevelsManager():
    def __init__(self, world, levelsPath: str):
        self.world = world

        self.__levelsList = []
        self.currentLevel = None

        self.perLevelData = {}

        self.currentLevelLayout = []

        self.levelsPath = levelsPath

        self.__loadLevels()
    
    def __loadLevels(self) -> None:
        for fileName in os.listdir(self.levelsPath):
            if not fileName.endswith(".txt"):
                continue

            self.__levelsList.append(loadLevelFromPath(f"{self.levelsPath}/{fileName}"))

    def listLevels(self) -> list:
        return self.__levelsList

    def loadLevel(self, levelId: int):
        chosenLevel = self.__levelsList[levelId]

        self.currentLevel = chosenLevel
        self.currentLevelLayout = self.currentLevel["MAP_LAYOUT"]

        self.__loadCollisionTiles()
    
    def __loadCollisionTiles(self):
        self.collisionTiles = []

        for row_idx, row in enumerate(reversed(self.currentLevelLayout)):
            for col_idx, ch in enumerate(row):
                img = tilesData.get(ch)
                if not img:
                    continue

                x = col_idx * self.world["TILE_SIZE"]
                y = self.world["SCREEN_SIZE"][1] - ((row_idx + 1) * self.world["TILE_SIZE"])  # row_idx=0 -> in alto; cresce verso il basso

                print(x, y)

                collision = pygame.Rect(x, y, self.world["TILE_SIZE"], self.world["TILE_SIZE"])

                self.collisionTiles.append(collision)
    
    def drawLevel(self, screen):
        for row_idx, row in enumerate(reversed(self.currentLevelLayout)):
            for col_idx, ch in enumerate(row):
                img = tilesData.get(ch)
                if not img:
                    continue

                x = col_idx * self.world["TILE_SIZE"]
                y = self.world["SCREEN_SIZE"][1] - ((row_idx + 1) * self.world["TILE_SIZE"])  # row_idx=0 -> in alto; cresce verso il basso

                screen.blit(img, (x, y))
        
        # for rect in self.collisionTiles:
        #     pygame.draw.rect(screen, "red", rect)
