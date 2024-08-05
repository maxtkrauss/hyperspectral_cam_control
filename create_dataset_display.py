### Create a dataset from displayed images with the hyperspectral cubert cam and the Thorlabs diffractive cam ###

import pylablib as pll
from pylablib.devices import Thorlabs as tl
#import cuvis
import pygame
import os
import image

# Parameters
display_image_folder = 'images/display'
thorlabs_image_folder = 'images/thorlabs'
cubert_image_folder = 'images/cubert'

display_x = 1280
display_y = 720

exposure_time_tl = 250
exposure_time_cb = 250

## Main function
def main():
    # Setup the Thorlabs cam
    cam_tl = setup_thorlabs_cam()

    # Setup the the Cubert cam

    # Calibrate the Cubert cam

    # Set up the pygame display and images
    scrn, images_disp = setup_pygame_display(display_x, display_y, display_image_folder)

    # Wait a few seconds so the monitor can update
    pygame.time.wait(1000)

    # Loop over all loaded display images
    for img_disp in images_disp:

        # Display image
        scrn.blit(img_disp[0], img_disp[1]) # image data, image center
        pygame.display.flip()
        pygame.display.set_caption(img_disp[2]) # image name

        # Take photo with Thorlabs cam
        img_tl = cam_tl.snap()

        # Save Thorlabs image
        im_tl = image.from_array(img_tl)
        im_tl.save(os.path.join(thorlabs_image_folder, img_disp[2] + "_tl"))

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


## setup everything for the Thorlabs camera
def setup_thorlabs_cam():
    cam = tl.ThorlabsTLCamera()
    cam.set_exposure(exposure_time_tl)
    cam.set_roi(0, 640, 0, 640, hbin=1, vbin=1)
    return cam

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