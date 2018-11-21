from __future__ import print_function
import spectral
import numpy as np
from spectral import envi
import os
from edit_header_info import *


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

    #thresh_min = threshold_minimum(NDVI_image)
    #binary_min = cv2.threshold(NDVI_image, thresh_min, 1, cv2.THRESH_BINARY)[1]
    #global_thresh = threshold_otsu(NDVI_image)
    #binary_global = cv2.threshold(NDVI_image, global_thresh, 1, cv2.THRESH_BINARY)[1]
    #binary_matrix = np.stack(binary_global*bands, 1)
   # print(binary_matrix.shape)
    #vegetation = binary_global * img

    #save image in new folder called veg-extract
    os.makedirs(dirname + "/veg-extract")
    envi.save_image(dirname + "veg-extract/" + filename + "NDVI05.hdr", img, force=True, dtype=np.float32)
    get_header_file_radiance_conv(fpath, dirname + "veg-extract/" + filename + "NDVI05.hdr")

    #cv2.imshow("binary_threshold", binary_global)
    #cv2.waitKey(0)
    #return binary_global



