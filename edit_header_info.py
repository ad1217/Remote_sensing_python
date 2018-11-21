from __future__ import print_function

def get_header_file_reflectance(Header_File,Output_Header_File):

    f = open(Header_File, 'r')
    linelist = f.readlines()
    f.close

    # Re-open file here
    f2 = open(Output_Header_File, 'w')
    for line in linelist:
        line = line.replace('HEADWALL Hyperspec III],RADIANCE', '[HEADWALL Hyperspec III],Conversion to Reflectance Cube')
        line = line.replace('bsq','bip')
        line = line.replace('{49,86,191}','{38,93,149}')
        f2.write(line)
    f2.close()

    return

def get_header_file_radiance(Header_File,Output_Header_File):

    f = open(Header_File, 'r')
    linelist = f.readlines()
    f.close

    # Re-open file here
    f2 = open(Output_Header_File, 'w')
    for line in linelist:
        line = line.replace('HEADWALL Hyperspec III],RADIANCE', '[HEADWALL Hyperspec III],Radiance - Correct Orientation')
        line = line.replace('bsq','bip')
        line = line.replace('{49,86,191}', '{38,93,149}')
        f2.write(line)
    f2.close()

    return

def get_header_file_radiance_conv(Header_File,Output_Header_File):

    f = open(Header_File, 'r')
    linelist = f.readlines()
    f.close

    # Re-open file here
    f2 = open(Output_Header_File, 'w')
    for line in linelist:
        line = line.replace('[HEADWALL Hyperspec III]', '[HEADWALL Hyperspec III],Radiance - Own Calibration')
        line = line.replace('data type = 12', 'data type = 4')
        line = line.replace('bil','bip')
        line = line.replace('default bands = {49,86,191}', 'default bands = {149,93,38}')
        f2.write(line)
    f2.close()

    return