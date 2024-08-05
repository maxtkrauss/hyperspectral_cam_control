import os
import platform
import sys
import time
from datetime import timedelta
import cuvis

def do_dark_calibration():
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
    recDir = os.path.join(os.getcwd(), "images", "calibration")

    # Parameters
    exposure = 250  # in ms
    distance = 700  # in mm
    new_file_name = "cubert_dark_calibration.cu3"

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

    # Save picture
    if mesu is not None:
        processingContext.apply(mesu)
        cubeExporter.apply(mesu)

        # Rename the cu3 file:
        exported_file = os.path.join(recDir, "Auto_001_0001_raw.cu3")
        new_name = os.path.join(recDir, new_file_name)
        if os.path.exists(exported_file):
            os.rename(exported_file, new_name)
            print(f"Renamed file to {new_name}")

        print("Done")
    else:
        print("Failed")

    print("Finished.")


if __name__ == "__main__":
    do_dark_calibration()