import matplotlib.pyplot as plt
import numpy as np
import tifffile
import os

# Folder path for images
img_folder = 'images\\pol_test\\cubert'

# File names to load and display
file_names = [
    "no_polarizer.tif", 
    "0_degrees.tif", 
    "45_degrees.tif", 
    "90_degrees.tif", 
]

# Load images into a list
images = [tifffile.imread(os.path.join(img_folder, f)) for f in file_names]

# Define wavelengths and indices of interest
wavelengths = np.linspace(450, 850, images[0].shape[0])  # Assuming 106 bands
selected_wavelengths = [0, 25, 50, 75]  # Indices of selected wavelengths
selected_labels = [f"{wavelengths[idx]:.0f} nm" for idx in selected_wavelengths]

# Gain factor for brightness adjustment
gain = 2.0

# Function to apply gain and clip values
def apply_gain(image, gain):
    return np.clip(image * gain, 0, 255)  # Clip to valid range for display

# Create the plot with an extra column for row titles
fig, axs = plt.subplots(
    len(images), 
    len(selected_wavelengths) + 1, 
    figsize=(14, 10), 
    gridspec_kw={"width_ratios": [0.5] + [1] * len(selected_wavelengths)}  # Shrink the first column
)
fig.suptitle("HSI Visualization Across Wavelengths", fontsize=16)

for row, (img, name) in enumerate(zip(images, file_names)):
    # Add the label in the first column
    axs[row, 0].text(0.5, 0.5, name.replace('.tif', ''), fontsize=12, ha='center', va='center')
    axs[row, 0].axis('off')  # Hide axes for label cells

    for col, wl_idx in enumerate(selected_wavelengths):
        adjusted_img = apply_gain(img[wl_idx], gain)  # Apply gain to the image
        axs[row, col + 1].imshow(adjusted_img, cmap='viridis')
        axs[row, col + 1].axis('off')
        if row == 0:  # Add wavelength labels to the top row
            axs[row, col + 1].set_title(selected_labels[col], fontsize=12)

# Turn off the first column axes for the top row
for ax in axs[:, 0]:
    ax.axis('off')

plt.tight_layout(rect=[0, 0, 1, 0.95])  # Adjust layout to accommodate titles
plt.show()
