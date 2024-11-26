import os
import numpy as np
import tifffile
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button

# Folder containing the multichannel TIFF files
folder_path = "images\pol_test\cubert"

# List of polarization angles and corresponding files
polarizer_files = {
    "0°": "0_degrees.tif",
    "45°": "45_degrees.tif",
    "90°": "90_degrees.tif",
    "135°": "135_degrees.tif",
    "No Polarizer": "no_polarizer.tif"
}

# Load all TIFF files into a dictionary
def load_tiff_files(folder, file_dict):
    data = {}
    for angle, filename in file_dict.items():
        file_path = os.path.join(folder, filename)
        if os.path.exists(file_path):
            print(f"Loading {angle} polarizer file: {filename}")
            data[angle] = tifffile.imread(file_path)
        else:
            print(f"File not found: {filename}")
    return data

# Calculate SNR
def snr(img):
    mean = np.mean(img)
    std_dev = np.std(img)
    return mean / std_dev if std_dev > 0 else 0

# Update plots based on selected channel
def update_plot(channel):
    ax_img.clear()
    ax_metrics.clear()

    # Display the selected channel for all polarizer angles
    for angle, img_stack in data.items():
        img = img_stack[channel]
        intensity = np.mean(img)
        ax_metrics.bar(angle, intensity, label=f"{angle} (Mean Intensity: {intensity:.2f})")

        if angle == current_angle:
            ax_img.imshow(img, cmap="viridis")
            ax_img.set_title(f"Channel {channel} | {angle}")

    ax_metrics.set_title("Mean Intensity Across Polarizers")
    ax_metrics.set_ylabel("Intensity")
    ax_metrics.set_xlabel("Polarizer Angle")
    ax_metrics.legend()

    fig.canvas.draw_idle()

# Move to the next channel
def next_channel(event):
    global current_channel
    current_channel = (current_channel + 1) % num_channels
    update_plot(current_channel)

# Move to the previous channel
def prev_channel(event):
    global current_channel
    current_channel = (current_channel - 1) % num_channels
    update_plot(current_channel)

# Initialize data and global variables
data = load_tiff_files(folder_path, polarizer_files)
num_channels = list(data.values())[0].shape[0] if data else 0
current_channel = 0
current_angle = "0°"

# Create the plot layout
fig, (ax_img, ax_metrics) = plt.subplots(1, 2, figsize=(12, 6))
plt.subplots_adjust(bottom=0.2)

# Initial plot
update_plot(current_channel)

# Channel slider
ax_slider = plt.axes([0.25, 0.05, 0.5, 0.03])
channel_slider = Slider(ax_slider, "Channel", 0, num_channels - 1, valinit=current_channel, valstep=1)
channel_slider.on_changed(lambda val: update_plot(int(val)))

# Next/Previous channel buttons
ax_next = plt.axes([0.85, 0.1, 0.1, 0.04])
btn_next = Button(ax_next, "Next Channel")
btn_next.on_clicked(next_channel)

ax_prev = plt.axes([0.05, 0.1, 0.1, 0.04])
btn_prev = Button(ax_prev, "Previous Channel")
btn_prev.on_clicked(prev_channel)

# Display the plot
plt.show()
