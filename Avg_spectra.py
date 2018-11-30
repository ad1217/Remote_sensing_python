from __future__ import print_function
import spectral
from spectral import envi
import numpy as np
from collections import OrderedDict
import os
from csv import DictWriter
import collections


def average_spectrum(root_dir, filename):
    dirname = root_dir + filename + "/reflectance/veg-extract/"
    fpath = dirname + filename + "NDVI05_soil_mask.hdr"
    fpath2 = dirname + filename + "NDVI05.hdr"

    if os.path.isfile(fpath):
        img_obj = spectral.open_image(fpath)
    else:
        img_obj = spectral.open_image(fpath2)

    img = img_obj.open_memmap(writable=True)
    img_band_obj = img_obj.bands
    img_bandcenters_array = np.array(img_band_obj.centers)
    avg_refl = np.nanmean(img, axis=(0, 1))

    avg_spectrum = OrderedDict(zip(img_bandcenters_array, avg_refl))
    avg_spectrum["Filename"] = filename
    return avg_spectrum



ROOT_DIR = "D:/indoor_plant_measurements_20180831/"
filenames = os.listdir(ROOT_DIR)


average_spectra2 = []
for x, filename in enumerate(filenames):
    print("processing {} number {} of {}".format(filename, x, len(filenames)))
    average_spectra = average_spectrum(ROOT_DIR, filename)
    average_spectra2.append(average_spectra)

with open('Average_spectra.csv', 'w') as f:
    writer = DictWriter(f, average_spectra2[0].keys())
    writer.writeheader()
    writer.writerows(average_spectra2)

