import tifffile
import matplotlib.pyplot as plt

def get_tiff_shape(file_path):
    try:
        with tifffile.TiffFile(file_path) as tif:
            # Get the first page of the TIFF file
            page = tif.pages[0]
            # Get the shape of the image
            shape = page.shape
            print(f"The shape of the TIFF file is: {shape}")
    except Exception as e:
        print(f"Error: Failed to load TIFF file: {e}")

def display_first_channel(file_path):
    try:
        with tifffile.TiffFile(file_path) as tif:
            # Load the first page
            page = tif.pages[0]
            # Display the first channel
            plt.imshow(page.asarray()[:, :, 0], cmap='viridis')
            plt.title("First Channel")
            plt.colorbar()
            plt.show()
    except Exception as e:
        print(f"Error: Failed to load TIFF file: {e}")

if __name__ == "__main__":
    file_path = input("Enter the path to the TIFF file: ").strip()
    get_tiff_shape(file_path)
    display_first_channel(file_path)
    
