import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from skimage import io
import tifffile
from matplotlib.widgets import RectangleSelector

# Load the image
image_path = 'images\\thorlabs\\10_thorlabs_demos.tif'
tif = tifffile.imread(image_path)
image = tif[:, :, :]
print(f"Shape of tiff after demosaicing:{image.shape}")

image = tif[3, :, :]


# Create the plot
fig, ax = plt.subplots()
img = ax.imshow(image, cmap='viridis')
fig.colorbar(img, ax = ax)
ax.set_title("SNR Calculator")

# Callback function for region selection
def onselect(eclick, erelease):
    # Get the coordinates of the rectangle
    x1, y1 = int(eclick.xdata), int(eclick.ydata)
    x2, y2 = int(erelease.xdata), int(erelease.ydata)

    # Ensure coordinates are in the correct order
    if x1 > x2:
        x1, x2 = x2, x1
    if y1 > y2:
        y1, y2 = y2, y1

    # Extract the selected area
    selected_area = image[y1:y2+1, x1:x2+1]

    # Calculate mean and standard deviation for SNR
    snr = SNR(selected_area)

    # Display the SNR value on the plot
    ax.text(
        0.95, 0.95,
        f'SNR: {snr}',
        transform=ax.transAxes,
        fontsize=12,
        verticalalignment='top',
        horizontalalignment='right',
        bbox=dict(facecolor='white', alpha=0.5)
    )

    # Redraw the figure
    fig.canvas.draw_idle()

# Rectangle selector for selecting region of interest
rectangle_selector = RectangleSelector(
    ax,
    onselect,
    useblit=True,
    button=[1],  # Left mouse button
    minspanx=5, minspany=5,
    spancoords='pixels',
    interactive=True
)

def SNR(img, axis=None, ddof=0):
    img = np.asanyarray(img)
    mean_value = img.mean(axis)
    stddev_value = img.std(axis=axis, ddof=ddof)
    snr = np.where(stddev_value == 0, 0, mean_value / stddev_value)

    
    print(f"Mean: {mean_value}, Standard Deviation: {stddev_value}, SNR: {snr}")
    
    return snr

plt.show()
