from __future__ import print_function
import numpy as np
import datetime
import os
import shutil

def scan_file_inputs(Header_File):
    dirc = Header_File.rsplit('/', 1)[0]
    scan_file = dirc + '/scan.txt'

    dat_info = []
    with open(scan_file,'r') as f:
        for line in f:
            x = line.split(" = ")[-1]
            dat_info.append(float(x))


    speed = dat_info[0]
    dat_info = dat_info[1:]
    dat_info = np.array(dat_info) + 0.
    dat_info_org = np.reshape(dat_info,(len(dat_info)/3,3))

    start_position_angle = dat_info_org[:,0]
    stop_position_angle = dat_info_org[:,1]
    raw_files_in_dir = dat_info_org[:,2]

    raw_filename = Header_File.rsplit('/', 1)[1]
    rd_num = int(raw_filename.rsplit('_')[1])

    def find_nearest(array, value):
        idx = (np.abs(array - value)).argmin()
        return array[idx]

    rd_num_in_scan = find_nearest(raw_files_in_dir, rd_num)
    raw_img_pos = np.argwhere(rd_num_in_scan == raw_files_in_dir)
    start_angle_img = start_position_angle[int(raw_img_pos)]
    stop_angle_img = stop_position_angle[int(raw_img_pos)]

    if start_angle_img > stop_angle_img:
        img_corr_method = 'fliplr'
    elif start_angle_img < stop_angle_img:
        img_corr_method = 'rot180'
    print(img_corr_method)

    return speed, start_angle_img, stop_angle_img, img_corr_method

def create_log_files(results_folder,Header_File, speed, start_angle_img, stop_angle_img, radiance_file_name,
                     reflectance_file_name, Number_Poles, row, column, bands, white_plaque_num):
    dirc = Header_File.rsplit('/', 1)[0]
    settings_file = dirc + '/settings.txt'

    data_folder = Header_File.rsplit('/')[-2]
    hdr_file = Header_File.rsplit('/')[-1]
    rad_file = hdr_file.rsplit('.')[0]

    dat_info = []
    with open(settings_file, 'r') as f:
        for line in f:
            x = line.split(" = ")
            dat_info.append(x)

    start_time = dat_info[0][1]
    exposure = dat_info[2][1]
    frame_period = dat_info[3][1]

    height_of_mast = float(Number_Poles) * 1 + 1

    directory_path = os.getcwd()
    log_file = directory_path + '/' + results_folder + '/' + 'log_file_' + reflectance_file_name + '.txt'

    f = open(log_file, 'w')
    f.write('---Information about the data collection---\r\n')
    f.write('\r\n')
    f.write('Data folder = ' + data_folder + '\r\n')
    f.write('Name of the original radiance file = ' + rad_file + '\r\n')
    f.write('Data collection date = ' + start_time)
    f.write('Height of the mast(m) {number of poles} = ' + str(height_of_mast) + ' {' + Number_Poles + '}' '\r\n')
    f.write('Exposure(ms) = ' + exposure)
    f.write('Frame Period(ms) = ' + frame_period)
    f.write('Image size = ' + '{' + str(row) + ',' + str(column) + ',' + str(bands) + '}\r\n')
    f.write('Speed(deg/s) = ' + str(speed) + '\r\n')
    f.write('Zenith angles: ' + str(start_angle_img) + ' to ' + str(stop_angle_img) + '\r\n')
    f.write('Azimuth angles: Not available for now\r\n')
    f.write('\r\n')
    f.write('---Post Processing Information---\n')
    f.write('\r\n')
    f.write('Timestamp: {:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()) + '\r\n')
    f.write('Name of the radiance cube with correct orientation = ' + radiance_file_name + '\r\n')
    f.write('Name of the reflectance file = ' + reflectance_file_name + '\r\n')
    f.write('Spectralon Panel used for the reflectance calculation = ' + white_plaque_num + '\r\n')
    f.close()

    return

def get_exposure(Header_File):

    dirc = Header_File.rsplit('/', 1)[0]
    settings_file = dirc + '/settings.txt'

    dat_info = []
    with open(settings_file, 'r') as f:
        for line in f:
            x = line.split(" = ")
            dat_info.append(x)

    exposure = dat_info[2][1]
    exposure = exposure.rstrip()

    return exposure

def move_scan_settings_file(Header_File,rad_file_path):

    dirc = Header_File.rsplit('/', 1)[0]
    path_to_image = os.path.dirname(rad_file_path)

    print('Copying scan.txt & settings.txt into the new image folder')
    shutil.copy2(dirc + '/scan.txt', path_to_image + '/scan.txt')
    shutil.copy2(dirc + '/settings.txt', path_to_image + '/settings.txt')

    return
