import matplotlib.pyplot as plt
import numpy as np
import tifffile
import os
import scipy
import polanalyser as pa

def main():
    # images
    img_folder = os.path.join('testing', 'dfa_imgs_dial8')
    names = ['R','M','B','C','G','Y']

    R = tifffile.imread(os.path.join(img_folder, 'R.tif'))
    M = tifffile.imread(os.path.join(img_folder, 'M.tif'))
    B = tifffile.imread(os.path.join(img_folder, 'B.tif'))
    C = tifffile.imread(os.path.join(img_folder, 'C.tif'))
    G = tifffile.imread(os.path.join(img_folder, 'G.tif'))
    Y = tifffile.imread(os.path.join(img_folder, 'Y.tif'))

    imgs = np.array([R, M, B, C, G, Y])
    n = len(imgs)

    # polarisation demosaicing
    imgs_raw = imgs
    imgs = np.array([pa.demosaicing(img, code=pa.COLOR_PolarMono) for img in imgs])

    # cropping to dfa size
    imgs = imgs[:, :, 700:1200, 1000:1500]
    imgs_raw = imgs_raw[:, 700:1200, 1000:1500]
    print(imgs.shape)

    def plot_closeup(color, pol):
        plt.title(f'Demosaiced P={pol*45}')
        img = imgs[color, pol, 200:300, 200:300]
        plt.imshow(img)
        plt.text(5,95,f'SNR: {snr(img)},\nMax: {np.max(img)},\nMin: {np.min(img)}', c='white')

    # Plot 
    example_color = 5
    plt.figure(figsize=(11,8))
    plt.suptitle(f'Close-up of DFA diffractive pattern for color {names[example_color]}')

    plt.subplot(231)
    plot_closeup(example_color,0)
    plt.subplot(232)
    plot_closeup(example_color,1)
    plt.subplot(234)
    plot_closeup(example_color,2)
    plt.subplot(235)
    plot_closeup(example_color,3)
    plt.subplot(236)
    plt.title('Raw')
    img = imgs_raw[example_color, 200:300, 200:300]
    plt.imshow(img)
    plt.text(5,95,f'SNR: {snr(img)},\nMax: {np.max(img)},\nMin: {np.min(img)}', c='white')

    # creating matrix with pearson coefficient
    matrix = np.zeros((4, n, n))

    for pol in range(4):
        for i in range(n):
            for j in range(n):
                a, _ = scipy.stats.pearsonr(imgs[i, pol], imgs[j, pol], axis=None)
                matrix[pol, i, j] = a


    # plotting correlation matrix
    def plot(polar):
        plt.imshow(matrix[polar])

        # adding colorbar
        plt.colorbar()
        
        # Adding labels to the matrix
        plt.xticks(range(len(matrix[polar])), names, rotation=45, ha='right')
        plt.yticks(range(len(matrix[polar])), names)

    plt.figure(figsize=(8,8))
    plt.suptitle('Pearson Correlation Coefficient for DFA structures of different colors')
    plt.subplot(221)
    plt.title('P=0')
    plot(0)
    plt.subplot(222)
    plt.title('P=45')
    plot(1)
    plt.subplot(223)
    plt.title('P=90')
    plot(2)
    plt.subplot(224)
    plt.title('P=135')
    plot(3)

    # Display the plot
    plt.show()

## calc SNR
def snr(img, axis=None, ddof=0):
    img = np.asanyarray(img)
    m = img.mean(axis)
    sd = img.std(axis=axis, ddof=ddof)
    return np.where(sd == 0, 0, m/sd)

if __name__ == '__main__':
    main()