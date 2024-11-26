import tifffile as tiff
import matplotlib.pyplot as plt

def select_crop_region(image):
    """
    Allows user to interactively select a square region for cropping on an image.

    Parameters:
    image (numpy.ndarray): The input image to crop (2D array).

    Returns:
    tuple: Crop coordinates ((col_start, col_end), (row_start, row_end)).
    """
    fig, ax = plt.subplots()
    ax.imshow(image, cmap='gray')
    plt.title('Select two points (top-left and bottom-right corners)')

    points = []

    # Function to record clicks
    def onclick(event):
        if len(points) < 2:  # Store only two points
            points.append((int(event.xdata), int(event.ydata)))
            ax.plot(event.xdata, event.ydata, 'ro')
            plt.draw()
        if len(points) == 2:  # Close plot after second point
            plt.close()

    # Connect the event to the plot
    cid = fig.canvas.mpl_connect('button_press_event', onclick)
    plt.show()

    # Ensure two points are recorded
    if len(points) < 2:
        print("Please select exactly two points (top-left and bottom-right corners).")
        return None

    # Sort points to find the top-left and bottom-right corners
    col_start, col_end = sorted([points[0][0], points[1][0]])
    row_start, row_end = sorted([points[0][1], points[1][1]])

    # Return coordinates in the format ((col_start, col_end), (row_start, row_end))
    return ((col_start, col_end), (row_start, row_end))

file1 = 'images//scenes//cubert//20241114_110703_cubert.tif'
file2 = 'images//scenes//thorlabs//20241114_110703_thorlabs.tif'

# file1 = 'cubert_cropped_120x120.tiff'
# file2 = 'tl_cropped_660x660.tiff'

tiff1 = tiff.imread(file1)
tiff2 = tiff.imread(file2)

print(f'TIFF 1 shape: {tiff1.shape}')
print(f'TIFF 2 shape: {tiff2.shape}')

channel1 = tiff1[25]
channel2 = tiff2[2]

# Cropping Manual
#crop_tl = ((1200-350-100, 1200+350+100), (400-100, 1100+100)) #((550-50, 1350+50), (850-50, 1650+50))
#crop_cb = ((10, 150), (150-17, 250-13)) #((188+3, 234-1), (64+3, 110-1))

# Cropping Auto
crop_cb = select_crop_region(channel1)
crop_tl = select_crop_region(channel2)

print("Crop CB Region")
print(crop_cb)

print("Crop TL Region")
print(crop_tl)

# crop_tl = ((610, 1610), (291, 1291))  # Crop size: (1291 - 291, 1610 - 610) = (1000, 1000)

# crop_cb = ((2, 122), (128, 248))  # Crop size: (248 - 128, 122 - 2) = (120, 120)

img_cb = channel1[crop_cb[1][0]:crop_cb[1][1], crop_cb[0][0]:crop_cb[0][1]]
img_tl = channel2[crop_tl[1][0]:crop_tl[1][1], crop_tl[0][0]:crop_tl[0][1]]

print(f'Cubert Shape: {tiff1.shape}')
print(f'TL Shape: {tiff2.shape}')

print(f'Cubert Cropped Shape: {img_cb.shape}')
print(f'TL Cropped Shape: {img_tl.shape}')

# Visual Verification
fig, axs = plt.subplots(2, 2, figsize=(10, 5))

axs[0,0].imshow(channel1, cmap='gray')
axs[0,0].set_title('Cubert')
axs[0,0].axis('off')

axs[0,1].imshow(channel2, cmap='gray')
axs[0,1].set_title('TL')
axs[0,1].axis('off')

axs[1,0].imshow(img_cb, cmap='gray')
axs[1,0].set_title('Cropped Cubert')
axs[1,0].axis('off')

axs[1,1].imshow(img_tl, cmap='gray')
axs[1,1].set_title('Cropped TL')
axs[1,1].axis('off')

plt.show()



