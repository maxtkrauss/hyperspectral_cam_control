# Hyperspectral Camera Control

## How to run:

### thorlabs_dark_calibration.py
Run it to create a master dark frame for the Thorlabs camera. It will be saved in images/calibration/thorlabs_dark. Remember to put on a cap to darken the sensor.

### cubert_dark_calibration.py
Run it to create a master dark frame for the Thorlabs camera. It will be saved in images/calibration/cubert_dark. Remember to put on a cap to darken the sensor.

### create_dataset_display.py
Run it to show the images in images/display on a second monitor and take pictures with a binocular setup using a Thorlabs and a Cubert camera. The image files will be saved in images/thorlabs and images/cubert respectively.

## Notes

### How to use the hyperspectral camera with Cubert software
- Ethernet cable into camera and mini pc
- Ethernet cable from mini pc to pc
- Power cable splits and goes into both mini pc and camera (secure by turning)
- Turn on Windows Remote Desktop on pc (name of mini pc needed)
- open the software ...Touch...
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

