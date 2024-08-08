import cuvis
import numpy as np
import tifffile


def get_tiff_shape(file_path):
    try:
        with tifffile.TiffFile(file_path) as tif:
            # Get the first page of the TIFF file
            page = tif.pages[0]
            # Get the shape of the image
            shape = page.asarray().shape
            print(f"The shape of the TIFF file is: {shape}")
            return page.asarray()
    except Exception as e:
        print(f"Error: Failed to load TIFF file: {e}")

def get_npy_shape(file_path):
    try:
        data = np.load(file_path)
        shape = data.shape
        print(f"The size of the .npy file is: {shape}")
        return data
    except Exception as e:
        print(f"Error: Failed to load .npy file: {e}")
    

def subtract_and_save_tiff(tiff_data, npy_data, output_path):
    try:
        # Subtract npy_data from tiff_data
        result_data = tiff_data - npy_data
        # Ensure no negative values, set them to zero
        result_data = np.maximum(result_data, 0)
        print(f"The shape of the resulting TIFF file is: {result_data.shape}")
        # Save the result as a new TIFF file
        tifffile.imwrite(output_path, result_data,  photometric='minisblack')
        print(f"Subtracted image saved to {output_path}")
    except Exception as e:
        print(f"Error: Failed to save TIFF file: {e}")

        # Function to read and check the shape of the saved TIFF file
def check_tiff_shape(file_path):
    try:
        with tifffile.TiffFile(file_path) as tif:
            data = tif.asarray()
            shape = data.shape
            print(f"The shape of the saved TIFF file is: {shape}")
            return data
    except Exception as e:
        print(f"Error: Failed to load saved TIFF file: {e}")
        return None

tiff_file_path = "proof_of_concept\\images_cubert\\dark_test_2.tiff"
npy_file_path = "images\\calibration\\cubert_dark\\masterdark_cb_250ms.npy"
output_tiff_path = "proof_of_concept\\images_cubert\\dark_test_2_ds.tiff"

tiff_data = get_tiff_shape(tiff_file_path)
npy_data = get_npy_shape(npy_file_path)

subtract_and_save_tiff(tiff_data, npy_data, output_tiff_path)

# Check the shape of the saved TIFF file
saved_tiff_data = check_tiff_shape(output_tiff_path)

# Print some data points to verify content (optional)
if saved_tiff_data is not None:
    print(f"Sample data points from the saved TIFF file: {saved_tiff_data[0, 0, :5]}")





# # Load the .cu3s file
# file_path = "images\\calibration\cubert_dark\\Auto_001.cu3s"
# measurement = cuvis.SessionFile(file_path)[0]

# # Convert the ImageData object to numpy arrays
# data = measurement.data['cube']
# data_array = np.array(data.array)

# # Print the shape of the cube data and wavelengths
# print("Data shape:", data_array.shape)
# print("Averaged data: ", data_array[0, 0, :])