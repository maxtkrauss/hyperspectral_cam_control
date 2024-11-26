import tifffile as tiff

file1 = 'images//scenes//cubert//20241114_110703_cubert.tif'
file2 = 'images//scenes//thorlabs//20241114_110703_thorlabs.tif'

# Load images
cubert_image = tiff.imread(file1)
tl_image = tiff.imread(file2)

# Define center points
cubert_center_x, cubert_center_y = 157, 179  # Adjust based on your center
tl_center_x, tl_center_y = 1389, 933         # Adjust based on your center

# Define crop dimensions
cubert_crop_size = 120
tl_crop_size = 660

# Crop around center for Cubert using array slicing
cubert_left = cubert_center_x - cubert_crop_size // 2
cubert_upper = cubert_center_y - cubert_crop_size // 2
cubert_right = cubert_center_x + cubert_crop_size // 2
cubert_lower = cubert_center_y + cubert_crop_size // 2
cubert_cropped = cubert_image[:, cubert_upper:cubert_lower, cubert_left:cubert_right]

# Crop around center for TL using array slicing
tl_left = tl_center_x - tl_crop_size // 2
tl_upper = tl_center_y - tl_crop_size // 2
tl_right = tl_center_x + tl_crop_size // 2
tl_lower = tl_center_y + tl_crop_size // 2
tl_cropped = tl_image[:, tl_upper:tl_lower, tl_left:tl_right]

# Save the cropped images
tiff.imwrite("cubert_cropped_120x120.tiff", cubert_cropped)
tiff.imwrite("tl_cropped_660x660.tiff", tl_cropped)
