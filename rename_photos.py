# coding=utf-8
import os
import sys
import math
import exifread 
'''
dir = 0.386-math.pi/2
if(dir<0):
    dir += math.pi*2
dir = dir / math.pi * 180
#dir = -2.765
'''
def exifread_infos(photo):
    
    #加载 ExifRead 第三方库  https://pypi.org/project/ExifRead/
    #获取照片时间、经纬度信息
    #photo参数：照片文件路径
    
    # Open image file for reading (binary mode) 
    f = open(photo, 'rb')
    # Return Exif tags
    tags = exifread.process_file(f)

    try:
        #拍摄时间
        EXIF_Date=tags["EXIF DateTimeOriginal"].printable
        #纬度
        LatRef=tags["GPS GPSLatitudeRef"].printable
        Lat=tags["GPS GPSLatitude"].printable[1:-1].replace(" ","").replace("/",",").split(",")
        Lat=float(Lat[0])+float(Lat[1])/60+float(Lat[2])/float(Lat[3])/3600
        if LatRef != "N":
            Lat=Lat*(-1)
        #经度
        LonRef=tags["GPS GPSLongitudeRef"].printable
        Lon=tags["GPS GPSLongitude"].printable[1:-1].replace(" ","").replace("/",",").split(",")
        Lon=float(Lon[0])+float(Lon[1])/60+float(Lon[2])/float(Lon[3])/3600
        if LonRef!="E":
            Lon=Lon*(-1)
        f.close()
    except :
        return False,"ERROR:请确保照片包含经纬度等EXIF信息。"
    else:
        return True,EXIF_Date,Lat,Lon

def myrename(originname, lng, lat):
    flag = True
    i = 0
    while(flag):
        newname = 'photo_lng'+lng+'_lat'+lat+'_'+str(i)+'.jpg'
        if(os.path.isfile(newname)):
            i += 1
        else:
            os.rename(fs, newname)
            #+'_dir'+str(round(dir,2))
            print(newname)
            flag = False

####################
# 主入口
####################
if __name__ == '__main__':
    print(sys.path[0])
    flist = os.listdir(sys.path[0])
    for fs in flist:
        if(os.path.isfile(fs)):
            sp = fs.split('.')
            if(sp[-1]=='jpg' or sp[-1]=='jpeg' or sp[-1]=='JPG' or sp[-1]=='JPEG'):
                #fname = 'IMG_20180709_182639.jpg'
                res = exifread_infos(fs)
                if(res[0]):
                    print(res)
                    myrename(fs, str(round(res[3],6)), str(round(res[2],6)))
