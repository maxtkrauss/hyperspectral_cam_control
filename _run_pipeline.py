import cubert_dark_calibration as calib_cb
import thorlabs_dark_calibration as calib_tl
import create_dataset_display as create
import paired_img_viewer_v3 as view

# Parameter
exp_tl = 2000
exp_cb = 500
n_frames = 10
dist_cb = 690
dataset_path = "images\\display\\dataset"

# Calibration Routines
#calib_tl.do_dark_calibration(exp_time=exp_tl, n_frames=n_frames)
#calib_cb.do_dark_calibration(exp_time=exp_cb, n_frames=n_frames, dist=dist_cb)

# Wait for removal of Lens caps
#input("Remove lens caps and press Enter.")

# Run Dataset Creation
create.exposure_time_tl = exp_tl
create.exposure_time_cb = exp_cb
create.display_image_folder = dataset_path
create.main()

# Open Paired Image Viewer
view.main()