import os
import platform
import sys
import time
from datetime import timedelta
import cuvis
import numpy as np

def do_dark_calibration(exp_time = 250, n_frames = 10, dist = 800):

    print("REMEMBER TO PUT THE CAP ON.")

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
    recDir = os.path.join(os.getcwd(), "images", "calibration", "cubert_dark")

    # Parameters
    exposure = exp_time  # in ms
    distance = dist  # in ms
    n_calibration_frames = n_frames

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

    data_arrays = []

    # Take pictures
    i = 0
    imaging_failed_counter = 0
    while i < n_calibration_frames:
        print(f"Image recording... {i}")
        try:
            am = acquisitionContext.capture()
            m, r = am.get(timedelta(milliseconds=1000))
        except:
            m = None
            imaging_failed_counter += 1
            print(f"CB: imaging failed. Counter: {imaging_failed_counter}")

        if m is not None:
            processingContext.apply(m)
            data_arrays.append(np.array(m.data['cube'].array))
            i += 1
        else:
            print("Imaging failed. Trying again.")

    # Stack the data arrays along a new axis and compute the average
    stacked_data = np.stack(data_arrays, axis=0)
    average_data = np.mean(stacked_data, axis=0)

    # Print the shape of the averaged data
    print("Shape of Master Dark:", average_data.shape)
    print("Max of Master Dark:", np.max(average_data))
    print("Min of Master Dark:", np.min(average_data))
    print("Std of Master Dark:", np.std(average_data))
    # print("Averaged data shape:", average_data.shape)
    # print("Averaged data (sample values):", average_data[0, 0, :])

    # saving
    np.save(f'images/calibration/cubert_dark/masterdark_cb_{exposure}ms.npy', average_data)

    print("Finished dark calibration")


if __name__ == "__main__":
    do_dark_calibration()