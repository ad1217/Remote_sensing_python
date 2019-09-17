#!/usr/bin/env python3

#Runs vegetation threshold and vegetation indices

from collections import OrderedDict
from csv import DictWriter
import os

import numpy as np

import spectral
from spectral import envi

INPUT_DIR = "/Volumes/New Volume/indoor_plant_measurements_20180831"
OUTPUT_DIR = "/Volumes/New Volume/vis_indoor_plant_measurements_20180831"

def vegetation_mask(root_dir, filename):
    dirname = os.path.join(root_dir, filename, "reflectance/")
    fpath = os.path.join(dirname, filename + "reflectance-crop.hdr")


    img_obj = spectral.open_image(fpath)
    img = img_obj.open_memmap(writable=True)

    img_band_obj = img_obj.bands
    img_bandcenters_array = np.array(img_band_obj.centers)

    red_band_idx = np.argmin(np.absolute(img_bandcenters_array - 670.0))
    nir_band_idx = np.argmin(np.absolute(img_bandcenters_array - 800.0))

    red_image = img_obj.read_band(red_band_idx)
    nir_image = img_obj.read_band(nir_band_idx)

    NDVI_image = (nir_image - red_image)/(nir_image + red_image)
    #subset image based on NDVI threshold of 0.5
    img[NDVI_image < 0.5] = np.nan

    #save image in new folder called veg-extract
    if not os.path.isdir(dirname + "veg-extract"):
        os.makedirs(dirname + "veg-extract")
    envi.save_image(
        os.path.join(dirname, "veg-extract/", filename + "NDVI05.hdr"),
        img, force=True, dtype=np.float32)
    get_header_file_radiance_conv(
        fpath, os.path.join(dirname, "veg-extract", filename + "NDVI05.hdr"))

def get_header_file_radiance_conv(header_file, output_header_file):

    f = open(header_file, 'r')
    linelist = f.readlines()
    f.close

    # Re-open file here
    f2 = open(output_header_file, 'w')
    for line in linelist:
        line = line.replace('[HEADWALL Hyperspec III]', '[HEADWALL Hyperspec III],Radiance - Own Calibration')
        line = line.replace('data type = 12', 'data type = 4')
        line = line.replace('bil','bip')
        line = line.replace('default bands = {49,86,191}', 'default bands = {149,93,38}')
        f2.write(line)
    f2.close()

    return

def vegetation_indices(root_dir, filename):

    def get_index(wavelength):
        return np.argmin(np.absolute(img_bandcenters_array - wavelength))

    # Band Search
    def bs(wavelength):
        return img_obj.read_band(get_index(wavelength))

    def broad(wavelength_min, wavelength_max):
        band_idxs = [get_index(x) for x in range(wavelength_min, wavelength_max)]
        band_values = img_obj.read_bands(band_idxs)
        return np.average(band_values, axis=2)

    indirname = os.path.join(root_dir, filename, "reflectance/veg-extract/")
    fpath = os.path.join(indirname, filename + "NDVI05.hdr")
    img_obj = spectral.open_image(fpath)

    #define broad-bands
    img_band_obj = img_obj.bands
    img_bandcenters_array = np.array(img_band_obj.centers)

    VIs = OrderedDict()

    VIs["REP"] = 700 + 40 * (((bs(670) + bs(780)) / 2) - bs(700)) / (bs(740) - bs(700))
    VIs["NDVI"] = ((bs(800) - bs(680))/(bs(800) + bs(680)))
    VIs["WI"] = bs(900)/ bs(970)
    VIs["OSAVI"] = (bs(800) - bs(670)) / (bs(800) + bs(670) + 0.16)+ 1.16
    VIs["OSAVI2"] = 1.16 + (bs(750) - bs(705))/(bs(750) + bs(705) + 0.16)
    VIs["MCARI"] = (bs(700) - bs(670)) - 0.2 * (bs(700) - bs(550)) * (bs(700) / bs(670))
    VIs["RES"] = (bs(718) - bs(675)) / (bs(755) + bs(675))
    VIs["NDNI"] = (np.log10(1 / bs(1510)) - np.log10(1 / bs(1680))) / (np.log10(1 / bs(1510)) + np.log10(1 / bs(1680)))
    VIs["PRI"] = (bs(531) - bs(570)) / (bs(531) + bs(570))

    # indices using 680 as red, 800 as NIR, 530 as GREEN
    VIs["RVI"] = bs(800)/ bs(680)
    VIs["GRVI"] = (bs(530)- bs(680)) / (bs(530) + bs(680))
    VIs["MSAVI"] = 2 * bs(800) + 1 - np.sqrt((2 * bs(800)+1) ** 2 - 8 *
                                                      (bs(800) - bs(680))) / 2
    VIs["WDR_NDVI"] = (0.2*bs(800) - bs(680)) / (0.2 * bs(800) + bs(680))


    NIR_broad = broad(841, 876)
    RED_broad = broad(620, 670)
    GREEN_broad = broad(545, 565)

    #calculate broad-band indices
    VIs["RVI_broad"] =  NIR_broad/ RED_broad
    VIs["GRVI_broad"] = (GREEN_broad- RED_broad) / (GREEN_broad + RED_broad)
    VIs["MSAVI_broad"] = 2 * NIR_broad + 1 - np.sqrt((2 * NIR_broad+1) ** 2 - 8 * (NIR_broad - RED_broad)) / 2
    VIs["WDR_NDVI_broad"] = (0.2*NIR_broad - RED_broad) / (0.2 * NIR_broad + RED_broad)

    veg_indices = np.stack(list(VIs.values()), axis=2)
    envi.save_image(
        os.path.join(OUTPUT_DIR, filename + "vegetation_indices.hdr"),
        veg_indices, force=True, dtype=np.float32,
        metadata={'band names': list(VIs.keys())})

    #average value for each VI (not working...)
    avg_vi = {k: np.nanmean(v) for k, v in VIs.items()}
    avg_vi["Filename"] = filename
    print(avg_vi)
    return avg_vi


filenames = os.listdir(INPUT_DIR)

average_VIs = []
for x, filename in enumerate(filenames):
    print(f"processing {filename} number {x} of {len(filenames)}")
    #vegetation_mask(INPUT_DIR, filename)
    average_VI = vegetation_indices(INPUT_DIR, filename)
    average_VIs.append(average_VI)



with open('Average-VIs.csv', 'w') as f:
    writer = DictWriter(f, list(average_VIs[0].keys()))
    writer.writeheader()
    writer.writerows(average_VIs)
