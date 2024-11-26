import numpy as np
import matplotlib.pyplot as plt
import tifffile as tiff
import os

def plot_polarizations(tif_images, polarizations=["0°", "45°", "90°", "135°"], scale_factor=0.1):
    """
    Args:
        tif_images: List of file paths to .tif images.
        polarizations: List of polarization labels.
        scale_factor: Factor to downscale the images for display.
    """
    n_rows = len(tif_images)  # Each row corresponds to a new image
    n_cols = len(polarizations)  # Each column corresponds to a polarization

    fig, axes = plt.subplots(n_rows, n_cols, figsize=(15, 5 * n_rows))
    if n_rows == 1:
        axes = np.expand_dims(axes, axis=0)  # Ensure 2D array of axes for single row

    for row_idx, tif_path in enumerate(tif_images):
        # Extract the title from the filename
        image_title = os.path.basename(tif_path)

        # Open the .tif image
        image = tiff.imread(tif_path)  # Shape: (5, 2048, 2448)

        # Downscale images for display
        downscaled_images = [
            image[channel, ::int(1/scale_factor), ::int(1/scale_factor)]
            for channel in range(len(polarizations))
        ]

        # Add row title above the row
        fig.text(0.5, 1 - (row_idx + 0.5) / n_rows, image_title, ha='center', va='center', fontsize=14)

        # Plot each polarization
        for col_idx, downscaled_image in enumerate(downscaled_images):
            ax = axes[row_idx, col_idx]
            ax.imshow(downscaled_image, cmap='gray')
            ax.axis('off')
            ax.set_title(f"Polarization {polarizations[col_idx]}", fontsize=10)

    plt.tight_layout()
    plt.subplots_adjust(top=0.9)  # Adjust the top margin for row titles
    plt.show()

tif_images = ["images\\pol_check\\3__thorlabs.tif", "images\\pol_check\\12_thorlabs.tif", "images\\pol_check\\130_thorlabs.tif", "images\\pol_check\\430_thorlabs.tif"]  # Replace with actual paths
plot_polarizations(tif_images)
