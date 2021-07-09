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

class Line(pygame.sprite.Sprite):
    def __init__(self, start,end):
        pygame.sprite.Sprite.__init__(self)

        end_y =  end[1]

        self.width = 2
        self.length = self.get_length(start, end)

        self.image =  pygame.Surface((self.length,self.width))
        self.image.fill((255,255,255))
        pygame.draw.line(self.image, (255,255,255), (0,0), (0,end_y), self.width)
        self.rect = self.image.get_rect()
        x,y = start
        self.rect.centerx = x + self.length/2
        self.rect.centery = y + self.length/2

    def update(self):
        pass

    def get_length(self,start, end):
        x1, y1 = start
        x2, y2 = end

        return math.sqrt(pow((x2-x1),2) + pow((y2-y1),2))


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

    
    ########### AGC Set Up ####################
    agc = AGC(100, 50)
    all_agc = pygame.sprite.RenderPlain((agc, AGC(300,50), AGC(500,50)))

    ########### Circle Set Up ################
    circles = pygame.sprite.RenderPlain()

    circle_1 = Circle(200,200)
    circle_2 = Circle(200,500)
    circle_3 = Circle(500,500)
    circle_4 = Circle(500,200)

    circles.add(circle_1)
    circles.add(circle_2)
    circles.add(circle_3)
    circles.add(circle_4)

    ########### Line Set Up ####################

    lines = pygame.sprite.RenderPlain()

    line_1 = Line(circle_1.rect.center, circle_2.rect.center)
    line_2 = Line(circle_2.rect.center, circle_3.rect.center)
    line_3 = Line(circle_3.rect.center, circle_4.rect.center)
    line_4 = Line(circle_4.rect.center, circle_1.rect.center)

    lines.add(line_1)
    lines.add(line_2)
    lines.add(line_3)
    lines.add(line_4)
    
    clock = pygame.time.Clock()

    while True:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return
            
        lines.update()
        circles.update()
        all_agc.update()

        

        screen.blit(background, (0,0))
        lines.draw(screen)
        circles.draw(screen)
        all_agc.draw(screen)
        pygame.draw.line(screen, (22,255,255), (200,200), (200,500), 2)
        pygame.display.flip()


if __name__ == "__main__":
    sim()