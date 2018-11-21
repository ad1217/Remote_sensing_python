from vegetation_mask import *
import spectral
import os
from Vegetation_Indices import *
#to run a single file
filename = "control_1_2018_08_31_14_32_40"
#vegetation_mask(filename)
vegetation_indices(filename)


# uncomment to run batch
"""""
filenames = os.listdir("D:\indoor_plant_measurements_20180831")
i = len(filenames)

x = 0
for x in range(0, i):
    path = filenames[x]
    print("processing..." + path + "number" + x + " of " + i)
    path2 = "D:/indoor_plant_measurements_20180831/" + path + "/reflectance/"
    os.makedirs(path2 + "NDVI-threshold")
    vegetation_mask(path2 + path + ".img")
    x += 1
#set reflectance image folder
#path = "high_nutrient_4_2018_08_31_15_04_01"


#vegetation_mask()

"""""