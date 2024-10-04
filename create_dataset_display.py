import pylablib as pll
from pylablib.devices import Thorlabs as tl
import cuvis
import pygame

import os
import time
import platform
from datetime import timedelta

import tifffile
import numpy as np
import polanalyser as pa

## Parameters
display_image_folder = 'images/display'
thorlabs_image_folder = 'images/thorlabs'
cubert_image_folder = 'images/cubert'

display_x = 1920
display_y = 1080
img_size_x = 426*2.5
img_size_y = 240*2.5
img_offset_x = 0
img_offset_y = 180

exposure_time_tl = 1000 # in ms
exposure_time_cb = 500 # in ms

# Additional paramters for Thorlabs cam
do_dark_subtract_tl = True
path_dark_tl = f"images//calibration//thorlabs_dark//masterdark_tl_{exposure_time_tl}ms.npy"
roi_tl = (0, 2448, 0, 2048)

# Additional paramters for Cubert cam
do_dark_subtract_cb = True
path_dark_cb = f"images//calibration//cubert_dark//masterdark_cb_{exposure_time_cb}ms.npy"

distance_cb = 800 # in mm

# Cropping parameters
crop_tl = ((610, 1610), (291, 1291))  #((550-50, 1350+50), (850-50, 1650+50))
crop_cb = ((2, 122), (128, 248)) #((188+3, 234-1), (64+3, 110-1))

## Main function
def main():
    # Setup the Thorlabs cam
    cam_tl = setup_thorlabs_cam()
    print("TL setup done.")

    # Get Thorlabs masterdark calibration frame
    if do_dark_subtract_tl:
        dark_calibration_tl = np.load(path_dark_tl)

    # Setup the the Cubert cam
    acquisitionContext, processingContext, cubeExporter = setup_cubert_cam()
    print("CB setup done.")

    # Calibrate the Cubert cam
    if do_dark_subtract_cb:
        dark_calibration_cb = np.load(path_dark_cb)

    # Set up the pygame display and images
    scrn, images_disp = setup_pygame_display(display_x, display_y, img_size_x, img_size_y, display_image_folder)
    print("Pygame setup done.")

    # Wait a few seconds so the monitor can update
    pygame.time.wait(1000)

    # Loop over all loaded display images
    for img_disp in images_disp:

        # Display image
        img_name = display_image(img_disp=img_disp, scrn=scrn)

        # Taking and saving photo with Thorlabs cam
        tl_success, cam_tl = take_and_save_thorlabs_image(img_name=img_name, dark_cal=dark_calibration_tl, cam_tl=cam_tl)

        # Taking and saving photo with Cubert cam
        if tl_success:
            take_and_save_cubert_image(img_name=img_name, dark_cal=dark_calibration_cb, acquContext=acquisitionContext, procContext=processingContext)
        else:
            print("Skipping CB image because TL imaging was unsuccessful.")

        # wait a second
        pygame.time.wait(1000)

        # test if pygame should stop
        for e in pygame.event.get():
            if e.type == pygame.QUIT or e.type == pygame.KEYDOWN:
                print("Quitting.")
                pygame.quit()

    print("\nDataset creation finished. Quitting.")
    cam_tl.close()
    pygame.quit()


## setup everything for the Thorlabs camera
## setup everything for the Thorlabs camera
def setup_thorlabs_cam():
    tl.list_cameras_tlcam()
    cam = tl.ThorlabsTLCamera()
    cam.set_exposure(exposure_time_tl * 1e-3)
    cam.set_roi(*roi_tl, hbin=1, vbin=1)
    return cam

## take cubert image as array, do dark calibration and save that as a tiff
def take_and_save_thorlabs_image(img_name, dark_cal, cam_tl):
    imaging_failed_counter = 0
    success = False

    # Try taking and saving images until it works (max 15 times).
    while imaging_failed_counter < 15:
        print(f"TL: Taking {exposure_time_tl}ms exposure with TL cam...")
        try:
            if do_dark_subtract_tl:
                img_tl = cam_tl.snap() - dark_cal
                img_tl = np.maximum(img_tl, 0)
            else:
                img_tl = cam_tl.snap()
            print("TL: Imaging successfull.")
            success = True
            break
        except:
            imaging_failed_counter += 1
            print(f"TL: Imaging failed. Restarting cam. Counter {imaging_failed_counter}")
            cam_tl.close()
            cam_tl = setup_thorlabs_cam()

    if success:
        # Demonsaicing to different polarization channels
        img_tl_pol = pa.demosaicing(img_raw=img_tl, code=pa.COLOR_PolarMono)
        img_tl_pol = np.append(img_tl_pol, [img_tl], axis=0)

        # Crop to size of DFA
        img_tl_pol = img_tl_pol[:, crop_tl[1][0]:crop_tl[1][1], crop_tl[0][0]:crop_tl[0][1]]

        # Save Thorlabs image
        path = os.path.join(thorlabs_image_folder, img_name + "_thorlabs.tif")
        tifffile.imwrite(path, img_tl_pol,  photometric='minisblack')
        print(f"TL: Saved image as tiff. (Shape: {img_tl_pol.shape}, Max: {np.max(img_tl_pol)}, Min: {np.min(img_tl_pol)}, Avg: {np.average(img_tl_pol)}, SNR: {snr(img_tl_pol)})")
    else:
        print("TL: No image to save.")

    # Returnign cam_tl in case the camera had to be restarted
    return success, cam_tl

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

## take cubert image, extract raw data, do dark calibration and save that as a tiff
def take_and_save_cubert_image(img_name, dark_cal, acquContext, procContext):
    imaging_failed_counter = 0
    saved = False
    # Try taking and saving images until it works (max 5 times).
    while imaging_failed_counter < 15:
        time.sleep(0.5)
        # Take photo with Cubert cam
        print(f"CB: Taking {exposure_time_cb}ms exposure with CB cam...")
        try:
            am = acquContext.capture()
            mesu, res = am.get(timedelta(milliseconds=1000))
        except:
            mesu = None
            imaging_failed_counter += 1
            print(f"CB: imaging failed. Counter: {imaging_failed_counter}")


        # Save Cubert image
        if mesu is not None:
            mesu.set_name(img_name + "_cubert")
            procContext.apply(mesu)
            print("CB: Exporting image to multi-channel .tif...")
            # get array from mesurement
            data_array = np.array(mesu.data['cube'].array)
            # dark subtraction
            if do_dark_subtract_cb:
                data_array = data_array.astype(float) - dark_cal.astype(float)
                data_array = np.maximum(data_array, 0)
            else:
                data_array = data_array.astype(float)
            # switch third (spectral) dimension to first dimension
            data_array = data_array.transpose(2,0,1)
            # crop cube
            data_array = data_array[:, crop_cb[1][0]:crop_cb[1][1], crop_cb[0][0]:crop_cb[0][1]]
            if snr(data_array) > 0.05:
                # save as tif
                path = os.path.join(cubert_image_folder, img_name + "_cubert.tif")
                tifffile.imwrite(path, data_array,  photometric='minisblack')
                print(f"CB: Saved image as tiff. (Shape: {data_array.shape}, Max: {np.max(data_array)}, Min: {np.min(data_array)}, Avg: {np.average(data_array)}, SNR: {snr(data_array)})")
                saved = True
                # end while loop
                break
            else:
                imaging_failed_counter += 1
                print(f"CB: Image saving failed. Counter: {imaging_failed_counter}")
        else:   
            imaging_failed_counter += 1
            print(f"CB: Image saving failed. Counter: {imaging_failed_counter}")
    if saved == False:
        # delete TL image
        print("CB: Deleting corresponding TL image because CB image saving failed...")
        try: 
            os.remove(os.path.join(thorlabs_image_folder, 
             + "_thorlabs.tif"))
            print("CB: Deleted corresponding TL image.")
        except:
            print("CB: TL image could not be deleted.")
        

## setup pygame and load images for the display
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

    # Load images
    images = []
    filenames = sorted([f for f in os.listdir(img_path) if f.endswith('.jpg') | f.endswith('.png')], reverse=False)
    print("Filenames:", filenames)
    for name in filenames:
        img = pygame.image.load(os.path.join(img_path, name))
        images.append((*transformScaleKeepRatio(img, (img_size_x, img_size_y)), name))

    return scrn, images

## display image on screen with pygame
def display_image(img_disp, scrn):
    img_data, img_center, img_name = img_disp
    img_center.center = (display_x//2 + img_offset_x, display_y//2 + img_offset_y)
    scrn.blit(img_data, img_center) # image data, image center
    pygame.display.flip()
    pygame.display.set_caption(img_name) # image name
    print(f"\nShowing image {img_name} on display.")
    return img_name

## calc SNR
def snr(img, axis=None, ddof=0):
    img = np.asanyarray(img)
    m = img.mean(axis)
    sd = img.std(axis=axis, ddof=ddof)
    return np.where(sd == 0, 0, m/sd)

## Run main
if __name__ == "__main__":
    main()