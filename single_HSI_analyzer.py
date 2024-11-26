import matplotlib.pyplot as plt
import numpy as np
import tifffile
import os
from matplotlib.widgets import Slider, Button, RectangleSelector

# Folder path for HSI images
hsi_image_folder = 'images\pol_test\cubert_new'

# List available files in the folder
hsi_files = sorted([f for f in os.listdir(hsi_image_folder) if f.endswith(".tif")])

# Initial setup
current_img_index = 0
current_channel = 0
selected_regions = []
wavelengths = np.linspace(450, 850, 106)  # Assuming 106 channels from 450-850 nm

# Load HSI image
def load_hsi_image(file):
    file_path = os.path.join(hsi_image_folder, file)
    image = tifffile.imread(file_path)
    return image

# Update the plot with the selected image and channel
def update_hsi_plot():
    global ax_hsi, hsi_image, fig, colorbar_hsi
    ax_hsi.clear()

    img = hsi_image[current_channel, :, :]
    im_hsi = ax_hsi.imshow(img, cmap='viridis')
    ax_hsi.set_title(f"HSI Image: {hsi_files[current_img_index]} (Channel {current_channel}, {wavelengths[current_channel]:.1f} nm)")
    ax_hsi.annotate(
        f"Stats:\nSNR: {snr(img):.2f}\nMax: {np.max(img):.2f}\nMin: {np.min(img):.2f}\nAvg: {np.mean(img):.2f}",
        (0.05, 0.9), xycoords='axes fraction', fontsize=10, color='white'
    )

    # Update or create colorbar
    if colorbar_hsi:
        colorbar_hsi.update_normal(im_hsi)
    else:
        colorbar_hsi = plt.colorbar(im_hsi, ax=ax_hsi)

    fig.canvas.draw_idle()

# Callback function for region selection
def onselect(eclick, erelease):
    global selected_regions, ax_spectrum

    # Get rectangle bounds
    x1, y1 = int(eclick.xdata), int(eclick.ydata)
    x2, y2 = int(erelease.xdata), int(erelease.ydata)

    # Ensure coordinates are ordered correctly
    x1, x2 = min(x1, x2), max(x1, x2)
    y1, y2 = min(y1, y2), max(y1, y2)

    # Extract and average the selected region
    selected_area = hsi_image[:, y1:y2+1, x1:x2+1]
    average_spectrum = np.mean(selected_area, axis=(1, 2))
    selected_regions.append(average_spectrum)

    # Update spectrum plot
    ax_spectrum.clear()
    for i, spectrum in enumerate(selected_regions):
        ax_spectrum.plot(wavelengths, spectrum, label=f"Region {i+1}")
    ax_spectrum.set_title("Average Spectrum")
    ax_spectrum.set_xlabel("Wavelength (nm)")
    ax_spectrum.set_ylabel("Intensity")
    ax_spectrum.legend()
    fig.canvas.draw_idle()

# SNR calculation
def snr(img, axis=None, ddof=0):
    m = img.mean(axis)
    sd = img.std(axis=axis, ddof=ddof)
    return np.where(sd == 0, 0, m / sd)

# Button callbacks
def next_image(_):
    global current_img_index, hsi_image
    current_img_index = (current_img_index + 1) % len(hsi_files)
    hsi_image = load_hsi_image(hsi_files[current_img_index])
    update_hsi_plot()

def prev_image(_):
    global current_img_index, hsi_image
    current_img_index = (current_img_index - 1) % len(hsi_files)
    hsi_image = load_hsi_image(hsi_files[current_img_index])
    update_hsi_plot()

def clear_spectra(_):
    global selected_regions, ax_spectrum
    selected_regions = []
    ax_spectrum.clear()
    ax_spectrum.set_title("Average Spectrum")
    ax_spectrum.set_xlabel("Wavelength (nm)")
    ax_spectrum.set_ylabel("Intensity")
    fig.canvas.draw_idle()

# Slider callback
def change_channel(val):
    global current_channel
    current_channel = int(val)
    update_hsi_plot()

# Main function
def main():
    global fig, ax_hsi, ax_spectrum, hsi_image, colorbar_hsi
    colorbar_hsi = None

    # Load initial image
    hsi_image = load_hsi_image(hsi_files[current_img_index])

    # Create plot layout
    fig, (ax_hsi, ax_spectrum) = plt.subplots(1, 2, figsize=(16, 8))
    plt.subplots_adjust(bottom=0.25)

    # Initialize plots
    update_hsi_plot()
    ax_spectrum.set_title("Average Spectrum")
    ax_spectrum.set_xlabel("Wavelength (nm)")
    ax_spectrum.set_ylabel("Intensity")

    # Slider for channel selection
    ax_slider = plt.axes([0.25, 0.15, 0.5, 0.03])
    channel_slider = Slider(ax_slider, "Channel", 0, hsi_image.shape[0] - 1, valinit=current_channel, valstep=1)
    channel_slider.on_changed(change_channel)

    # Buttons for navigation
    ax_next = plt.axes([0.85, 0.05, 0.1, 0.04])
    next_button = Button(ax_next, "Next")
    next_button.on_clicked(next_image)

    ax_prev = plt.axes([0.7, 0.05, 0.1, 0.04])
    prev_button = Button(ax_prev, "Previous")
    prev_button.on_clicked(prev_image)

    # Button to clear spectra
    ax_clear = plt.axes([0.5, 0.05, 0.1, 0.04])
    clear_button = Button(ax_clear, "Clear Spectra")
    clear_button.on_clicked(clear_spectra)

    # Rectangle selector for region selection
    rectangle_selector = RectangleSelector(ax_hsi, onselect, useblit=True, button=[1], interactive=True)

    # Show plot
    plt.show()

if __name__ == "__main__":
    main()
