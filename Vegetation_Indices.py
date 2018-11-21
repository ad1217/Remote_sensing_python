from __future__ import print_function
import spectral
from spectral import envi
import numpy as np
from collections import OrderedDict
import cv2
from skimage.filters import threshold_otsu, threshold_minimum
import os
from edit_header_info import *


def band_search(filename, wavelength):
    fpath = "D:/indoor_plant_measurements_20180831/" + filename + "/reflectance/veg-extract/" + filename + "NDVI05.hdr"

    img_obj = spectral.open_image(fpath)
    img_band_obj = img_obj.bands
    img_bandcenters_array = np.array(img_band_obj.centers)

    band_idx = np.argmin(np.absolute(img_bandcenters_array - wavelength))
    band_image = img_obj.read_band(band_idx)
    return band_image


def vegetation_indices(filename):
    dirname = "D:/indoor_plant_measurements_20180831/" + filename + "/reflectance/veg-extract/"
    fpath = dirname + filename + "NDVI05.hdr"
    img_obj = spectral.open_image(fpath)
    img = img_obj.open_memmap(writable=True)

    #define broad-bands
    img_band_obj = img_obj.bands
    img_bandcenters_array = np.array(img_band_obj.centers)
    def broad(wavelength_min, wavelength_max):
        band_idxs = [np.argmin(np.absolute(img_bandcenters_array - x)) for x in range(wavelength_min, wavelength_max)]
        band_values = img_obj.read_bands(band_idxs)
        return np.average(band_values, axis=2)
    NIR_broad = broad(841, 876)
    RED_broad = broad(620,670)
    GREEN_broad = broad(545, 565)


    VIs = OrderedDict()
    
    VIs["REP"] = 700 + 40 * (((band_search(filename, 670) + band_search(filename, 780)) / 2) - band_search(filename, 700)) / \
          (band_search(filename, 740) - band_search(filename, 700))
    VIs["NDVI"] = ((band_search(filename, 800) - band_search(filename, 680))/(band_search(filename, 800) + band_search(filename, 680)))
    VIs["WI"] = band_search(filename, 900)/ band_search(filename, 970)
    VIs["OSAVI"] = (band_search(filename, 800) - band_search(filename, 670)) / (band_search(filename, 800) + band_search(filename, 670) + 0.16)+ 1.16
    VIs["OSAVI2"] = 1.16 + (band_search(filename, 750) - band_search(filename, 705))/(band_search(filename, 750) + band_search(filename, 705) + 0.16)
    VIs["MCARI"] = (band_search(filename, 700) - band_search(filename, 670)) - 0.2 * (
                band_search(filename, 700) - band_search(filename, 550)) * (
                        band_search(filename, 700) / band_search(filename, 670))
    VIs["RES"] = (band_search(filename, 718) - band_search(filename, 675)) / (
                band_search(filename, 755) + band_search(filename, 675))
    VIs["NDNI"] = (np.log10(1 / band_search(filename, 1510)) - np.log10(1 / band_search(filename, 1680))) / (
                np.log10(1 / band_search(filename, 1510)) + np.log10(1 / band_search(filename, 1680)))
    VIs["PRI"] = (band_search(filename, 531) - band_search(filename, 570)) / (band_search(filename, 531) + band_search(filename, 570))

    # indices using 680 as red, 800 as NIR, 530 as GREEN
    VIs["RVI"] = band_search(filename, 800)/ band_search(filename, 680)
    VIs["GRVI"] = (band_search(filename, 530)- band_search(filename, 680)) / (band_search(filename, 530) + band_search(filename, 680))
    VIs["MSAVI"] = 2 * band_search(filename, 800) + 1 - np.sqrt((2 * band_search(filename, 800)+1) ** 2 - 8 * (band_search(filename, 800) - band_search(filename, 680))) / 2
    VIs["WDR_NDVI"] = (0.2*band_search(filename, 800) - band_search(filename, 680)) / (0.2 * band_search(filename, 800) + band_search(filename, 680))

    #calculate broad-band indices
    VIs["RVI_broad"] =  NIR_broad/ RED_broad
    VIs["GRVI_broad"] = (GREEN_broad- RED_broad) / (GREEN_broad + RED_broad)
    VIs["MSAVI_broad"] = 2 * NIR_broad + 1 - np.sqrt((2 * NIR_broad+1) ** 2 - 8 * (NIR_broad - RED_broad)) / 2
    VIs["WDR_NDVI_broad"] = (0.2*NIR_broad - RED_broad) / (0.2 * NIR_broad + RED_broad)

    print({a:b.shape for a, b in VIs.iteritems()})
    veg_indices = np.stack(VIs.values(), axis=2)
    print(veg_indices.shape)
    envi.save_image(dirname + filename + "vegetation_indices.hdr", veg_indices, force=True, dtype=np.float32,
                    metadata={'band names': VIs.keys()})

