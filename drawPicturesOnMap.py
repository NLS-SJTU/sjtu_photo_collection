#!/usr/bin/python3
# coding=utf-8
'''
Created on 2018/8/22

@author: mrh
'''
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.animation as animation
from matplotlib.widgets import Button
import matplotlib.axes
import os,sys
from PIL import Image,ExifTags
import math
import shutil
import copy


class MapShow:
    
    def __init__(self,data=[],flist_data=[],dir =''):
        
        self.data_list = data
        self.delete_data_list = []
        self.delete_data_num = -1
        self.delete_data_num_list = []
        self.flist = flist_data
        self.dir =dir
        
        
        self.MAP_WID=2000
        self.MAP_HGT=1600
        
        self.lng_max = 121.457382
        self.lng_min = 121.438068 
        self.lat_max = 31.038497
        self.lat_min = 31.026197
        # 18级地图图像尺度测量
        #  经纬度                   像素坐标
        # 121.446191,31.032396    461 ,524
        # 121.451114,31.030701    1004,741
        #
        # 每个水平像素坐标--> 9.066298342550862e-06 经度
        # 每个垂直像素坐标-->-7.811059907824902e-06 维度
        self.MAP_X_SCALE= (self.lng_max - self.lng_min) / self.MAP_WID       # 水平像素坐标增量对应经度增量
        self.MAP_Y_SCALE=-(self.lat_max - self.lat_min) / self.MAP_HGT       # 
        


        self.SJTU_LNG=(self.lng_max + self.lng_min)/2                  # 交大东校区中心
        self.SJTU_LAT=(self.lat_max + self.lat_min)/2      
        self.SJTU_LOC='%.6f,%.6f'%(self.SJTU_LNG,self.SJTU_LAT)
        
        self.DATA_SZ=len(self.data_list)
        #DATA_SZ = 1014
        
        self.MARK_SZ=4

        self.lng_mean = self.SJTU_LNG
        self.lat_mean = self.SJTU_LAT
        
        self.img_PIL = []
        self.img_PIL_origin = []
        
        self.fig = plt.figure(1)
        self.fig.canvas.mpl_connect('button_press_event', self.on_press)
    
    def set_data(self,data):
        self.data_list = data
        self.DATA_SZ=len(self.data_list)
    
    def set_delete_data(self,delete_data_list):
        self.delete_data_list = delete_data_list
        
    def set_edges(self,edge_gps_data):
        self.edge_gps_list = edge_gps_data
    
    def get_data_coord(self,n): return float(self.data_list[n][0]),float(self.data_list[n][1])

    # 找到指定位置的数据（最近距离的数据）
    def search_data_by_lng_lat(self,lng,lat):
        dmin=np.inf
        nmin=-1
        for n in range(self.DATA_SZ):
            lng0,lat0=self.get_data_coord(n)
            d=(lng-lng0)**2+(lat-lat0)**2
            if d<dmin:
                dmin=d
                nmin=n
        return nmin,dmin
    
    def drawAllData(self):
        img_PIL_origin = Image.open(os.getcwd()+'/sjtu_png.png')
        self.img_PIL_origin = np.array(img_PIL_origin.resize((self.MAP_WID, self.MAP_HGT),Image.ANTIALIAS))
        self.img_PIL = copy.copy(self.img_PIL_origin)
        x0,y0=self.MAP_WID/2,self.MAP_HGT/2
        
        for n in range(self.DATA_SZ):
            lng = self.data_list[n][0]
            lat = self.data_list[n][1]

            lng0,lat0=lng-self.lng_min,lat-self.lat_min
            pos_x = int(round(lng0/self.MAP_X_SCALE))
            pos_y = self.MAP_HGT + int(round(lat0/self.MAP_Y_SCALE))
            
            if(pos_x<0 or pos_x>self.MAP_WID or pos_y<0 or pos_y>self.MAP_HGT):
                if(not n in self.delete_data_num_list):
                    self.delete_data_list.append(self.flist[n])
                    self.delete_data_num_list.append(n)
        self.button_delete_press()


        for n in range(self.DATA_SZ):
            lng = self.data_list[n][0]
            lat = self.data_list[n][1]

            lng0,lat0=lng-self.lng_min,lat-self.lat_min
            pos_x = int(round(lng0/self.MAP_X_SCALE))
            pos_y = self.MAP_HGT + int(round(lat0/self.MAP_Y_SCALE))
            
            if(pos_x<0 or pos_x>self.MAP_WID or pos_y<0 or pos_y>self.MAP_HGT):
                if(not n in self.delete_data_num_list):
                    self.delete_data_list.append(self.flist[n])
                    self.delete_data_num_list.append(n)
#             print(pos_x,pos_y)
            self.img_PIL[pos_y-self.MARK_SZ:pos_y+self.MARK_SZ+1,pos_x-self.MARK_SZ:pos_x+self.MARK_SZ+1,0]=0
            self.img_PIL[pos_y-self.MARK_SZ:pos_y+self.MARK_SZ+1,pos_x-self.MARK_SZ:pos_x+self.MARK_SZ+1,1]=0
            self.img_PIL[pos_y-self.MARK_SZ:pos_y+self.MARK_SZ+1,pos_x-self.MARK_SZ:pos_x+self.MARK_SZ+1,2]=255
            
    
    
        # 显示有图像数据的地图点
        #每次清空显示，重新画
        plt.clf()
#         self.point = plt.axes([0.3,0.03,0.1,0.03])

        point1 = plt.axes([0.3,0.03,0.1,0.03])
        button1 = Button(point1, "select into delete list")
        point2 = plt.axes([0.5,0.03,0.1,0.03])
        button2 = Button(point2, "delete all photos in list")
        point3 = plt.axes([0.7,0.03,0.1,0.03])
        button3 = Button(point3, "recover from delete list")
        
        plt.subplot(121)
        plt.imshow(self.img_PIL)
        plt.draw()
        plt.show()
        
 
    def button_select_press(self):
        print('select')
        try:
            if(self.delete_data_num == -1):
                print('Click image to choose delete file...')
            else:
                if(not self.delete_data_num in self.delete_data_num_list):
                    self.delete_data_list.append(self.flist[self.delete_data_num])
                    self.delete_data_num_list.append(self.delete_data_num)
                print(self.delete_data_num_list)
                self.delete_data_num=-1
        except:
            print('Click image to choose delete file...')
            
    def button_delete_press(self):
        print('delete')
        try:
            if(not os.path.exists(self.dir+'/remove')):
                os.mkdir(self.dir+'/remove')
                
            for file in self.delete_data_list:
                print('delete file:',file)
                shutil.move(file,self.dir+'/remove')
            data_gps_delete = [] 
            for n in self.delete_data_num_list:
                data_gps_delete.append(self.data_list[n])
                
            for data in data_gps_delete:
                self.data_list.remove(data)
                
            for file in self.delete_data_list:
                self.flist.remove(file)
                
            self.DATA_SZ=len(self.data_list)
            print(self.DATA_SZ)
            self.delete_data_list=[]
            self.delete_data_num_list=[]
        except:
            print('Click image to choose delete file...')
            
    def button_recover_press(self):
        print('recover')
        try:
            if(self.delete_data_num in self.delete_data_num_list):
                self.delete_data_num_list.remove(self.delete_data_num)
                self.delete_data_list.remove(self.flist[self.delete_data_num])
        except:
            print('Click image to choose delete file...')
              
    def on_press(self,event):
#         print(event)
        if(event.xdata == None or event.ydata == None):
            return
        axes_posx = event.inaxes.get_position().get_points()[0][0]
        self.img_PIL = copy.copy(self.img_PIL_origin)
        if(axes_posx == 0.3):
            self.button_select_press()
        elif(axes_posx == 0.5):
            self.button_delete_press()
            self.drawAllData()
        elif(axes_posx == 0.7):
            self.button_recover_press()
        else:
            lng = round(self.lng_min + event.xdata*self.MAP_X_SCALE,6)
            lat = round(self.lat_min + (event.ydata-self.MAP_HGT)*self.MAP_Y_SCALE,6)
            print("you pressed gps" , lng, lat)
    
            click_gps_list = [lng,lat]
            n0,d=self.search_data_by_lng_lat(click_gps_list[0],click_gps_list[1])
            self.delete_data_num=n0
            print('select file:',self.flist[n0])
            
            x0,y0=self.MAP_WID/2,self.MAP_HGT/2
            for n in range(self.DATA_SZ):
                lng = self.data_list[n][0]
                lat = self.data_list[n][1]
    
                lng0,lat0=lng-self.lng_min,lat-self.lat_min
                pos_x = int(round(lng0/self.MAP_X_SCALE))
                pos_y = self.MAP_HGT + int(round(lat0/self.MAP_Y_SCALE))
                
                if(n == n0):
                    self.img_PIL[pos_y-self.MARK_SZ:pos_y+self.MARK_SZ+1,pos_x-self.MARK_SZ:pos_x+self.MARK_SZ+1,0]=255
                    self.img_PIL[pos_y-self.MARK_SZ:pos_y+self.MARK_SZ+1,pos_x-self.MARK_SZ:pos_x+self.MARK_SZ+1,1]=0
                    self.img_PIL[pos_y-self.MARK_SZ:pos_y+self.MARK_SZ+1,pos_x-self.MARK_SZ:pos_x+self.MARK_SZ+1,2]=0
                elif(n in self.delete_data_num_list):
                    self.img_PIL[pos_y-self.MARK_SZ:pos_y+self.MARK_SZ+1,pos_x-self.MARK_SZ:pos_x+self.MARK_SZ+1,0]=255
                    self.img_PIL[pos_y-self.MARK_SZ:pos_y+self.MARK_SZ+1,pos_x-self.MARK_SZ:pos_x+self.MARK_SZ+1,1]=0
                    self.img_PIL[pos_y-self.MARK_SZ:pos_y+self.MARK_SZ+1,pos_x-self.MARK_SZ:pos_x+self.MARK_SZ+1,2]=255
                else:
                    self.img_PIL[pos_y-self.MARK_SZ:pos_y+self.MARK_SZ+1,pos_x-self.MARK_SZ:pos_x+self.MARK_SZ+1,0]=0
                    self.img_PIL[pos_y-self.MARK_SZ:pos_y+self.MARK_SZ+1,pos_x-self.MARK_SZ:pos_x+self.MARK_SZ+1,1]=0
                    self.img_PIL[pos_y-self.MARK_SZ:pos_y+self.MARK_SZ+1,pos_x-self.MARK_SZ:pos_x+self.MARK_SZ+1,2]=255
                    
            lng = self.data_list[n0][0]
            lat = self.data_list[n0][1]

            lng0,lat0=lng-self.lng_min,lat-self.lat_min
            pos_x = int(round(lng0/self.MAP_X_SCALE))
            pos_y = self.MAP_HGT + int(round(lat0/self.MAP_Y_SCALE))
            self.img_PIL[pos_y-self.MARK_SZ:pos_y+self.MARK_SZ+1,pos_x-self.MARK_SZ:pos_x+self.MARK_SZ+1,0]=255
            self.img_PIL[pos_y-self.MARK_SZ:pos_y+self.MARK_SZ+1,pos_x-self.MARK_SZ:pos_x+self.MARK_SZ+1,1]=0
            self.img_PIL[pos_y-self.MARK_SZ:pos_y+self.MARK_SZ+1,pos_x-self.MARK_SZ:pos_x+self.MARK_SZ+1,2]=0
            
            #每次清空显示，重新画
            plt.clf()
    #         self.point = plt.axes([0.3,0.03,0.1,0.03])
    #         self.button = Button(self.point, "delete")
    #         self.button.on_clicked(self.button_press)
    
            point1 = plt.axes([0.3,0.03,0.1,0.03])
            button1 = Button(point1, "select into delete list")
            point2 = plt.axes([0.5,0.03,0.1,0.03])
            button2 = Button(point2, "delete all photos in list")
            point3 = plt.axes([0.7,0.03,0.1,0.03])
            button3 = Button(point3, "recover from delete list")

            plt.subplot(121)
            plt.imshow(self.img_PIL)
            plt.title('Click map to choose point')
            #img = Image.open(self.flist[n0])
            img = mpimg.imread(self.flist[n0])
            plt.subplot(122)
            plt.imshow(img)
            plt.title('select file:'+self.flist[n0])
            plt.draw()
            plt.show()

 
        
def getPictures(image_dir =''):
    if(image_dir == ''):
        dir = os.getcwd()
    else:
        dir = image_dir
    flist=[]
    flistPath = []
    gps_list= []
    
    flistTmp = os.listdir(dir)
    for file in flistTmp:
        postfix=os.path.splitext(file)[1]
        if(postfix == '.jpg' or postfix == '.JPG'):
            flist.append(file)
            flistPath.append(dir+'/'+file)
            
    flist.sort(key = lambda x:str(x[:-4]))
    flistPath.sort(key = lambda x:str(x[:-4]))

    for filename in flist:
        try:
            image=Image.open(filename)
            for orientation in ExifTags.TAGS.keys():
                if ExifTags.TAGS[orientation]=='Orientation':
                    break
            exif=dict(image._getexif().items())

            if exif[orientation] == 3:
                image=image.rotate(180, expand=True)
            elif exif[orientation] == 6:
                image=image.rotate(270, expand=True)
            elif exif[orientation] == 8:
                image=image.rotate(90, expand=True)
            image.save(filename)
            image.close()

        except (AttributeError, KeyError, IndexError):
            # cases: image don't have getexif
            pass
    count = 0
    for filename in flist:
        splitFileName = filename.split('_')
        lng = float(splitFileName[1][3:])+(121.440107-121.429)
        lat = float(splitFileName[2][3:])+(31.032808-31.028433)
        flag = int(splitFileName[3][0])
        gps_list.append([lng,lat,flag])
        count = count+1
  
    Map = MapShow(gps_list,flistPath,dir)
    Map.drawAllData()

sys.setrecursionlimit(1000000)
getPictures()
    