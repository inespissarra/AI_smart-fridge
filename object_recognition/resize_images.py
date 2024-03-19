## resize images in dataset
import os
import cv2
import numpy as np
import matplotlib.pyplot as plt

# path to the dataset
path = ['dataset/eggs', 'dataset/milk', 'dataset/yogurt', 'dataset/water']

for p in path:
    for img in os.listdir(p):
        img_path = os.path.join(p, img)
        if img_path.endswith('.jpg') or img_path.endswith('.JPG'):
            img_array = cv2.imread(img_path)
            im_height, im_width, _ = img_array.shape
            print(im_height, im_width)
            img_array = cv2.resize(img_array, (int(im_width/8), int(im_height/8)))
            cv2.imwrite(img_path, img_array)
            print(img_path)