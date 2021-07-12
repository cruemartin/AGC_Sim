import os
import pygame
import math

WHITE = (255,255,255)
BLACK = (0,0,0)
BLUE = (0,0,255)
GREEN = (0,255,0)
RED = (255,0,0)

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
        self.move_x = 0 
        self.move_y = 1 


    def update(self):
        self._drive()

    def _drive(self):
        """Move the agc up and down changing dircetion if it will go off screen"""

        # newpos = self.rect.move((0,self.speed))
        newpos = self.rect.move((self.move_x, self.move_y))

        if newpos.y % 100 == 0 and newpos.x % 100 != 0:
            print("y= " + str(newpos.y) + "move down")
            self.move_y = 0
            self.move_x = 1

        elif newpos.x % 100 == 0 and newpos.y % 100 != 0:

            print("x= " + str(newpos.x) + "move down")
            self.move_y = 1
            self.move_x = 0

        if not self.area.contains(newpos):
            self.speed = -self.speed
            newpos = self.rect.move((0,self.speed))
        self.rect = newpos

class AGV():
    """A class for the agv cart object, this is a class i am rolling with out the use if the sprite parent class"""
    
    def __init__(self, X, Y, screen):
        self.x = X
        self.y = Y
        self.screen = screen
        self.rect =  None
        self.speed = 1  

        self.right = True

        # self.rect = Rect(self.x, self.y, 50,100)



    # def draw(self):

    #     if self.right:
    #         self.drive_right()

    #     temp_rect = pygame.draw.rect(self.screen, GREEN, (self.x, self.y, 100,50))

    #     if not self.rect :
    #         self.rect = temp_rect

    # def drive_left(self):
    #     pass
    
    # def drive_right(self):
    #     self.x += self.speed

        

class Map():
    def __init__(self, screen):
        self.nodes = []
        self.screen = screen

    def add_nodes(self, node):
        self.nodes.append(node)

    def draw_map(self):
        for node in self.nodes:
            node.draw()

        self.draw_lines()

    
    def draw_lines(self):

        for node in self.nodes:
            start = node.x, node.y
            
            for neighbor in node.neighbors:
                end =  neighbor.x, neighbor.y
                pygame.draw.line(self.screen, WHITE, start, end, width=2)

class Node():
    def __init__(self, x, y, screen, radius = 10):
        self.x = x
        self.y = y
        self.radius = radius
        self.neighbors = []
        self.screen = screen
        self.rect = None

    def add_neighbors(self, node):
        self.neighbors.append(node)

    def draw(self):
        temp_rect = pygame.draw.circle(self.screen, WHITE, (self.x,self.y), self.radius)
        if not self.rect:
            self.rect = temp_rect



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
    agc = AGC(101, 101)
    all_agc = pygame.sprite.RenderPlain((agc))

    agv = AGV(300,100,screen)

    ########### Circle Set Up ################

    my_map = Map(screen)

    node_1 = Node(200,200,screen)
    node_2 = Node(200,500,screen)
    node_3 = Node(500,500,screen)
    node_4 = Node(500,200,screen)

    node_1.add_neighbors(node_2)
    node_2.add_neighbors(node_3)
    node_3.add_neighbors(node_4)
    node_4.add_neighbors(node_1)
    node_4.add_neighbors(node_2)

    my_map.add_nodes(node_1)
    my_map.add_nodes(node_2)
    my_map.add_nodes(node_3)
    my_map.add_nodes(node_4)

    ########### Line Set Up ####################

   
    clock = pygame.time.Clock()

    while True:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return
            
        # lines.update()
        all_agc.update()

        

        screen.blit(background, (0,0))
        # lines.draw(screen)
        
        my_map.draw_map()

        # agv.draw()

        all_agc.draw(screen)
        # pygame.draw.line(screen, (22,255,255), (200,200), (200,500), 2)
        pygame.display.flip()

        


if __name__ == "__main__":
    sim()