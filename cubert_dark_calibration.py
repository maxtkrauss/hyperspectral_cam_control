import os
import platform
import sys
import time
from datetime import timedelta
import cuvis
import numpy as np

def do_dark_calibration():

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
    exposure = 250  # in ms
    distance = 700  # in mm
    n_calibration_frames = 10

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

    mesu = []
    res = []

    # Take pictures
    for i in range(n_calibration_frames):
        print("Image recording...")
        am = acquisitionContext.capture()
        m, r = am.get(timedelta(milliseconds=1000))
        mesu.append(m)
        res.append(r)

    # data_arrays = []
    # for i in range(n_calibration_frames):
    #     data_arrays.append(np.array(mesu[i].data['cube'].array))

    for i in range(n_calibration_frames):
        processingContext.apply(mesu[i])
        cubeExporter.apply(mesu[i])

    time.sleep(5)

    # Initialize a list to store the data arrays
    data_arrays = []

    # Load each .cu3s file and add the data array to the list
    count = 0
    for i in range(1,10):
        file_path = os.path.join(recDir, f"Auto_00{i}.cu3s")
        measurement = cuvis.SessionFile(file_path)[0]
        data = measurement.data['cube']
        data_array = np.array(data.array)
        data_arrays.append(data_array)

    # Stack the data arrays along a new axis and compute the average
    stacked_data = np.stack(data_arrays, axis=0)
    average_data = np.mean(stacked_data, axis=0)

    # Print the shape of the averaged data
    print("Averaged data shape:", average_data.shape)
    print("Averaged data (sample values):", average_data[0, 0, :])

    # saving
    np.save(f'images/calibration/cubert_dark/masterdark_cb_{exposure}ms.npy', average_data)

    print("Finished dark calibration")


if __name__ == "__main__":
    do_dark_calibration()