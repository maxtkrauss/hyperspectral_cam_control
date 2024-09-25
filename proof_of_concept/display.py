import pygame
import os

# Parameters
display_image_folder = 'images\\display\\dataset'

display_x = 1920
display_y = 1080
img_size_x = 426*2
img_size_y = 240*2
img_offset_x = 0
img_offset_y = 180

def main():
    # Set up the pygame display
    scrn, img_disp = setup_pygame_display(display_x, display_y, img_size_x, img_size_y, display_image_folder)
    print("Pygame setup done.")

    # Display the image and hold the screen
    display_image(img_disp, scrn)

    # Wait until the user quits
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                pygame.quit()
                return

## setup pygame and load one image for display
def setup_pygame_display(X, Y, img_size_x, img_size_y, img_path):
    # Pygame and display setup
    pygame.init()
    try:
        scrn = pygame.display.set_mode((X, Y), pygame.FULLSCREEN, display=1) # show on second monitor
    except:
        print("No second monitor available, using main monitor.")
        scrn = pygame.display.set_mode((X, Y), pygame.FULLSCREEN)

    def transformScaleKeepRatio(image, size):
        iwidth, iheight = image.get_size()
        scale = min(size[0] / iwidth, size[1] / iheight)
        new_size = (round(iwidth * scale), round(iheight * scale))
        scaled_image = pygame.transform.scale(image, new_size)
        image_rect = scaled_image.get_rect(center = (size[0] // 2, size[1] // 2))
        return scaled_image, image_rect

    # Load one image
    filenames = [f for f in os.listdir(img_path) if f.endswith('.jpg') or f.endswith('.png')]
    if filenames:
        img = pygame.image.load(os.path.join(img_path, filenames[0]))
        img_disp = (*transformScaleKeepRatio(img, (img_size_x, img_size_y)), filenames[0])
        return scrn, img_disp
    else:
        raise FileNotFoundError("No images found in the specified folder.")

## display image on screen with pygame
def display_image(img_disp, scrn):
    img_data, img_center, img_name = img_disp
    img_center.center = (display_x//2 + img_offset_x, display_y//2 + img_offset_y)
    scrn.blit(img_data, img_center) # image data, image center
    pygame.display.flip()
    pygame.display.set_caption(img_name) # image name
    print(f"\nShowing image {img_name} on display.")

## Run main
if __name__ == "__main__":
    main()
