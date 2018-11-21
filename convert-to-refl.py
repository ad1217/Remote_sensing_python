# wow!!! it's not pretty, but it works!!!!!! amazing!!!
#version 2-- for batch processing files: replace file path in line 54 to point to the folder containing the imagery


import numpy as np
from spectral import envi
import shutil
import os
from envi_header import *
from edit_header_info import *


#import calibration file (spectralon #3)
cal_file = np.loadtxt("D:/spectralon_num3_resample.txt", skiprows= 1)

#import avg. spectralon #3
whiteref_file = np.loadtxt("D:/white-ref/avg-only_white_plaque3.txt", skiprows= 1)

#set working directory
#os.chdir("D:/indoor_plant_measurements_20180831/")
#set image folder
#path = "high_nutrient_4_2018_08_31_15_04_01"
#path2 = "D:/indoor_plant_measurements_20180831/" + path
def convert_to_reflectance(path, path2):
    #import image
    img = envi.open(path2 + "/raw_0.hdr", path2 + "/raw_0")
    img = img.open_memmap(writable=True)

    #determine size of image
    row = img.shape[0]
    column = img.shape[1]
    bands = img.shape[2]

    print('Making the matrix for the calibration data')
    cal_matrix = np.kron(np.ones((row, 1, 1)), cal_file[:, 1])
    whiteref_matrix = np.kron(np.ones((row, 1, 1)), whiteref_file[:, 1])

    print('Converting to reflectance')
    reflectance_img = (img / whiteref_matrix) * cal_matrix
    print(reflectance_img.shape)

    #make reflectance folder
    os.makedirs(path2 + "/reflectance")


    #save image
    envi.save_image(path2 + "/reflectance/" + path + "reflectance.hdr", reflectance_img, force=True, dtype=np.float32)

    #read header data
    #read_hdr_file(path2 + "/raw_0.hdr")
    get_header_file_radiance_conv(path2 + "/raw_0.hdr", path2 + "/reflectance/" + path + "reflectance.hdr")


filenames = os.listdir("D:\indoor_plant_measurements_20180831")
i = len(filenames)
x = 0
for x in range(0, i):
    path = filenames[x]
    print("processing..." + path + "number" + str(x) + " of " + str(i))
    path2 = "D:/indoor_plant_measurements_20180831/" + path
    convert_to_reflectance(path, path2)
    x += 1


