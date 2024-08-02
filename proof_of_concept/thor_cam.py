import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import filedialog
from PIL import Image
from pylablib.devices import Thorlabs

# Function to list cameras and select the first available one
def initialize_camera():
    cameras = Thorlabs.list_cameras_tlcam()
    if not cameras:
        print("No cameras detected.")
        return None
    print(f"Available cameras: {cameras}")
    return Thorlabs.ThorlabsTLCamera(serial=cameras[0])

# Function to capture and display an image
def capture_image():
    global cam, canvas, ax
    if cam:
        try:
            # Capture a single frame
            frame = cam.snap()

            # Display the captured image
            ax.clear()
            ax.imshow(frame, cmap='gray')
            ax.set_title("Captured Image")
            canvas.draw()

            # Get the file name from the entry widget
            file_name = file_name_entry.get()
            if file_name:
                # Save the captured image as a .tif file
                img = Image.fromarray(frame)
                img.save(f"{file_name}.tif")
                print(f"Image saved as {file_name}.tif")
            else:
                print("No file name provided. Image not saved.")

        except Exception as e:
            print(f"Error capturing image: {e}")

# Function to close the camera and the GUI
def on_closing():
    if cam:
        cam.close()
    root.destroy()

# Initialize the camera
cam = initialize_camera()
if cam:
    cam.set_exposure(50E-3)
    cam.set_roi(0, 640, 0, 640, hbin=1, vbin=1)

# Create the main window
root = tk.Tk()
root.title("Thorlabs Camera Control")
root.geometry("1000x700")  # Set a larger default window size

# Create a frame for the image display
image_frame = tk.Frame(root, bg='white')
image_frame.grid(row=0, column=0, sticky='nsew')

# Create a figure and axis for displaying the image
fig, ax = plt.subplots(figsize=(8, 6))
canvas = FigureCanvasTkAgg(fig, master=image_frame)
canvas.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Create a frame for the controls
control_frame = tk.LabelFrame(root, text="Controls", padx=20, pady=20)
control_frame.grid(row=1, column=0, sticky='ew')

# Create an entry widget for the file name
file_name_label = tk.Label(control_frame, text="File Name:", font=('Arial', 14))
file_name_label.grid(row=0, column=0, padx=5, pady=5, sticky='w')
file_name_entry = tk.Entry(control_frame, width=40, font=('Arial', 14))
file_name_entry.grid(row=0, column=1, padx=5, pady=5, sticky='ew')

# Create a button to capture the image
capture_button = tk.Button(control_frame, text="Capture Image", command=capture_image, font=('Arial', 14))
capture_button.grid(row=0, column=2, padx=5, pady=5)

# Configure column weights to expand the controls frame properly
root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=0)

# Set up the closing protocol
root.protocol("WM_DELETE_WINDOW", on_closing)

# Start the GUI event loop
root.mainloop()
