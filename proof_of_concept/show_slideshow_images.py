import pygame
import os

import pygame.image

pygame.init()

x_res = 1920
y_res = 1080
x_size = 426
y_size = 240
x_offset = 0
y_offset = 200

scrn = pygame.display.set_mode((x_res, y_res), pygame.FULLSCREEN)

def transformScaleKeepRatio(image, size):
    iwidth, iheight = image.get_size()
    scale = min(size[0] / iwidth, size[1] / iheight)
    new_size = (round(iwidth * scale), round(iheight * scale))
    scaled_image = pygame.transform.scale(image, new_size)
    image_rect = scaled_image.get_rect(center = (size[0] // 2, size[1] // 2))
    return scaled_image, image_rect

# Load images
img_path = 'images/display'

images = []
filenames = [f for f in os.listdir(img_path) if f.endswith('.jpg')]
print(filenames)
for name in filenames:
    img = pygame.image.load(os.path.join(img_path, name))
    images.append((*transformScaleKeepRatio(img, (x_size, y_size)), name))

# Display images
for i in images:
    i[1].center = (x_res//2 + x_offset, y_res//2 + y_offset)
    pos = i[1]
    print(pos)
    scrn.blit(i[0], pos)
    pygame.display.flip()
    pygame.display.set_caption(i[2])
    pygame.time.wait(2000)

    for e in pygame.event.get():
        if e.type == pygame.QUIT or e.type == pygame.KEYDOWN:
            pygame.quit()

pygame.quit()