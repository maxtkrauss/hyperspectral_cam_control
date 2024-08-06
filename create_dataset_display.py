### Create a dataset from displayed images with the hyperspectral cubert cam and the Thorlabs diffractive cam ###

import pylablib as pll
from pylablib.devices import Thorlabs as tl
import cuvis
import pygame

import os
import time
import platform
from datetime import timedelta

from PIL import Image
import numpy as np

## Parameters
display_image_folder = 'images/display'
thorlabs_image_folder = 'images/thorlabs'
cubert_image_folder = 'images/cubert'

display_x = 1280
display_y = 720

exposure_time_tl = 10 # in ms
exposure_time_cb = 250 # in ms

# Additional paramters for Thorlabs cam
do_dark_subtract_tl = True
roi_tl = (0, 2448, 0, 2048)

# Additional paramters for Cubert cam
do_dark_subtract_cb = True
distance_cb = 700 # in mm
get_time_cb = 2000 # in ms


## Main function
def main():
    # Setup the Thorlabs cam
    cam_tl = setup_thorlabs_cam()
    print("TL setup done.")

    # Get Thorlabs masterdark calibration frame
    if do_dark_subtract_tl:
        dark_calibration_tl = np.load(f"images//calibration//thorlabs_dark//masterdark_tl_{exposure_time_tl}ms.npy")

    # Setup the the Cubert cam
    acquisitionContext, processingContext, cubeExporter = setup_cubert_cam()
    print("CB setup done.")

    # Calibrate the Cubert cam
    if do_dark_subtract_cb:
        dark_calibration_cb = None

    # Set up the pygame display and images
    scrn, images_disp = setup_pygame_display(display_x, display_y, display_image_folder)
    print("Pygame setup done.")

    # Wait a few seconds so the monitor can update
    pygame.time.wait(1000)

    # Loop over all loaded display images
    for img_disp in images_disp:

        # Display image
        img_data, img_center, img_name = img_disp
        scrn.blit(img_data, img_center) # image data, image center
        pygame.display.flip()
        pygame.display.set_caption(img_name) # image name
        print(f"\nShowing image {img_name} on display.")

        # Take photo with Thorlabs cam
        if do_dark_subtract_tl:
            img_tl = cam_tl.snap() - dark_calibration_tl
        else:
            img_tl = cam_tl.snap()
        print(f"Taking {exposure_time_tl}ms exposure with TL cam.")

        # Save Thorlabs image
        im_tl = Image.fromarray(img_tl)
        im_tl.save(os.path.join(thorlabs_image_folder, img_name[:-4] + "_thorlabs.tif"))
        print(f"Saving TL cam image. (Max: {np.max(img_tl)}, Min: {np.min(img_tl)})")

        # Taking and saving photo with Cubert cam
        take_and_save_cubert_image(img_name, acquisitionContext, processingContext, cubeExporter)

        # wait half a second
        pygame.time.wait(500)

        # test if pygame should stop
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                print("Quitting.")
                pygame.quit()

        pass

    print("\nDataset creation finished. Quitting.")
    pygame.quit()


## setup everything for the Thorlabs camera
def setup_thorlabs_cam():
    tl.list_cameras_tlcam()
    cam = tl.ThorlabsTLCamera()
    cam.set_exposure(exposure_time_tl * 1e-3)
    cam.set_roi(*roi_tl, hbin=1, vbin=1)
    return cam

## setup everything for the Thorlabs camera
def setup_cubert_cam():
    # Default directories and files:
    data_dir = None
    lib_dir = None

    if platform.system() == "Windows":
        lib_dir = os.getenv("CUVIS")
        data_dir = os.path.normpath(os.path.join(lib_dir, os.path.pardir, "sdk", "sample_data", "set_examples"))
    elif platform.system() == "Linux":
        lib_dir = os.getenv("CUVIS_DATA")
        data_dir = os.path.normpath(os.path.join(lib_dir, "sample_data", "set_examples"))

    # Default factory directory:
    factory_dir = os.path.join(lib_dir, os.pardir, "factory")

    # Default settings and output directories:
    userSettingsDir = os.path.join(data_dir, "settings")

    # Start camera
    print("Loading user settings...")
    settings = cuvis.General(userSettingsDir)
    settings.set_log_level("info")

    print("Loading calibration, processing, and acquisition context (factory)...")
    calibration = cuvis.Calibration(factory_dir)
    processingContext = cuvis.ProcessingContext(calibration)
    acquisitionContext = cuvis.AcquisitionContext(calibration)

    saveArgs = cuvis.SaveArgs(export_dir=cubert_image_folder, allow_overwrite=True, allow_session_file=True)
    cubeExporter = cuvis.CubeExporter(saveArgs)

    # Wait for camera to come online
    while acquisitionContext.state == cuvis.HardwareState.Offline:
        print(".", end="")
        time.sleep(1)
    print("\nCubert camera is online.")

    # Set acquisition context parameters
    acquisitionContext.operation_mode = cuvis.OperationMode.Software
    acquisitionContext.integration_time = exposure_time_cb
    processingContext.calc_distance(distance_cb)

    return acquisitionContext, processingContext, cubeExporter

def take_and_save_cubert_image(img_name, acquisitionContext, processingContext, cubeExporter):
    imaging_failed_counter = 0
    # Try taking and siving images until it works.
    while imaging_failed_counter < 5:
        # Take photo with Cubert cam
        print(f"Taking {exposure_time_cb}ms exposure with CB cam...")
        am = acquisitionContext.capture()
        mesu, res = am.get(timedelta(milliseconds=get_time_cb))

        # Save Cubert image
        if mesu is not None:
            mesu.set_name(img_name[:-4] + "_cubert")
            processingContext.apply(mesu)
            print("Export CB image to multi-channel .tif...")
            multi_tiff_settings = cuvis.TiffExportSettings(export_dir=cubert_image_folder, format=cuvis.TiffFormat.MultiChannel)
            multiTiffExporter = cuvis.TiffExporter(multi_tiff_settings)
            multiTiffExporter.apply(mesu)
            print("CB image saved.")
            break
        else:   
            print(f"CB image saving failed. Counter: {imaging_failed_counter}")
            imaging_failed_counter += 1

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