import os
import pygame
import math

class AGC(pygame.sprite.Sprite):
    """An Agc cart object, move around points on the screen"""
    
    def __init__(self, X, Y):
        pygame.sprite.Sprite.__init__(self) #call Sprite initializer
        self.image, self.rect = load_image("agc.png")
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.rect.x = X
        self.rect.y = Y
        self.speed = 1


    def update(self):
        self._drive()

    def _drive(self):
        """Move the agc up and down changing dircetion if it will go off screen"""
        newpos = self.rect.move((0,self.speed))
        if not self.area.contains(newpos):
            if self.rect.top < self.area.top or self.rect.bottom > self.area.bottom:
                self.speed = -self.speed
                newpos = self.rect.move((0,self.speed))
        self.rect = newpos
        
        test = f"(X,Y): ({self.rect.x},{self.rect.y})"
        # print(test)

class Map():
    def __init__(self):
        self.nodes = []

    def add_nodes(self, node):
        self.nodes.append(node)

    def draw_map(self):
        pass
        

class Node():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.neighbors = []

    def add_neighbors(self, node):
        self.neighbors.append(node)


class Circle(pygame.sprite.Sprite):

    def __init__(self, x, y, radius = 25):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.image = pygame.Surface((radius*2, radius*2))
        self.image.fill((0,0,255))
        pygame.draw.circle(self.image, (255,255,255), (radius, radius), radius)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        
    def update(self):
         pass



def load_image(name):
    fullname = os.path.join("assets", name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print("Cannot load Image: ", name)
        raise SystemError(message)

    image = image.convert()

    return image, image.get_rect()

def sim():
    pygame.init()
    screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
    pygame.display.set_caption("AGC Simulation")

    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((0,0,0))

    screen.blit(background, (0,0))
    pygame.display.flip()

    agc = AGC(100, 50)



    circles = pygame.sprite.RenderPlain()

    for x in range(0, 1000, 100):
        # temp.append(Circle(x,100))
        circles.add(Circle(x,100))
        print("added : ", str(x))

    all_agc = pygame.sprite.RenderPlain((agc, AGC(300,50), AGC(500,50)))

    clock = pygame.time.Clock()

    print(circles)

    while True:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return
            

        circles.update()
        all_agc.update()

        screen.blit(background, (0,0))
        circles.draw(screen)
        all_agc.draw(screen)
        pygame.display.flip()


if __name__ == "__main__":
    sim()