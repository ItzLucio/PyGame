import os
import pygame
import random

from levels.utilities import loadLevelFromPath

# Definisci il dizionario dei tiles
tilesData = {
    "G0": pygame.transform.scale(pygame.image.load("./assets/grass/Grass0.png"), (100, 100)),
    "G1": pygame.transform.scale(pygame.image.load("./assets/grass/Grass1.png"), (100, 100)),
    "G2": pygame.transform.scale(pygame.image.load("./assets/grass/Grass2.png"), (100, 100)),
    "M0": pygame.transform.scale(pygame.image.load("./assets/mud/Mud0.png"), (100, 100)),
    "M1": pygame.transform.scale(pygame.image.load("./assets/mud/Mud1.png"), (100, 100)),
    "M2": pygame.transform.scale(pygame.image.load("./assets/mud/Mud2.png"), (100, 100)),
    "M3": pygame.transform.scale(pygame.image.load("./assets/mud/Mud3.png"), (100, 100)),
    "B": pygame.transform.scale(pygame.image.load("./assets/mud/Mud0.png"), (100, 100)),
    " ": None
}

class LevelsManager:
    def __init__(self, world, levelsPath: str):
        self.world = world
        self.__levelsList = []
        self.currentLevel = None
        self.perLevelData = {}
        self.currentLevelLayout = []
        self.levelsPath = levelsPath
        self.collisionTiles = []
        self.__loadLevels()

    def __loadLevels(self) -> None:
        # Carica tutti i livelli dalla cartella specificata
        for fileName in os.listdir(self.levelsPath):
            if not fileName.endswith(".txt"):
                continue
            self.__levelsList.append(loadLevelFromPath(f"{self.levelsPath}/{fileName}"))

    def listLevels(self) -> list:
        return self.__levelsList

    def loadLevel(self, levelId: int):
        # Resetta la mappa del livello precedente prima di caricare un nuovo livello
        self.currentLevelLayout = []
        chosenLevel = self.__levelsList[levelId]
        self.currentLevel = chosenLevel

        # Carica il layout del livello
        for row in chosenLevel["MAP_LAYOUT"]:
            currentRow = []
            for ch in row:
                if ch == "G":
                    currentRow.append(ch+str(random.randint(0, 1)))
                elif ch == "M":
                    currentRow.append(ch+str(random.randint(0, 3)))
                else:
                    currentRow.append(ch)
            self.currentLevelLayout.append(currentRow)

        # Carica i tiles di collisione
        self.__loadCollisionTiles()

    def __loadCollisionTiles(self) -> None:
        # Resetta la lista delle collisioni
        self.collisionTiles = []

        for row_idx, row in enumerate(reversed(self.currentLevelLayout)):
            for col_idx, ch in enumerate(row):
                img = tilesData.get(ch)
                if not img:
                    continue

                # Calcola le coordinate della tile
                x = col_idx * self.world["TILE_SIZE"]
                y = self.world["SCREEN_SIZE"][1] - ((row_idx + 1) * self.world["TILE_SIZE"])

                # Aggiungi il rettangolo di collisione
                collision = pygame.Rect(x, y, self.world["TILE_SIZE"], self.world["TILE_SIZE"])
                self.collisionTiles.append(collision)

    def drawLevel(self, screen) -> None:
        # Disegna la mappa del livello
        for row_idx, row in enumerate(reversed(self.currentLevelLayout)):
            for col_idx, ch in enumerate(row):
                img = tilesData.get(ch)
                if not img:
                    continue

                # Calcola le coordinate per il disegno
                x = col_idx * self.world["TILE_SIZE"]
                y = self.world["SCREEN_SIZE"][1] - ((row_idx + 1) * self.world["TILE_SIZE"])

                screen.blit(img, (x, y))

        # Disegna le collisioni (per debugging)
        # for rect in self.collisionTiles:
        #     pygame.draw.rect(screen, "red", rect, 1)  # Mostra i rettangoli di collisione in rosso

