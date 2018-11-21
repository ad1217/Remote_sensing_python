from vegetation_mask import *
import os
from Vegetation_Indices import *
from csv import DictWriter

ROOT_DIR = "D:/indoor_plant_measurements_20180831/"
filenames = os.listdir(ROOT_DIR)


average_VIs = []
for x, filename in enumerate(filenames):
    print("processing {} number {} of {}".format(filename, x, len(filenames)))
    vegetation_mask(ROOT_DIR, filename)
    average_VI = vegetation_indices(ROOT_DIR, filename)
    average_VIs.append(average_VI)



with open('Average-VIs.csv', 'w') as f:
    writer = DictWriter(f, average_VIs[0].keys())
    writer.writerows(average_VIs)