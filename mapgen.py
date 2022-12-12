import pygame

#Start up pygame modules
pygame.init()


#define window size
displayWidth = 800
displayHeight = 600

#setup display window surface
surface = pygame.display.set_mode((displayWidth, displayHeight))

#set the window name
pygame.display.set_caption('Image')

#load the image to draw
displayImage = pygame.image.load(r'ban.png')

while True:
    surface.fill((255, 255, 255))
    surface.blit(displayImage, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        pygame.display.update()
