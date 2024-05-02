# -*- coding: utf-8 -*-
"""
Created on Thu May  2 09:54:05 2024

@author: sayala
"""

# Return the monthly site albedo for a given lat/lon value
def returnAlbedo(lat,lon) :
    '''
    return: list of 12 albedo values
    '''
    
    #TODO: return albedo value based on NASA map, 
    from skimage import io, img_as_float

    # read in NASA MODIS 1800x3600 .JPG images.  pixel [900,1800] represents 0.0 , 0.0
    latIndex = int(900-round(lat*10)) #90 lat = 0, -90 lat = 1800
    lonIndex = int(round(lon*10)+1800) #-180 = 0, 180 = 3600
    
    filelist = getfilelist(os.path.join(testfolder,'albedo'),'.jpg')
    albedo = [] 
    for file1 in filelist:
        image = img_as_float(io.imread(os.path.join(testfolder,'albedo',file1)))
        albedo_val  = image[latIndex,lonIndex]
        if albedo_val < 1:
            albedo.append(albedo_val)
    
    if albedo.__len__() == 0:
        albedo.append(1)
    return sum(albedo) / albedo.__len__()  #average annual albedo for the location

