import os
import pygame

def __loadImagesFromDir(folderPath) -> list:
    frames = []

    for fileName in sorted(os.listdir(folderPath)):
        if fileName.endswith(".png") or fileName.endswith(".jpg"):
            frame = pygame.image.load(os.path.join(folderPath, fileName)).convert_alpha()
            frames.append(pygame.transform.scale(frame, (100, 180)))
    
    return frames

def loadCharacterFrames(characterName) -> dict:
    folderPath = f"./assets/characters/{characterName}"

    data = {
        "IDLING": __loadImagesFromDir(f"{folderPath}/IDLING"),
        "RUNNING": __loadImagesFromDir(f"{folderPath}/RUNNING")
    }

    return data