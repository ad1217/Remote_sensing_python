from __future__ import print_function
import numpy as np
import spectral.io.envi as envi
from envi_header import *
import datetime
from edit_header_info import get_header_file_radiance_conv

def convert_raw_to_rad(directory,results_folder,Raw_File,Header_File,slope_data,int_data):

    # Get wavelengths and convert to NumPy array
    in_header = find_hdr_file(Header_File)
    header_data = read_hdr_file(in_header)
    wavelengths = header_data['wavelength'].split(',')[0:]
    wavelengths = [float(w) for w in wavelengths]
    wavelengths = numpy.array(wavelengths)

    img = envi.open(Header_File, Raw_File)
    img = img.open_memmap(writable=True)

    row = img.shape[0]
    column = img.shape[1]
    bands = img.shape[2]  # July 24, cmb: added this since we may need this info as well

    print('Making the matrix for the slope data: {:%Y-%m-%d_%H:%M:%S}'.format(datetime.datetime.now()))
    slope_data_repmat = np.kron(np.ones((row,1,1)), slope_data)
    print('Making the matrix for the intercept data: {:%Y-%m-%d_%H:%M:%S}'.format(datetime.datetime.now()))
    int_data_repmat = np.kron(np.ones((row,1,1)), int_data)
    print('Starting the conversion from DN to Radiance: {:%Y-%m-%d_%H:%M:%S}'.format(datetime.datetime.now()))
    radiance_conv = img*slope_data_repmat + int_data_repmat
    print('Starting to save the data: {:%Y-%m-%d_%H:%M:%S}'.format(datetime.datetime.now()))

    rad_file_name = '_rd_rit'
    (drname, fl_org) = os.path.split(Raw_File)
    rad_file_name_with_time = fl_org + rad_file_name
    img_folder = 'OwnCalRad_' + drname.rsplit('/')[-1]
    img_path = directory + '/' + results_folder + '/' + img_folder
    if not os.path.exists(img_path):
        os.makedirs(img_path)
    rad_file_path = directory + '/' + results_folder + '/' + img_folder + '/' + \
                    rad_file_name_with_time + '.hdr'

    envi.save_image(rad_file_path,radiance_conv, force=True, dtype=np.float32)
    get_header_file_radiance_conv(Header_File,rad_file_path)

    os.rename(rad_file_path,rad_file_path.rsplit('.')[0] + '.img.hdr')

    return rad_file_path
