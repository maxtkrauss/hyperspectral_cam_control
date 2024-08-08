import tifffile
import matplotlib.pyplot as plt
from matplotlib.widgets import RectangleSelector
import numpy as np

# List to keep track of multiple selected regions
selected_regions = []

# wavelengths
lambdas = np.linspace(450,850,106)

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
            img = page.asarray()[:, :, 53]
            fig, ax = plt.subplots(figsize = (10,7))
            cax = ax.imshow(img, cmap='gray')
            cbar = fig.colorbar(cax, ax=ax)
            plt.title(f"Frame: {file_path}")
            cbar.set_label('Intensity', rotation=270, labelpad=15)

            # Create RectangleSelector
            toggle_selector.RS = RectangleSelector(ax, onselect, useblit=True,
                                                   button=[1], minspanx=5, minspany=5, spancoords='pixels',
                                                   interactive=True)
            plt.connect('key_press_event', toggle_selector)

            # Store the image data for further use
            ax.image_data = tif.asarray()

            plt.show()
    except Exception as e:
        print(f"Error: Failed to load TIFF file: {e}")

def onselect(eclick, erelease):
    # Get the coordinates of the rectangle
    x1, y1 = int(eclick.xdata), int(eclick.ydata)
    x2, y2 = int(erelease.xdata), int(erelease.ydata)

    # Ensure coordinates are in the correct order
    if x1 > x2:
        x1, x2 = x2, x1
    if y1 > y2:
        y1, y2 = y2, y1

    # Extract the reflectance values for the selected area
    img = plt.gca().image_data
    selected_area = img[y1:y2+1, x1:x2+1, :]

    # Calculate the average reflectance values for the selected area
    reflectance_values = np.mean(selected_area, axis=(0, 1))

    # Store the normalized reflectance values and color for this selection
    selected_regions.append(reflectance_values)

    # Plot all selected spectra
    plt.figure()
    for i, spectrum in enumerate(selected_regions):
        plt.plot(lambdas, spectrum, label=f'Selection {i+1}')
    plt.xlabel("Wavelength (nm)")
    plt.ylabel("Intensity")
    plt.title("Spectrum for Selected Areas")
    plt.legend()
    plt.show()

def toggle_selector(event):
    print('Key pressed.')
    if event.key in ['Q', 'q'] and toggle_selector.RS.active:
        print('RectangleSelector deactivated.')
        toggle_selector.RS.set_active(False)
    if event.key in ['A', 'a'] and not toggle_selector.RS.active:
        print('RectangleSelector activated.')
        toggle_selector.RS.set_active(True)

if __name__ == "__main__":
    file_path = "images\\cubert\\3_cubert.tif"
    get_tiff_shape(file_path) 
    display_first_channel(file_path)
