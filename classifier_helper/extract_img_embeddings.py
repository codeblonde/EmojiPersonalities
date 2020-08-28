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
#from tensorflow.keras.preprocessing.image import load_image, img_to_array


### Pseudo Code ###

# load model
model = Xception(weights='imagenet', include_top = False)

required_size = (299,299)

img_dir = '../Insta_pics/instagram-scrapper/abcdefghijkleila_/*.jpg' #Users/Jana1/Desktop/Forschungsprojekt
img_path = '../Insta_pics/instagram-scrapper/abcdefghijkleila_/abcdefghijkleila_0.jpg'


# image preprocessing


# # get embeddings
def process_img(img_path, required_size):
    name = os.path.split(img_path)[1]
    name = os.path.splitext(name)[0]

    img = tf.keras.preprocessing.image.load_img(img_path, color_mode='rgb', target_size = required_size)
    img_array = tf.keras.preprocessing.image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)

    return img_array, name    

def get_embedding(model, img):
    print('Creating embeddings ... ')
    emb = model.predict(img)
    return emb


def create_dataset(img_dir, required_size):
    imgs_array = []
    labels = []
    for img_path in glob.glob(img_dir):
        # TODO: adapt to subdirs, get subdir names cleverly
        sub_dir = 
        print('Currently processing: %s' %img_path)
        img, name = process_img(img_path, required_size)
        imgs_array.extend(img)
        labels.extend(name)

    print('Found %d samples for %d classes' % (len(imgs_array), len())) 
    return np.asarray(imgs_array), np.asarray(labels)


def save_compressed_dataset(embeddings, labels, output_directory)
    # # train test split
    X_train, X_test, y_train, y_test = train_test_split(embeddings, labels)

    # save compressed dataset
    numpy.savez_compressed(output_directory+'image_dataset.npz', X_train, X_test, y_train, y_test)


imgs_array, labels = create_dataset(img_dir, required_size)
print(imgs_array.shape)

embs = get_embedding(model, imgs_array)
print(embs.shape)

save_compressed_dataset(embs, labels, output_directory)
