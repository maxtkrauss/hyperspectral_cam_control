import matplotlib.pyplot as plt
import numpy as np
import tifffile
from matplotlib.widgets import Slider, Button, TextBox
import os

# Folder paths for images
thorlabs_image_folder = 'images/thorlabs'
cubert_image_folder = 'images/cubert'

# List available files in each folder
thorlabs_files = [f for f in os.listdir(thorlabs_image_folder) if f.endswith(".tif")]
cubert_files = [f for f in os.listdir(cubert_image_folder) if f.endswith(".tif")]

# Initial selections
current_tl_file = thorlabs_files[0]
current_cb_file = cubert_files[0]
current_channel = 0
wavelengths = np.linspace(450, 850, 106)  # Assuming 106 channels from 450-850 nm

# Load images
def load_images(tl_file, cb_file):
    tl_image_path = os.path.join(thorlabs_image_folder, tl_file)
    cb_image_path = os.path.join(cubert_image_folder, cb_file)

    # Load Thorlabs image
    tl_image = tifffile.imread(tl_image_path)

    # Load Cubert image
    cb_image = tifffile.imread(cb_image_path)

    return tl_image, cb_image

# Update the plot with the selected images and channel
def update_plot(tl_file, cb_file, channel):
    tl_image, cb_image = load_images(tl_file, cb_file)

    # Clear the current plot
    ax_tl.clear()
    ax_cb.clear()

    # Plot Thorlabs image
    ax_tl.imshow(tl_image, cmap='viridis')
    ax_tl.set_title(f"Thorlabs Image: {tl_file}")

    # Plot selected channel of Cubert image
    ax_cb.imshow(cb_image[:, :, channel], cmap='viridis')
    wavelength = wavelengths[channel]
    ax_cb.set_title(f"Cubert Image: {cb_file} (Channel {channel + 1}/{cb_image.shape[2]}, {wavelength:.1f} nm)")

    # Redraw the figure
    fig.canvas.draw_idle()

# Change the Thorlabs file
def change_thorlabs_file(text):
    global current_tl_file
    if text in thorlabs_files:
        current_tl_file = text
        update_plot(current_tl_file, current_cb_file, current_channel)
    else:
        print(f"File '{text}' not found in Thorlabs folder.")

# Change the Cubert file
def change_cubert_file(text):
    global current_cb_file
    if text in cubert_files:
        current_cb_file = text
        update_plot(current_tl_file, current_cb_file, current_channel)
        channel_slider.valmax = load_images(current_tl_file, current_cb_file)[1].shape[2] - 1
        channel_slider.set_val(current_channel)  # Update channel slider to new file's channel count
    else:
        print(f"File '{text}' not found in Cubert folder.")

# Change the channel
def change_channel(val):
    global current_channel
    current_channel = int(val)
    update_plot(current_tl_file, current_cb_file, current_channel)

# Create the plot
fig, (ax_tl, ax_cb) = plt.subplots(1, 2, figsize=(10, 5))
plt.subplots_adjust(bottom=0.3)

# Initial plot
update_plot(current_tl_file, current_cb_file, current_channel)

# Sliders and textboxes for selecting images and channel
ax_tl_textbox = plt.axes([0.1, 0.2, 0.3, 0.05])
tl_textbox = TextBox(ax_tl_textbox, 'Thorlabs File', initial=current_tl_file)
tl_textbox.on_submit(change_thorlabs_file)

ax_cb_textbox = plt.axes([0.6, 0.2, 0.3, 0.05])
cb_textbox = TextBox(ax_cb_textbox, 'Cubert File', initial=current_cb_file)
cb_textbox.on_submit(change_cubert_file)

ax_channel_slider = plt.axes([0.25, 0.1, 0.65, 0.03])
channel_slider = Slider(
    ax=ax_channel_slider,
    label='Cubert Channel',
    valmin=0,
    valmax=load_images(current_tl_file, current_cb_file)[1].shape[2] - 1,
    valinit=current_channel,
    valstep=1
)
channel_slider.on_changed(change_channel)

# Display the plot
plt.show()
