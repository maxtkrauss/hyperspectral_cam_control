import cubert_dark_calibration as calib_cb
import thorlabs_dark_calibration as calib_tl
import create_dataset_display as create
# import paired_img_viewer_v3 as view
import os

# Parameter
exp_tl = 200
exp_cb = 500
n_frames = 10
dist_cb = 800
dataset_path = "images\\display\\dataset"
save_path = "B:\\nasa_hsi_dataset\\frosted_plastic_2024-09-10_4"
try:
    os.mkdir(save_path)
    os.mkdir(os.path.join(save_path, 'thorlabs'))
    os.mkdir(os.path.join(save_path, 'cubert'))
except:
    pass

# Calibration Routines
#calib_tl.do_dark_calibration(exp_time=exp_tl, n_frames=n_frames)
#calib_cb.do_dark_calibration(exp_time=exp_cb, n_frames=n_frames, dist=dist_cb)

# Wait for removal of Lens caps
#input("Remove lens caps and press Enter.")

# Run Dataset Creation
create.exposure_time_tl = exp_tl
create.exposure_time_cb = exp_cb
create.distance_cb = dist_cb
create.display_image_folder = dataset_path
create.thorlabs_image_folder = os.path.join(save_path, 'thorlabs')
create.cubert_image_folder = os.path.join(save_path, 'cubert')
create.main()

# Open Paired Image Viewer
#view.main()