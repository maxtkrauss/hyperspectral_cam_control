import pygame
import os

import pygame.image

pygame.init()

X = 1280
Y = 720

scrn = pygame.display.set_mode((X, Y))

def transformScaleKeepRatio(image, size):
    iwidth, iheight = image.get_size()
    scale = min(size[0] / iwidth, size[1] / iheight)
    new_size = (round(iwidth * scale), round(iheight * scale))
    scaled_image = pygame.transform.scale(image, new_size)
    image_rect = scaled_image.get_rect(center = (size[0] // 2, size[1] // 2))
    return scaled_image, image_rect

# Load images
img_path = 'proof_of_concept\slideshow_test_images'

images = []
filenames = [f for f in os.listdir(img_path) if f.endswith('.jpg')]
print(filenames)
for name in filenames:
    img = pygame.image.load(os.path.join(img_path, name))
    images.append((*transformScaleKeepRatio(img, (X, Y)), name))

# Display images
for i in images:
    scrn.blit(i[0], i[1])
    pygame.display.flip()
    pygame.display.set_caption(i[2])
    pygame.time.wait(2000)

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()

pygame.quit()