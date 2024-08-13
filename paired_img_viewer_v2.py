import matplotlib.pyplot as plt
import numpy as np
import tifffile
import os
from matplotlib.widgets import RectangleSelector, Slider, TextBox

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

# List to keep track of multiple selected regions
selected_regions = []

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
    global cb_image  # Make sure cb_image is accessible in the callback

    tl_image, cb_image = load_images(tl_file, cb_file)

    # Clear the current plot
    ax_tl.clear()
    ax_cb.clear()

    # Plot Thorlabs image
    im_tl = ax_tl.imshow(tl_image, cmap='viridis')
    ax_tl.set_title(f"Thorlabs Image: {tl_file}")

    # Plot selected channel of Cubert image
    im_cb = ax_cb.imshow(cb_image[:, :, channel], cmap='viridis')
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

def get_color_from_wavelength(wavelength):
    if 380 <= wavelength < 450:
        return "Violet"
    elif 450 <= wavelength < 500:
        return "Blue"
    elif 500 <= wavelength < 570:
        return "Green"
    elif 570 <= wavelength < 590:
        return "Yellow"
    elif 590 <= wavelength < 620:
        return "Orange"
    elif 620 <= wavelength <= 750:
        return "Red"
    else:
        return "Out of Visible Range"

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

    # Extract the reflectance values for the selected area
    selected_area = cb_image[y1:y2+1, x1:x2+1, :]

    # Calculate the average reflectance values for the selected area
    reflectance_values = np.mean(selected_area, axis=(0, 1))

    # Store the normalized reflectance values and color for this selection
    selected_regions.append(reflectance_values)

    # Plot all selected spectra
    ax_intensity.clear()
    for i, spectrum in enumerate(selected_regions):
        ax_intensity.plot(wavelengths, spectrum, label=f'Selection {i+1}')

        # Find the peak wavelength for the first selection
        if i == 0:
            peak_index = np.argmax(spectrum)
            peak_wavelength = wavelengths[peak_index]
            color = get_color_from_wavelength(peak_wavelength)
            
            # Write peak wavelength in the top-right corner of the plot
            ax_intensity.text(
                0.95, 0.95,  # x, y position in axes coordinates (0.95, 0.95) corresponds to the top-right corner
                f'Peak: {peak_wavelength:.1f} nm\nColor: {color}',
                transform=ax_intensity.transAxes,  # Use axes coordinates for positioning
                fontsize=10,
                verticalalignment='top',
                horizontalalignment='right',
                color='red'
            )

    ax_intensity.set_xlabel("Wavelength (nm)")
    ax_intensity.set_ylabel("Intensity")
    ax_intensity.set_title("Spectrum for Selected Areas")
    ax_intensity.legend()

    # Redraw the figure
    fig.canvas.draw_idle()

# Create the plot
fig, (ax_tl, ax_cb, ax_intensity) = plt.subplots(1, 3, figsize=(18, 6))
plt.subplots_adjust(left=0.05, right=0.95, top=0.85, bottom=0.3, wspace=0.4)

# Set window title
fig.suptitle('Paired Image Viewer')

# Initial plot
tl_image, cb_image = load_images(current_tl_file, current_cb_file)
update_plot(current_tl_file, current_cb_file, current_channel)

# Sliders and textboxes for selecting images and channel
ax_tl_textbox = plt.axes([0.05, 0.1, 0.3, 0.05])  # Adjusted position and size
tl_textbox = TextBox(ax_tl_textbox, 'Thorlabs File', initial=current_tl_file)
tl_textbox.on_submit(change_thorlabs_file)

ax_cb_textbox = plt.axes([0.6, 0.1, 0.3, 0.05])  # Adjusted position and size
cb_textbox = TextBox(ax_cb_textbox, 'Cubert File', initial=current_cb_file)
cb_textbox.on_submit(change_cubert_file)

ax_channel_slider = plt.axes([0.25, 0.05, 0.65, 0.03])
channel_slider = Slider(
    ax=ax_channel_slider,
    label='Cubert Channel',
    valmin=0,
    valmax=cb_image.shape[2] - 1,
    valinit=current_channel,
    valstep=1
)
channel_slider.on_changed(change_channel)

# RectangleSelector for selecting region on the Cubert image
rectangle_selector = RectangleSelector(
    ax_cb,
    onselect,
    useblit=True,
    button=[1],  # Left mouse button
    minspanx=5, minspany=5,
    spancoords='pixels',
    interactive=True
)

# Display the plot
plt.show()
