import cuvis
import numpy as np
import platform
import os

# Directory containing the .cu3s files
dir_path = "proof_of_concept\\images_cubert"

# Initialize a list to store the data arrays
data_arrays = []

# Load each .cu3s file and add the data array to the list
for i in range(1, 11):
    file_path = os.path.join(dir_path, f"dark_{i}.cu3s")
    measurement = cuvis.SessionFile(file_path)[0]
    data = measurement.data['cube']
    data_array = np.array(data.array)
    data_arrays.append(data_array)

# Stack the data arrays along a new axis and compute the average
stacked_data = np.stack(data_arrays, axis=0)
average_data = np.mean(stacked_data, axis=0)
average_data = average_data.astype(int)

# Print the shape of the averaged data
print("Averaged data shape:", average_data.shape)
print("Averaged data (sample values):", average_data[0, 0, :])

# Load preexisting .cu3s file
file_path = os.path.join(dir_path, f"dark_10.cu3s")
measurement = cuvis.SessionFile(file_path)[0]
assert measurement._handle

print(dir(measurement))


# rewrite it's array
measurement.data['cube'].array = average_data

# check that it is rewritten
print("Average Cube: ", np.array(measurement.data['cube'].array)[0,0,:])

# export the mesu
saveArgs = cuvis.SaveArgs(export_dir=dir_path, allow_overwrite=True, allow_session_file=True)
cubeExporter = cuvis.Export.CubeExporter(saveArgs)
cubeExporter.apply(measurement)


