import matplotlib.pyplot as plt
import numpy as np
import tifffile
import os
import scipy
import polanalyser as pa

def main():
    # images
    img_folder = os.path.join('testing', 'dfa_imgs_dial8')
    names = ['M','B','C','G','Y','R']
    names_pol = ['0', '45', '90', '135']

    M = tifffile.imread(os.path.join(img_folder, 'M.tif'))
    B = tifffile.imread(os.path.join(img_folder, 'B.tif'))
    C = tifffile.imread(os.path.join(img_folder, 'C.tif'))
    G = tifffile.imread(os.path.join(img_folder, 'G.tif'))
    Y = tifffile.imread(os.path.join(img_folder, 'Y.tif'))
    R = tifffile.imread(os.path.join(img_folder, 'R.tif'))


    imgs = np.array([M, B, C, G, Y, R])
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
        img = imgs[color, pol, 230:270, 230:270]
        plt.imshow(img)
        plt.colorbar()
        plt.text(5,95,f'SNR: {snr(img)},\nMax: {np.max(img)},\nMin: {np.min(img)}', c='white')

    # Plot 
    example_color = 4
    plt.figure(figsize=(10,6))
    plt.suptitle(f'({img_folder}) Close-up of DFA diffractive pattern for color {names[example_color]}')

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
    img = imgs_raw[example_color, 230:270, 230:270]
    plt.imshow(img)
    plt.colorbar()
    plt.text(5,95,f'SNR: {snr(img)},\nMax: {np.max(img)},\nMin: {np.min(img)}', c='white')
    plt.savefig(img_folder+"/dfa_pattern.png")


    # creating 4 color matrices with pearson coefficient
    matrix_col = np.zeros((4, n, n))

    for pol in range(4):
        for i in range(n):
            for j in range(n):
                a, _ = scipy.stats.pearsonr(imgs[i, pol], imgs[j, pol], axis=None)
                matrix_col[pol, i, j] = a


    # plotting correlation matrices of colors
    def plot_corr_col(polar):
        plt.imshow(matrix_col[polar])

        # adding colorbar
        plt.colorbar()
        
        # Adding labels to the matrix
        plt.xticks(range(len(matrix_col[polar])), names, rotation=45, ha='right')
        plt.yticks(range(len(matrix_col[polar])), names)

    plt.figure(figsize=(10,8))
    plt.suptitle(f'({img_folder}) Pearson Correlation Coefficient for DFA structures of different colors')
    plt.subplot(221)
    plt.title('P=0')
    plot_corr_col(0)
    plt.subplot(222)
    plt.title('P=45')
    plot_corr_col(1)
    plt.subplot(223)
    plt.title('P=90')
    plot_corr_col(2)
    plt.subplot(224)
    plt.title('P=135')
    plot_corr_col(3)
    plt.savefig(img_folder+"/corr_col.png")


    # creating n polarisation matrices with pearson coefficient
    matrix_pol = np.zeros((n, 4, 4))

    for i in range(n):
        for pol_i in range(4):
            for pol_j in range(4):
                a, _ = scipy.stats.pearsonr(imgs[i, pol_i], imgs[i, pol_j], axis=None)
                matrix_pol[i, pol_i, pol_j] = a

    # plotting correlation matrices of polarisation
    def plot_corr_pol(col):
        plt.imshow(matrix_pol[col])
        # adding colorbar
        plt.colorbar()
        # Adding labels to the matrix
        plt.xticks(range(len(matrix_pol[col])), names_pol, rotation=45, ha='right')
        plt.yticks(range(len(matrix_pol[col])), names_pol)

    plt.figure(figsize=(10,6))
    plt.suptitle(f'({img_folder}) Pearson Correlation Coefficient for DFA structures of different polarisations')
    plt.subplot(231)
    plt.title('M')
    plot_corr_pol(0)
    plt.subplot(232)
    plt.title('B')
    plot_corr_pol(1)
    plt.subplot(233)
    plt.title('C')
    plot_corr_pol(2)
    plt.subplot(234)
    plt.title('G')
    plot_corr_pol(3)
    plt.subplot(235)
    plt.title('Y')
    plot_corr_pol(4)
    plt.subplot(236)
    plt.title('R')
    plot_corr_pol(5)
    plt.savefig(img_folder+"/corr_pol.png")

    # show
    plt.show()

## calc SNR
def snr(img, axis=None, ddof=0):
    img = np.asanyarray(img)
    m = img.mean(axis)
    sd = img.std(axis=axis, ddof=ddof)
    return np.where(sd == 0, 0, m/sd)

if __name__ == '__main__':
    main()