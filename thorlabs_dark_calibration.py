import pylablib as pll

from pylablib.devices import Thorlabs as tl
import numpy as np
import matplotlib.pyplot as plt

def do_dark_calibration(exp_time = 1000, n_frames = 25, roi_tl = (0, 2448, 0, 2048)):
    print("REMEMBER TO PUT THE CAP ON.")

    # connecting cam
    tl.list_cameras_tlcam()
    cam = tl.ThorlabsTLCamera()

    # doing exposures
    cam.set_exposure(exp_time*1e-3)
    cam.set_roi(*roi_tl, hbin=1, vbin=1)
    frames = cam.grab(nframes=n_frames)

    # averaging
    avg = np.average(frames, axis = 0)
    print("Shape of Master Dark:", avg.shape)
    print("Max of Master Dark:", np.max(avg))
    print("Min of Master Dark:", np.min(avg))
    print("Std of Master Dark:", np.std(avg))

    # saving
    np.save(f'images/calibration/thorlabs_dark/masterdark_tl_{exp_time}ms.npy', avg)


if __name__ == "__main__":
    do_dark_calibration()
