import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from skimage import io
import tifffile
from matplotlib.widgets import RectangleSelector, Slider, TextBox

image_path = 'images\\thorlabs\\10_thorlabs.tif'

image = tifffile.imread(image_path)
fig, ax = plt.subplots()
ax.imshow(image, cmap='viridis')
ax.set_title("SNR Calculator")
plt.show()

# Callback function for region selection
def onselect(eclick, erelease):
    global selected_regions, cb_image

    # Get the coordinates of the rectangle
    x1, y1 = int(eclick.xdata), int(eclick.ydata)
    x2, y2 = int(erelease.xdata), int(erelease.ydata)

    # Ensure coordinates are in the correct order
    if x1 > x2:
        x1, x2 = x2, x1
    if y1 > y2:
        y1, y2 = y2, y1

    # Extract the the selected area
    selected_area = image[y1:y2+1, x1:x2+1, :]

    mean = np.mean(selected_area)
    stddev = np.std(selected_area)
    SNR = mean/stddev

    ax.text(
        0.95,0.95,
        f'SNR: {SNR:.1f}'
    )

    # Redraw the figure
    fig.canvas.draw_idle()

rectangle_selector = RectangleSelector(
    ax,
    onselect,
    useblit=True,
    button=[1],  # Left mouse button
    minspanx=5, minspany=5,
    spancoords='pixels',
    interactive=True
)

