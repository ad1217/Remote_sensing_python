#!/usr/bin/env python3

#Runs vegetation threshold and vegetation indices

from collections import OrderedDict
from csv import DictWriter
import os

import numpy as np

import spectral
from spectral import envi

ROOT_DIR = "/Volumes/New Volume/indoor_plant_measurements_20180831"

def vegetation_mask(root_dir, filename):
    dirname = root_dir + filename + "/reflectance/"
    fpath = dirname + filename + "reflectance-crop.hdr"


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
    envi.save_image(os.path.join(dirname, "veg-extract/", filename + "NDVI05.hdr"), img, force=True, dtype=np.float32)
    get_header_file_radiance_conv(fpath, os.path.join(dirname, "veg-extract", filename + "NDVI05.hdr"))


def get_header_file_reflectance(Header_File,Output_Header_File):

    f = open(Header_File, 'r')
    linelist = f.readlines()
    f.close

    # Re-open file here
    f2 = open(Output_Header_File, 'w')
    for line in linelist:
        line = line.replace('HEADWALL Hyperspec III],RADIANCE', '[HEADWALL Hyperspec III],Conversion to Reflectance Cube')
        line = line.replace('bsq','bip')
        line = line.replace('{49,86,191}','{38,93,149}')
        f2.write(line)
    f2.close()

    return

def get_header_file_radiance(Header_File,Output_Header_File):

    f = open(Header_File, 'r')
    linelist = f.readlines()
    f.close

    # Re-open file here
    f2 = open(Output_Header_File, 'w')
    for line in linelist:
        line = line.replace('HEADWALL Hyperspec III],RADIANCE', '[HEADWALL Hyperspec III],Radiance - Correct Orientation')
        line = line.replace('bsq','bip')
        line = line.replace('{49,86,191}', '{38,93,149}')
        f2.write(line)
    f2.close()

    return

def get_header_file_radiance_conv(Header_File,Output_Header_File):

    f = open(Header_File, 'r')
    linelist = f.readlines()
    f.close

    # Re-open file here
    f2 = open(Output_Header_File, 'w')
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

    def band_search(wavelength):
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

    VIs["REP"] = 700 + 40 * (((band_search(670) + band_search(780)) / 2) - band_search(700)) / \
          (band_search(740) - band_search(700))
    VIs["NDVI"] = ((band_search(800) - band_search(680))/(band_search(800) + band_search(680)))
    VIs["WI"] = band_search(900)/ band_search(970)
    VIs["OSAVI"] = (band_search(800) - band_search(670)) / (band_search(800) + band_search(670) + 0.16)+ 1.16
    VIs["OSAVI2"] = 1.16 + (band_search(750) - band_search(705))/(band_search(750) + band_search(705) + 0.16)
    VIs["MCARI"] = (band_search(700) - band_search(670)) - 0.2 * (
                band_search(700) - band_search(550)) * (
                        band_search(700) / band_search(670))
    VIs["RES"] = (band_search(718) - band_search(675)) / (
                band_search(755) + band_search(675))
    VIs["NDNI"] = (np.log10(1 / band_search(1510)) - np.log10(1 / band_search(1680))) / (
                np.log10(1 / band_search(1510)) + np.log10(1 / band_search(1680)))
    VIs["PRI"] = (band_search(531) - band_search(570)) / (band_search(531) + band_search(570))

    # indices using 680 as red, 800 as NIR, 530 as GREEN
    VIs["RVI"] = band_search(800)/ band_search(680)
    VIs["GRVI"] = (band_search(530)- band_search(680)) / (band_search(530) + band_search(680))
    VIs["MSAVI"] = 2 * band_search(800) + 1 - np.sqrt((2 * band_search(800)+1) ** 2 - 8 *
                                                      (band_search(800) - band_search(680))) / 2
    VIs["WDR_NDVI"] = (0.2*band_search(800) - band_search(680)) / (0.2 * band_search(800) + band_search(680))


    NIR_broad = broad(841, 876)
    RED_broad = broad(620, 670)
    GREEN_broad = broad(545, 565)

    #calculate broad-band indices
    VIs["RVI_broad"] =  NIR_broad/ RED_broad
    VIs["GRVI_broad"] = (GREEN_broad- RED_broad) / (GREEN_broad + RED_broad)
    VIs["MSAVI_broad"] = 2 * NIR_broad + 1 - np.sqrt((2 * NIR_broad+1) ** 2 - 8 * (NIR_broad - RED_broad)) / 2
    VIs["WDR_NDVI_broad"] = (0.2*NIR_broad - RED_broad) / (0.2 * NIR_broad + RED_broad)

    veg_indices = np.stack(list(VIs.values()), axis=2)
    envi.save_image(os.path.join('/Volumes/New Volume/vis_indoor_plant_measurements_20180831', filename + "vegetation_indices.hdr"), veg_indices, force=True, dtype=np.float32,
                    metadata={'band names': list(VIs.keys())})

    #average value for each VI (not working...)
    avg_vi = {k: np.nanmean(v) for k, v in VIs.items()}
    avg_vi["Filename"] = filename
    print(avg_vi)
    return avg_vi


filenames = os.listdir(ROOT_DIR)

average_VIs = []
for x, filename in enumerate(filenames):
    print(f"processing {filename} number {x} of {len(filenames)}")
    #vegetation_mask(ROOT_DIR, filename)
    average_VI = vegetation_indices(ROOT_DIR, filename)
    average_VIs.append(average_VI)



with open('Average-VIs.csv', 'w') as f:
    writer = DictWriter(f, list(average_VIs[0].keys()))
    writer.writeheader()
    writer.writerows(average_VIs)
