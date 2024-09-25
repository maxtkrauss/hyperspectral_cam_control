from PIL import Image
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import pearsonr

# Define the directory containing the TIFF files
directory = os.path.join('testing', 'psf1')

# Load the dark PSF image
dark_image_path = os.path.join(directory, "dark_psf.tiff")
dark_image = np.array(Image.open(dark_image_path), dtype=np.float32)

# Initialize lists to hold image data and filenames
image_data = []
image_names = []

# Load and subtract the dark image from each PSF image
for wavelength in range(440, 861, 30):
    filename = f"{wavelength}nm_psf.tiff"
    image_path = os.path.join(directory, filename)
    
    if os.path.exists(image_path):
        image = np.array(Image.open(image_path), dtype=np.float32)
        # Dark subtraction
        subtracted_image = image - dark_image
        image_data.append(subtracted_image)
        image_names.append(wavelength)
    else:
        print(f"File not found: {filename}")

# Compute Pearson correlation between each pair of images
num_images = len(image_data)
correlation_matrix = np.zeros((num_images, num_images))

for i in range(num_images):
    for j in range(num_images):
        # Flatten the images to 1D arrays for correlation calculation
        img1 = image_data[i].flatten()
        img2 = image_data[j].flatten()
        # Compute Pearson correlation
        corr, _ = pearsonr(img1, img2)
        correlation_matrix[i, j] = corr

# Plot and save the correlation matrix as a PNG
plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, xticklabels=image_names, yticklabels=image_names, cmap='viridis', annot=True)
plt.title("Pearson Cross-Correlation of NASA DFA1")
plt.xlabel("Wavelengths")
plt.ylabel("Wavelengths")
plt.tight_layout()
output_path = os.path.join(directory, "pearson_correlation_matrix.png")
plt.savefig(output_path)
plt.close()

print(f"Pearson correlation matrix saved as {output_path}")
