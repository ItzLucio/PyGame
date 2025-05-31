from entity import Entity

class Player(Entity):
    def __init__(self, nome, characterName, speed, world):
        super().__init__(characterName, speed, world)

        self.nome = nome
        self.score = 0
    
    def setScore(self, score: int) -> None:
        self.score = score