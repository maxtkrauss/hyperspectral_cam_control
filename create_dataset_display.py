### Create a dataset from displayed images with the hyperspectral cubert cam and the Thorlabs diffractive cam ###

import pylablib as pll
#import cuvis
import pygame
import os

# Parameters
display_image_folder = 'images/display'
thorlabs_image_folder = 'images/thorlabs'
cubert_image_folder = 'images/cubert'

display_x = 1280
display_y = 720


## Main function
def main():
    # Setup the Thorlabs cam

    # Setup the the Cubert cam

    # Calibrate the Cubert cam

    # Set up the pygame display and images
    scrn, images = setup_pygame_display(display_x, display_y, display_image_folder)

    # Wait a few seconds so the monitor can update
    pygame.time.wait(2000)

    # Loop over all loaded images
    for img in images:

        # Display image
        scrn.blit(img[0], img[1]) # image data, image center
        pygame.display.flip()
        pygame.display.set_caption(img[2]) # image name

        # Take photo with Thorlabs cam

        # Save Thorlabs image

        # Take photo with Cubert cam

        # Save Cubert image

        # wait half a second
        pygame.time.wait(500)

        # test if pygame should stop
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()

        pass

    pygame.quit()

## setup pygame and load images for the display
def setup_pygame_display(X, Y, img_path):
    # Pygame and display setup
    pygame.init()
    try:
        scrn = pygame.display.set_mode((X, Y), display=1) # show on second monitor
    except:
        print("No second monitor available, using main monitor.")
        scrn = pygame.display.set_mode((X, Y))

    def transformScaleKeepRatio(image, size):
        iwidth, iheight = image.get_size()
        scale = min(size[0] / iwidth, size[1] / iheight)
        new_size = (round(iwidth * scale), round(iheight * scale))
        scaled_image = pygame.transform.scale(image, new_size)
        image_rect = scaled_image.get_rect(center = (size[0] // 2, size[1] // 2))
        return scaled_image, image_rect

    # Load images
    images = []
    filenames = [f for f in os.listdir(img_path) if f.endswith('.jpg')]
    print("Filenames:", filenames)
    for name in filenames:
        img = pygame.image.load(os.path.join(img_path, name))
        images.append((*transformScaleKeepRatio(img, (X, Y)), name))

    return scrn, images

## Run main
if __name__ == "__main__":
    main()