from __future__ import print_function
import spectral
from spectral import envi
import numpy as np
from collections import OrderedDict


def vegetation_indices(root_dir, filename):

    def get_index(wavelength):
        return np.argmin(np.absolute(img_bandcenters_array - wavelength))

    def band_search(wavelength):
        return img_obj.read_band(get_index(wavelength))

    def broad(wavelength_min, wavelength_max):
        band_idxs = [get_index(x) for x in range(wavelength_min, wavelength_max)]
        band_values = img_obj.read_bands(band_idxs)
        return np.average(band_values, axis=2)

    dirname = root_dir + filename + "/reflectance/veg-extract/"
    fpath = dirname + filename + "NDVI05.hdr"
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

    veg_indices = np.stack(VIs.values(), axis=2)
    envi.save_image(dirname + filename + "vegetation_indices.hdr", veg_indices, force=True, dtype=np.float32,
                    metadata={'band names': VIs.keys()})

    #average value for each VI
    avg_vi = {k: np.average(v) for k, v in VIs}
    avg_vi["Filename"] = filename
    return avg_vi

