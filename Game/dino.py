import pygame
import numpy as np
pygame.init()

WIDTH = 500
HEIGHT = 500

class Window:
    def __init__(self, width, height, character):
        self.win = pygame.display.set_mode((width, height))
        pygame.display.set_caption('Dino Game')
        self.jumpSound = pygame.mixer.Sound('Game/Sounds/jump.wav')
        self.level = pygame.mixer.Sound('Game/Sounds/level.wav')
        self.character = character
        self.run = True
        self.score = 0
        self.font = pygame.font.SysFont('freesansbold', 30)
        self.leveler = [100, 200, 500, 1000]
        self.timeCounter = 0
        self.obsTracker = []
    
    def update(self):
        self.timeCounter += 1
        self.score +=1
        self.win.fill((255, 255, 255))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False

        if len(self.obsTracker) > 0:
            for i, obs in enumerate(self.obsTracker):
                obs.x -= obs.velocity

        if self.timeCounter % 50 == 0 and self.timeCounter > 0:
            if np.random.randint(0,2) == 0:
                self.obsTracker.append(Obstical())
            else:
                self.obsTracker.append(Bird())

        keys = pygame.key.get_pressed()
        if not self.character.jump:
            if keys[pygame.K_SPACE] and not self.character.duck:
                self.character.jump = True
                self.jumpSound.play()
            elif keys[pygame.K_DOWN]:
                self.character.duck = True
                self.character.y = 380
            else:
                self.character.duck = False
                self.character.y = 355
        else:
            if self.character.jumpStage >= -10:
                x = 1
                if self.character.jumpStage < 0:
                    x = -1
                self.character.y -= x*((self.character.jumpStage**2)*0.18)
                self.character.jumpStage -= 1
            else:
                self.character.jump = False
                self.character.jumpStage = 10
        self.redraw()
    
    def redraw(self):
        self.character.update()
        level = self.leveler[0]
        if self.score == level:
            self.level.play()
            if not self.leveler[0] >= 1000:
                self.leveler.pop(0)
            else:
                self.leveler[0]+= 500

        text = self.font.render(f'Score: {self.score}', 1, self.character.colour)
        self.win.blit(text, (350, 10))
        
        pygame.draw.rect(self.win, self.character.colour,
        (self.character.x, self.character.y,
        self.character.width, self.character.height))

        for i, obs in enumerate(self.obsTracker):
            pygame.draw.rect(self.win, self.character.colour,
            (obs.x, obs.y,
            obs.width, obs.height))
            if obs.x <= 0:
                    self.obsTracker.pop(i)
                    if self.score + 50 >= self.leveler[0]:
                        self.leveler[0] += 500
                        self.level.play()
                    self.score += 50
        pygame.display.update()

class Character:
    def __init__(self):
        self.x = 60
        self.y = 355
        self.width = 25
        self.height = 50
        self.velocity = 2
        self.jump = False
        self.jumpStage = 10
        self.dead = False
        self.colour = (90, 90, 90)
        self.duck = False
    
    def update(self):
        if self.duck:
            self.height = 25
        else:
            self.height = 50

class Obstical:
    def __init__(self):
        self.x = 500
        self.y = 373
        self.width = 25
        self.height = 32
        self.velocity = 5

class Bird:
    def __init__(self):
        self.x = 500
        self.heights = [382, 358, 310]
        self.y = np.random.choice(self.heights, 1)[0]
        self.width = 40
        self.height = 16
        self.velocity = 5


def run():
    char = Character()
    world = Window(WIDTH, HEIGHT, char)

    while world.run:
        pygame.time.delay(30)
        world.update()
    pygame.quit()