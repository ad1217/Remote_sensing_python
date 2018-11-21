from __future__ import print_function
from statement_inputs import get_RawFile
from envi_header import *
from get_cal_files import get_calibration_file
from get_cal_files import parse_slope_data
from get_cal_files import parse_intercept_data
from edit_metadata_files import get_exposure
from convert_raw_dn_to_radiance import convert_raw_to_rad
from edit_metadata_files import move_scan_settings_file
import datetime

print('***************************************************************************************************************')
print('Code Converting the Raw DN of the Headwall Camera to Radiance')

start_time = '{:%Y-%m-%d_%H:%M:%S}'.format(datetime.datetime.now())
Raw_File, Header_File = get_RawFile()
directory_path = os.getcwd()
directory_cal_file = './calibration_folder'

results_folder = 'Image_Converted_To_Radiance'
if not os.path.exists(results_folder):
    os.makedirs(results_folder)

exposure = get_exposure(Header_File)
int_file, slope_file = get_calibration_file(directory_cal_file,exposure)
slope_data = parse_slope_data(slope_file)
int_data = parse_intercept_data(int_file)

rad_file_path = convert_raw_to_rad(directory_path,results_folder,Raw_File,Header_File,slope_data,int_data)
move_scan_settings_file(Header_File,rad_file_path)

end_time = '{:%Y-%m-%d_%H:%M:%S}'.format(datetime.datetime.now())

print('***************************************************************************************************************')
print('Start Time = ',start_time)
print('End Time = ',end_time)
print('Headwall File', Raw_File)
print('Exposure the data was collected = ',exposure)
print('Slope File = ', slope_file)
print('Intercept File = ', int_file)
print('Saved Radiance File = ', rad_file_path)
print('***************************************************************************************************************')