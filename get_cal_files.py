import numpy as np
import csv
from envi_header import *

def get_calibration_file(directory,exposure):

    def get_filepaths(directory):
        """
        This function will generate the file names in a directory
        tree by walking the tree either top-down or bottom-up. For each
        directory in the tree rooted at directory top (including top itself),
        it yields a 3-tuple (dirpath, dirnames, filenames).
        """
        file_paths = []  # List which will store all of the full filepaths.

        # Walk the tree.
        for root, directories, files in os.walk(directory):
            for filename in files:
                # Join the two strings in order to form the full filepath.
                filepath = os.path.join(root, filename)
                file_paths.append(filepath)  # Add it to the list.

        return file_paths  # Self-explanatory.


    # Run the above function and store its results in a variable.


    full_file_paths = get_filepaths(directory)
    All_intercept_files = [s for s in full_file_paths if 'Intercept' in s]
    All_slope_files = [s for s in full_file_paths if 'Slope' in s]



    int_file = [s for s in All_intercept_files if exposure in s][0]
    slope_file = [s for s in All_slope_files if exposure in s][0]

    return int_file, slope_file

def parse_slope_data(slope_file):

    rd = open(slope_file,'rU')
    csv_reader = csv.reader(rd)
    data = list(csv_reader)
    data = np.asarray(data)

    wavelength_dat = data[1:,0]
    wavelength_dat = wavelength_dat.astype(np.float)
    wavelength_dat = wavelength_dat.flatten()

    slope_data = data[1:,1:]
    slope_data = slope_data.astype(np.float32)
    slope_data = np.transpose(slope_data)

    return slope_data

def parse_intercept_data(int_file):

    rd = open(int_file, 'rU')
    csv_reader = csv.reader(rd)
    data = list(csv_reader)
    data = np.asarray(data)

    wavelength_dat = data[1:, 0]
    wavelength_dat = wavelength_dat.astype(np.float)
    wavelength_dat = wavelength_dat.flatten()

    int_data = data[1:, 1:]
    int_data = int_data.astype(np.float32)
    int_data = np.transpose(int_data)

    return int_data

