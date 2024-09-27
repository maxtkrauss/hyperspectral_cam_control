import numpy as np
import tifffile
import os

import matplotlib.pyplot as plt

TRAIN_DIR_X = "images/thorlabs"
TRAIN_DIR_Y = "images/cubert"

crop_x = ((750-400, 1650+400), (300-400, 1200+400))
crop_y = ((50-11, 150-7), (150-17, 250-13)) 

show_image = True
verify_images = False
crop_all_images = False


def main():
    if show_image:
        show_crop()

    if verify_images or crop_all_images:
        image_loop()


def show_crop():
    print("Loading image paths.")
    x_paths = sorted([os.path.join(TRAIN_DIR_X, f) for f in os.listdir(TRAIN_DIR_X)[20:23]])
    y_paths = sorted([os.path.join(TRAIN_DIR_Y, f) for f in os.listdir(TRAIN_DIR_Y)[20:23]])

    print("Cropping images to show.")

    x_imgs = []
    y_imgs = []

    for i, (x_path, y_path) in enumerate(zip(x_paths, y_paths)): 
        print(i)
        x_imgs.append(do_crop_x(tifffile.imread(x_path)))
        y_imgs.append(do_crop_y(tifffile.imread(y_path)))       

    print("Plotting.")

    plt.subplot(231)
    plt.imshow(x_imgs[0][0])
    plt.subplot(232)
    plt.imshow(y_imgs[0][53])
    plt.subplot(233)
    plt.imshow(x_imgs[1][0])
    plt.subplot(234)
    plt.imshow(y_imgs[1][53])
    plt.subplot(235)
    plt.imshow(x_imgs[2][0])
    plt.subplot(236)
    plt.imshow(y_imgs[2][53])


def image_loop():
    print("Loading image paths.")
    # List available files in each folder
    x_train = sorted([os.path.join(TRAIN_DIR_X, f) for f in os.listdir(TRAIN_DIR_X)])
    y_train = sorted([os.path.join(TRAIN_DIR_Y, f) for f in os.listdir(TRAIN_DIR_Y)])

    print(f"Dataset has {len(x_train)} X and {len(y_train)} Y images.")
    if len(x_train) != len(y_train):
        print("THAT'S BAD!")

    print("Dataset:")
    for i, (x_path, y_path) in enumerate(zip(x_train, y_train)):
        print("index:", i)
        x_img = tifffile.imread(x_path)
        y_img = tifffile.imread(y_path)

        if verify_images: 
            check_for_errors(i, x_img, y_img, x_path, y_path)
        if crop_all_images:
            x_img, y_img = do_crop(x_img, y_img)
        tifffile.imwrite(x_path, x_img)
        tifffile.imwrite(y_path, y_img)
    print("Image loop done.")


def check_for_errors(i, x_img, y_img, x_path, y_path):
    if y_path.split('/')[-1].split('_')[0] != x_path.split('/')[-1].split('_')[0]:
        print(f"Image index {i}: ")
        print(f"X ({x_path}) and Y ({y_path}) are probably not the same image.")

    x_nan = np.count_nonzero(np.isnan(x_img))
    if x_nan != 0:
        print(f"X image {i}  ({x_path}) contains {x_nan} nan values.")

    y_nan = np.count_nonzero(np.isnan(y_img))
    if y_nan != 0:
        print(f"Y image {i} ({y_path}) contains {y_nan} nan values.")   

def do_crop(x, y):
    x = x[:, crop_x[1][0]:crop_x[1][1], crop_x[0][0]:crop_x[0][1]]
    y = y[:, crop_y[1][0]:crop_y[1][1], crop_y[0][0]:crop_y[0][1]]
    return x, y

def do_crop_x(x):
    x_new = x[:, crop_x[1][0]:crop_x[1][1], crop_x[0][0]:crop_x[0][1]]
    return x_new

def do_crop_y(y):
    y_new = y[:, crop_y[1][0]:crop_y[1][1], crop_y[0][0]:crop_y[0][1]]
    return y_new


if __name__ == "__main__":
    print("Starting verfication.")
    main()