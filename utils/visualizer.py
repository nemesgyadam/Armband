import numpy as np
import cv2
from utils.signal import normalize
from scipy.signal import resample

class Visualizer:
    def __init__(self, name='demo', size=(500,500)):
        self.name = name
        self.size = size
        self.EMG_windows_size =  (1600,900)

    def format_value(self, value):
        value *= -1
        value +=1
        value *= self.size[0]/2
        return int(value)

    def draw(self, data):

        img = np.ones((self.size[0],self.size[1],3), dtype=np.uint8)
        img = cv2.line(img, (0,int(self.size[0]/2)), (int(self.size[1]),int(self.size[0]/2)), (0,0,200), 1)
        last_value = self.size[0]//2
        if data.shape[0]!= self.size[1]:
            data = resample(data, self.size[1])
        for i, value in enumerate(data):
        
            value = self.format_value(value)
            img = cv2.line(img, (i-1, int(last_value)), (i, int(value)), (0,200,0), 1)
            last_value = value
        return img

    def show(self, data):
        #print(data.shape)
        img = self.draw(data)
        img = self.border(img)
        cv2.imshow(self.name, img)
        cv2.waitKey(1)

    def border(self, img):
        canvas = np.zeros(img.shape)
        dim = (int(img.shape[0]*0.9), int(img.shape[1]*0.9))
        resized = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
        canvas[int(img.shape[0]*0.05):int(img.shape[0]*0.95), int(img.shape[1]*0.05):int(img.shape[1]*0.95)] =resized 
        return canvas[:img.shape[0],:img.shape[1]]

    def showEMG(self, data, sleep = 1000):
        imgs = []
        for channel in data:
            imgs.append(self.border(self.draw(channel)))
        canvas = np.zeros((1000,2000,3), dtype=np.uint8)
        canvas[:,:] = (200,200,200)

        uper_line = cv2.hconcat([imgs[0], imgs[1], imgs[2], imgs[3]])
        lower_line = cv2.hconcat([imgs[4], imgs[5], imgs[6], imgs[7]])
        all = cv2.vconcat([uper_line, lower_line])

        all = cv2.resize(all, self.EMG_windows_size, interpolation=cv2.INTER_AREA)

        cv2.imshow(self.name, all)
        cv2.waitKey(sleep)

    def showAll(self, data, sleep =1000):
        imgs = []
        for channel in data:
            imgs.append(self.border(self.draw(channel)))
        canvas = np.zeros((1000,2000,3), dtype=np.uint8)
        canvas[:,:] = (100,100,100)

        uper_line = cv2.hconcat([imgs[0], imgs[1], imgs[2], imgs[3], imgs[8]])
        lower_line = cv2.hconcat([imgs[4], imgs[5], imgs[6], imgs[7], imgs[9]])
        all = cv2.vconcat([uper_line, lower_line])

        all = cv2.resize(all, self.EMG_windows_size, interpolation=cv2.INTER_AREA)

        cv2.imshow(self.name, all)
        cv2.waitKey(sleep)


