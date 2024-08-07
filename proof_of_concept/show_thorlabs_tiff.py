from tifffile import tifffile
import matplotlib.pyplot as plt
import numpy as np

frame = tifffile.imread('images\\thorlabs\\1_thorlabs.tif')

avg = np.average(frame)
std = np.std(frame)
print("shape:", frame.shape, "min:", np.min(frame), "max:", np.max(frame), "std:", std, "avg:", avg)

plt.figure(figsize=(10,7))
plt.imshow(frame)#, vmin=avg-std, vmax=avg+std) # to better view dark frames
plt.colorbar()
plt.title("frame")
plt.show()