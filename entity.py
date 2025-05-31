import pygame
import os

from character import loadCharacterFrames

class Entity():
    def __init__(self, characterName, speed, world):
        self.characterImages = loadCharacterFrames(characterName)

        self.height = self.characterImages["IDLING"][0].get_size()[1]

        self.positionX = 0
        self.positionY = world["SCREEN_SIZE"][1] - world["GROUND_HEIGHT"] - self.height - 2

        self.speed = speed

        self.velocityX = 0
        self.velocityY = 0

        self.orientation = 1
        
        self.prevX = 0
        self.prevY = 0

        self.onGround = False

        self.world = world

        self.stateName = "IDLING"

        self.currentStateFrames = self.characterImages[self.stateName]
        self.currentFrameIndex = 0
        self.currentFrame = self.currentStateFrames[self.currentFrameIndex]

        self.frameTimer = 0.0
        self.frameDuration = 0.5
    
        self.width = self.currentFrame.get_width()
        self.height = self.currentFrame.get_height()
        self.rect = pygame.Rect(self.positionX,
                                self.positionY,
                                self.width,
                                self.height)
    def __turn(self) -> None:
        base_img = self.currentStateFrames[self.currentFrameIndex]

        if self.orientation >= 0:
            self.currentFrame = base_img
        else:
            self.currentFrame = pygame.transform.flip(base_img, True, False)

    def __updateState(self) -> None:
        if abs(self.velocityX) > 0:
            if self.stateName != "RUNNING":
                self.stateName = "RUNNING"
        else:
            if self.stateName != "IDLING":
                self.stateName = "IDLING"
        
        self.currentStateFrames = self.characterImages[self.stateName]
    
    def __updateAnimation(self, deltaTime: float) -> None:
        if len(self.currentStateFrames) > 1:
            self.frameTimer += deltaTime

            if self.frameTimer >= self.frameDuration:
                self.frameTimer = 0.0
                self.currentFrameIndex = (self.currentFrameIndex + 1) % len(self.currentStateFrames)
        else:
            self.currentFrameIndex = 0

        if self.currentFrameIndex >= len(self.currentStateFrames):
            self.currentFrameIndex = 0

        self.currentFrame = self.currentStateFrames[self.currentFrameIndex]

    def setPosition(self, x: int, y: int) -> None:
        self.positionX = x
        self.positionY = y
    
    def setVelocityX(self, velocityX: int):
        self.velocityX = velocityX

        if self.velocityX >= 0:
            self.orientation = 1
        else:
            self.orientation = -1
    
    def jump(self) -> None:
        if self.onGround:
            self.velocityY = -400
            self.onGround = False

    def update(self, deltaTime: float, collisionTiles: list) -> None:
        # stato, animazione e flip
        self.__updateState()
        self.__updateAnimation(deltaTime)
        self.__turn()

        # salva vecchie posizioni
        self.prevX = self.positionX
        self.prevY = self.positionY

        # VERTICALE: applica gravità e movimento Y
        if not self.onGround:
            # accelera verso il basso
            self.velocityY += self.world["GRAVITY"] * deltaTime
        # distanza da muovere in Y
        dy = self.velocityY * deltaTime * self.world["VELOCITY_MULTIPLIER"]

        # aggiorna rect e posizioneY temporanee
        self.rect.y += dy
        self.onGround = False
        for tile in collisionTiles:
            if self.rect.colliderect(tile):
                if self.velocityY > 0:
                    # cadendo: blocca sopra il tile
                    self.rect.bottom = tile.top
                    self.onGround = True
                elif self.velocityY < 0:
                    # salendo: blocca sotto il tile
                    self.rect.top = tile.bottom
                self.velocityY = 0
        # sincronizza positionY col rect
        self.positionY = self.rect.y

        # ORIZZONTALE: movimento X (speed → impulso one–shot)
        dx = self.velocityX * deltaTime * self.speed * self.world["VELOCITY_MULTIPLIER"]
        self.velocityX = 0
        self.rect.x += dx
        for tile in collisionTiles:
            if self.rect.colliderect(tile):
                if dx > 0:
                    # muovendosi a destra: blocca a sinistra del tile
                    self.rect.right = tile.left
                elif dx < 0:
                    # muovendosi a sinistra: blocca a destra del tile
                    self.rect.left = tile.right
        # sincronizza positionX col rect
        self.positionX = self.rect.x

        # (opzionale) se vuoi dimezzare lo spostamento orizzontale quando in aria:
        if not self.onGround:
            self.positionX = self.prevX + (self.positionX - self.prevX) * 0.5
            self.rect.x = self.positionX

    
    def draw(self, screen) -> None:
        screen.blit(self.currentFrame, (self.positionX, self.positionY))
