#!/your/absolute/path/personality-venv/bin/python

import numpy as np
import pandas as pd
from PIL import Image
#import cv2 as cv
import glob
import os
import tensorflow as tf
from tensorflow import keras
import sklearn
from tensorflow.keras.applications.xception import Xception, preprocess_input
from tensorflow.keras.preprocessing.image import load_img, img_to_array


# image preprocessing
def process_img(img_path, required_size):
    img = tf.keras.preprocessing.image.load_img(img_path, color_mode='rgb', target_size = required_size)
    img_array = tf.keras.preprocessing.image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)

    return img_array    

# get embedding
def get_embedding(model, img):
    #print('Creating embeddings ... ')
    emb = model.predict(img)
    return emb


if __name__ == '__main__':
    # test image
    test_img_path = '../Insta_pics/instagram-scrapper/user_0/user_0_0.jpg'
    
    # load model
    model = Xception(weights='imagenet', include_top = False)

    required_size = (299,299)

    # create embeddings
    img_array = process_img(test_img_path, required_size)
    embs = get_embedding(model, imgs_array)
    print(embs.shape)