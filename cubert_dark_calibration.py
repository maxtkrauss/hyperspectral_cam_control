import cuvis
import numpy as np
import os
import time
from datetime import timedelta
import platform

## Parameters
cubert_dark_frame_folder = "images/calibration/cubert_dark"
exposure_time_cb = 700  # in ms
num_dark_frames = 10

def setup_cubert_cam():
    # Detect the platform and set directories
    data_dir = None
    lib_dir = None

    if platform.system() == "Windows":
        lib_dir = os.getenv("CUVIS")
        data_dir = os.path.normpath(os.path.join(lib_dir, os.path.pardir, "sdk", "sample_data", "set_examples"))
    elif platform.system() == "Linux":
        lib_dir = os.getenv("CUVIS_DATA")
        data_dir = os.path.normpath(os.path.join(lib_dir, "sample_data", "set_examples"))

    factory_dir = os.path.join(lib_dir, os.pardir, "factory")
    userSettingsDir = os.path.join(data_dir, "settings")

    # Start camera
    print("Loading user settings...")
    settings = cuvis.General(userSettingsDir)
    settings.set_log_level("info")

    print("Loading calibration, processing, and acquisition context (factory)...")
    calibration = cuvis.Calibration(factory_dir)
    processingContext = cuvis.ProcessingContext(calibration)
    acquisitionContext = cuvis.AcquisitionContext(calibration)

    # Wait for camera to come online
    while acquisitionContext.state == cuvis.HardwareState.Offline:
        print(".", end="")
        time.sleep(1)
    print("\nCubert camera is online.")

    acquisitionContext.operation_mode = cuvis.OperationMode.Software
    acquisitionContext.integration_time = exposure_time_cb

    return acquisitionContext

def take_dark_frame(acquisitionContext):
    print(f"Capturing {exposure_time_cb}ms dark frame...")
    am = acquisitionContext.capture()
    mesu, res = am.get(timedelta(milliseconds=1000))
    if mesu is not None:
        dark_frame = np.array(mesu.data['cube'].array, dtype=float)
        print("Dark frame captured successfully.")
        return dark_frame
    else:
        print("Failed to capture dark frame.")
        return None

def save_master_dark(dark_frame_avg, folder, exposure_time):
    filename = f"masterdark_cb_{exposure_time}ms.npy"
    path = os.path.join(folder, filename)
    np.save(path, dark_frame_avg)
    print(f"Master dark frame saved at: {path}")

def main():
    # Ensure the output folder exists
    os.makedirs(cubert_dark_frame_folder, exist_ok=True)

    # Setup the Cubert camera
    acquisitionContext = setup_cubert_cam()

    # Capture multiple dark frames
    dark_frames = []
    for i in range(num_dark_frames):
        dark_frame = take_dark_frame(acquisitionContext)
        if dark_frame is not None:
            dark_frames.append(dark_frame)
        time.sleep(0.5)  # Allow some delay between captures

    # Average the dark frames
    if len(dark_frames) > 0:
        dark_frame_avg = np.mean(dark_frames, axis=0)
        save_master_dark(dark_frame_avg, cubert_dark_frame_folder, exposure_time_cb)
    else:
        print("No dark frames captured. Please check the camera setup.")

if __name__ == "__main__":
    main()
