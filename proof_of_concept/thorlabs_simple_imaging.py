import pylablib as pll
#pll.par['devices/dlls/thorlabs_tlcam'] = 'thorlabs_dlls/'

from pylablib.devices import Thorlabs as tl
import numpy as np
import matplotlib.pyplot as plt

tl.list_cameras_tlcam()
cam = tl.ThorlabsTLCamera()

cam.set_exposure(50e-3)
cam.set_roi(0, 640, 0, 640, hbin=1, vbin=1)
frame = cam.snap()

print("shape:", frame.shape)

plt.imshow(frame)
plt.colorbar()
plt.title("frame")
np.save('thorlabs_img/frame.npy', frame)
