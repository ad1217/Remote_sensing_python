from __future__ import print_function
import spectral
import numpy as np
import cv2
from skimage.filters import threshold_otsu, threshold_minimum

def vegetation_mask(fpath, ):
    img_obj = spectral.open_image(fpath)

    img_band_obj = img_obj.bands
    img_bandcenters_array = np.array( img_band_obj.centers)

    red_band_idx = np.argmin(np.absolute(img_bandcenters_array- 670.0))
    nir_band_idx = np.argmin(np.absolute(img_bandcenters_array - 800.0))

    red_image = img_obj.read_band(red_band_idx)
    nir_image = img_obj.read_band(nir_band_idx)

    NDVI_image = (nir_image - red_image)/(nir_image + red_image)

    #thresh_min = threshold_minimum(NDVI_image)
    #binary_min = cv2.threshold(NDVI_image, thresh_min, 1, cv2.THRESH_BINARY)[1]

    global_thresh = threshold_otsu(NDVI_image)
    binary_global = cv2.threshold(NDVI_image, global_thresh, 1, cv2.THRESH_BINARY)[1]
    return binary_global
