# Hyperspectral Camera Control

## TODO
- add the option to also average the light frames
- align and crop (maybe downsample) the images so that both cameras image the same field of view (kind of done)
- Slideshow with multiple sample images
- rclone dataset to Google Drive
- Looking into difference of dfa patterns when shifting spatially
- Testing cross-correlation of different polarisations
- Cooling the Cubert cam
- Testing the ML algorithm

## How to run

### _run_pipeline.py
Runs all the steps in the usual data creation routine. Edit it how you like.

### thorlabs_dark_calibration.py
Run it to create a master dark frame for the Thorlabs camera. It will be saved in images/calibration/thorlabs_dark. Remember to put on a cap to darken the sensor.

### cubert_dark_calibration.py
Run it to create a master dark frame for the Thorlabs camera. It will be saved in images/calibration/cubert_dark. Remember to put on a cap to darken the sensor.

### create_dataset_display.py
Run it to show the images in images/display on a second monitor and take pictures with a binocular setup using a Thorlabs and a Cubert camera. The image files will be saved in images/thorlabs and images/cubert respectively.

### paired_image_viewer_v?.py
Showing images both with interactive tools to look at spectrum and polarisation

## Notes

### How to use the hyperspectral camera with Cubert software
- Ethernet cable into camera and mini pc
- Ethernet cable from mini pc to pc
- Power cable splits and goes into both mini pc and camera (secure by turning)
- Turn on Windows Remote Desktop on pc (name of mini pc needed)
- open the software Cubert Utils Touch
- calibrate the white point by using a white paper, then calbrate black point by putting the lens cap on
- Distance calibration optional

### Get ThorLabs Camera running
- pip install pylablib
- see examples in pylablib docs

### Get Cubert Camera running
- pip install cuvis
- get factory settings file from usb stick, put it into default folder mentioned in the github code
- see python examples on cubert-hyperspectral github

### Created slideshow using pygame
- see code example

## Documentation

### Setup for display imaging
- Thorlabs cam with 4f system, DFA, 50mm lens currently sitting on a rail
- Cubert cam at the same distance
- 4f system is currently introducing strong vignetting and field curvature because the flange distance was extended to have a closer min focus distance.

### Cropping of the images
- Currently the Thorlabs cam has a 50mm lens and the Cubert is sitting on the same plane as the Thorlabs lens
- The Thorlabs image is cropped to the visible size if the dfa (with a small safety border). The resulting size of the image is 4x900x900
- The Cubert cam is cropped to match the fov of the Thorlabs. That's a 106x42x42 image. We should possibly change the lens on the TL cam to have a wider fov and more resolution on the Cubert image.

### Polarisation channels of Thorlabs cam
- Polarisation demosaicing works by taking every fourth pixel according to a polarisation matrix in front of the sensor and interpolating the pixels in between with regard to the other polarisation channels.
- This results in four channel 2448 x 2408 image.
- After implementing polarisation demosaicing, it is quite visible that different polarisation channels show moderately different diffractive patterns even when imaging non polarized light.
- This is probably result of the four pixel array of the sensor. The size of a 2x2 super pixel is bigger than the structure of the dfa pattern so every pixel in the super pixel is getting a different diffraction. During demosaicing this will result in reconstructing the dfa pattern differently in different polarisation channels.
- Maybe this won't affect the machine learning model (?). To reduce this one could create the dfa with a structure that is the size of a 2x2 super pixel.
- The Pearson Correlation Coefficient matrix between different imaged colors is looking pretty similar for all polarisation channels though.

### HDR imaging
- HDR imaging will be implemented soon
- making multiple frames by passing in an array of exposure times
- using a cv2 hdr merging algorithm to create the HDR image
