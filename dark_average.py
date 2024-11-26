import os
import numpy as np
import tifffile

# Paths
calibration_folder = "images/calibration"
output_npy_file = os.path.join(calibration_folder, "masterdark_cb_average.npy")

def average_tiff_files(folder_path):
    # List all .tif files in the folder
    tiff_files = [f for f in os.listdir(folder_path) if f.endswith(".tif")]
    if len(tiff_files) == 0:
        print("No .tif files found in the specified folder.")
        return None

    print(f"Found {len(tiff_files)} .tif files for averaging.")

    # Initialize sum and count
    image_sum = None
    for tiff_file in tiff_files:
        file_path = os.path.join(folder_path, tiff_file)
        print(f"Processing file: {file_path}")
        image = tifffile.imread(file_path)

        # Accumulate images
        if image_sum is None:
            image_sum = image.astype(float)
        else:
            image_sum += image.astype(float)

    # Compute average
    image_average = image_sum / len(tiff_files)
    return image_average

def save_as_npy(array, output_path):
    np.save(output_path, array)
    print(f"Average image saved as .npy file at: {output_path}")

def main():
    # Average the .tif files
    average_image = average_tiff_files(calibration_folder)
    if average_image is not None:
        # Save the averaged image as a .npy file
        save_as_npy(average_image, output_npy_file)

if __name__ == "__main__":
    main()
