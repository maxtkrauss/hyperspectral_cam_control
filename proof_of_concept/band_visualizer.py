import numpy as np
import tifffile
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk

num_plots = 1

# Load the hyperspectral image
def load_image(file_path):
    return tifffile.imread(file_path)

class HyperspectralGUI:
    def __init__(self, root, image):
        self.root = root
        self.image = image
        self.band_vars = [tk.IntVar(value=0) for _ in range(num_plots)]
        self.create_widgets()

    def create_widgets(self):
        # Create Matplotlib figures
        self.figures = [plt.Figure(figsize=(5, 4), dpi=100) for _ in range(num_plots)]
        self.axes = [fig.add_subplot(111) for fig in self.figures]
        self.canvases = [FigureCanvasTkAgg(fig, master=self.root) for fig in self.figures]

        # Layout for the plots
        for i, canvas in enumerate(self.canvases):
            canvas.get_tk_widget().grid(row=0, column=i, padx=10, pady=10)

        # Create sliders
        for i, band_var in enumerate(self.band_vars):
            slider = tk.Scale(self.root, from_=0, to=105, orient='horizontal', variable=band_var, label=f'Band {i+1}')
            slider.grid(row=1, column=i, padx=10, pady=10)
            band_var.trace('w', lambda *args, idx=i: self.update_plot(idx))

        self.update_plots()

    def update_plot(self, idx):
        band_index = self.band_vars[idx].get()
        self.axes[idx].clear()

        self.axes[idx].imshow(self.image[:, :, band_index], cmap='viridis')
        self.axes[idx].set_title(f'Band {band_index}')
        self.axes[idx].figure.tight_layout()
        self.canvases[idx].draw()

    def update_plots(self):
        for i in range(num_plots):
            self.update_plot(i)

# Main function
def main():
    root = tk.Tk()
    root.title("Hyperspectral Image Viewer")
    image = load_image('images\\cubert\\3_cubert.tif')
    app = HyperspectralGUI(root, image)
    root.mainloop()

if __name__ == '__main__':
    main()
