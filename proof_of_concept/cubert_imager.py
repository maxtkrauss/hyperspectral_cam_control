import os
import platform
import sys
import time
from datetime import timedelta
import cuvis

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
recDir = os.path.join(os.getcwd(), "proof_of_concept", "images_cubert")

# Dark and white calibration images:
dark_dir = os.path.join(recDir, "single_dark_1.cu3s")
white_dir = os.path.join(recDir, "single_white_1.cu3s")

# Parameters
exposure = 250  # in ms
distance = 700  # in mm

# TIFF filename:
tiff_filename =  "spectra_analysis.tiff"
reflectance_tiff_filename = "ref_spectra_analysis.tiff"

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

# Load dark and white calibration images
print("Loading dark and white calibration images...")
#dark = cuvis.SessionFile(dark_dir)[0]
#white = cuvis.SessionFile(white_dir)[0]

# Set references in processing context
#processingContext.set_reference(dark, cuvis.ReferenceType.Dark)
#processingContext.set_reference(white, cuvis.ReferenceType.White)

# Save picture
if mesu is not None:
    processingContext.apply(mesu)
    cubeExporter.apply(mesu)

    print("Export to Multi-Channel Tiff...")
    multi_tiff_settings = cuvis.TiffExportSettings(export_dir=recDir, format=cuvis.TiffFormat.MultiChannel)
    multiTiffExporter = cuvis.TiffExporter(multi_tiff_settings)
    multiTiffExporter.apply(mesu)

    # Rename the tiff file:
    exported_file = os.path.join(recDir, "Auto_001_0001_raw.tiff")
    new_name = os.path.join(recDir, tiff_filename)
    if os.path.exists(exported_file):
        os.rename(exported_file, new_name)
        print(f"Renamed file to {new_name}")

    print("Done")
else:
    print("Failed")

# # Process image in reflectance mode
# if mesu is not None:
#     procArgs = cuvis.ProcessingArgs()
#     procArgs.processing_mode = cuvis.ProcessingMode.Reflectance
#     processingContext.set_processing_args(procArgs)
#     processingContext.apply(mesu)

#     print("Export to Multi-Channel Tiff...")
#     multi_tiff_settings = cuvis.TiffExportSettings(export_dir=recDir, format=cuvis.TiffFormat.MultiChannel)
#     multiTiffExporter = cuvis.TiffExporter(multi_tiff_settings)

#     multiTiffExporter.apply(mesu)

#     # Rename the tiff file:
#     exported_file = os.path.join(recDir, "Auto_001_0001_raw.tiff")
#     new_name = os.path.join(recDir, reflectance_tiff_filename)
#     if os.path.exists(exported_file):
#         os.rename(exported_file, new_name)
#         print(f"Renamed file to {new_name}")

#     print("Done")
# else:
#     print("Failed")


print("Finished.")
