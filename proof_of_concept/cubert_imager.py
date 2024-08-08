import os
import platform
import sys
import time
from datetime import timedelta
import cuvis
import numpy as np
import tifffile as tiff

# Default directories and files:
data_dir = None
lib_dir = None

dark_calibration_cb = np.load(f"images//calibration//cubert_dark//masterdark_cb_250ms.npy")

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
recDir = os.path.join(os.getcwd(), "proof_of_concept", "images_cubert")

# Parameters
exposure = 250  # in ms
distance = 700  # in mm

# TIFF filename:
tiff_filename =  "calibration_testing"

# Start camera
print("Loading user settings...")
settings = cuvis.General(userSettingsDir)
settings.set_log_level("info")

print("Loading calibration, processing, and acquisition context (factory)...")
calibration = cuvis.Calibration(factory_dir)
processingContext = cuvis.ProcessingContext(calibration)
acquisitionContext = cuvis.AcquisitionContext(calibration)

saveArgs = cuvis.SaveArgs(export_dir=recDir, allow_overwrite=True, allow_session_file=True)
cubeExporter = cuvis.CubeExporter(saveArgs)

# Wait for camera to come online
while acquisitionContext.state == cuvis.HardwareState.Offline:
    print(".", end="")
    time.sleep(1)
print("\nCamera is online")

# Set acquisition context parameters
acquisitionContext.operation_mode = cuvis.OperationMode.Software
acquisitionContext.integration_time = exposure
processingContext.calc_distance(distance)

# Take picture
print("Image recording...")
am = acquisitionContext.capture()
mesu, res = am.get(timedelta(milliseconds=1000))

# Process image in raw
if mesu is not None:
    mesu.set_name(tiff_filename)
    processingContext.apply(mesu)
    test = np.array(mesu.data['cube'].array)
    print(test.shape)
    test = test - dark_calibration_cb.astype(float)
    result_data = np.maximum(test, 0)
    tiff.imwrite("proof_of_concept\\images_cubert\\calib_test.tiff", result_data,  photometric='minisblack')

    # print("Export to Multi-Channel Tiff...")
    # multi_tiff_settings = cuvis.TiffExportSettings(export_dir=recDir, format=cuvis.TiffFormat.MultiChannel)
    # multiTiffExporter = cuvis.TiffExporter(multi_tiff_settings)
    # multiTiffExporter.apply(mesu)

    print("Done")
else:   
    print("Failed")

# Process image in dark subtract 
# if mesu is not None:
#     mesu.set_name(tiff_filename)
#     procArgs = cuvis.ProcessingArgs()
#     procArgs.processing_mode = cuvis.ProcessingMode.DarkSubtract
#     processingContext.set_processing_args(procArgs)
#     processingContext.apply(mesu)

#     print("Export to Multi-Channel Tiff...")
#     multi_tiff_settings = cuvis.TiffExportSettings(export_dir=recDir, format=cuvis.TiffFormat.MultiChannel)
#     multiTiffExporter = cuvis.TiffExporter(multi_tiff_settings)

#     multiTiffExporter.apply(mesu)

#     print("Done")
# else:
#     print("Failed")


print("Finished.")