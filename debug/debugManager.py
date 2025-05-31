import wmi
import pygame
import psutil
import os

def getRamUsage():
    process = psutil.Process(os.getpid())
    memBytes = process.memory_info().rss
    memMb = memBytes / 1024 / 1024

    return memMb

def getGPUInfo():
    gpuInfo = wmi.WMI().Win32_VideoController()[0]
    return gpuInfo

class DebugManager():
    def __init__(self, screen, world):
        self.gpuName = getGPUInfo().Name
        self.screen = screen
        self.world = world

        self.debugFont = pygame.font.Font("./assets/fonts/04B_03__.ttf", 20)

    def showDebugInfo(self, fps, deltaTime):
        realFps = round(1/deltaTime)
        memoryUsage = round(getRamUsage())

        metrics = [
            self.debugFont.render(f"Metrics (Pygame {pygame.ver})", True, "white"),
            self.debugFont.render(f"Rendering : {realFps}/{fps} FPS ({self.gpuName})", True, "white"),
            self.debugFont.render(f"Memory Usage (RAM) : {memoryUsage}MB", True, "white")
        ]

        for index, metric in enumerate(reversed(metrics)):
            self.screen.blit(metric, (5, self.world["SCREEN_SIZE"][1] - (metric.get_height() * (index + 1)) - 5))