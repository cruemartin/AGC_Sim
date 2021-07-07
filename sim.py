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
        print(test)
        
      

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

    allsprites = pygame.sprite.RenderPlain(agc)

    clock = pygame.time.Clock()

    while True:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return
            
        allsprites.update()

        screen.blit(background, (0,0))
        allsprites.draw(screen)
        pygame.display.flip()


if __name__ == "__main__":
    sim()