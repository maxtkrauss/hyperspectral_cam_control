import pylablib as pll
#pll.par['devices/dlls/thorlabs_tlcam'] = 'thorlabs_dlls/'

from pylablib.devices import Thorlabs as tl
import numpy as np
import matplotlib.pyplot as plt

tl.list_cameras_tlcam()
cam = tl.ThorlabsTLCamera()

cam.set_exposure(100e-3)
cam.set_roi(0, 2448, 0, 2408, hbin=1, vbin=1)
frame = cam.snap()

avg = np.average(frame)
std = np.std(frame)
print("shape:", frame.shape, "min:", np.min(frame), "max:", np.max(frame), "std:", std, "avg:", avg)

plt.imshow(frame, vmin=avg-std, vmax=avg+std) # to better view dark frames
plt.colorbar()
plt.title("frame")
plt.show()