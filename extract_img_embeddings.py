import numpy as np
import pandas as pd
import PIL
import cv2 as cv
import glob
import tensorflow as tf
import keras
import sklearn
from tf.keras.applications.xception import Xception, preprocess_input
from tf.keras.preprocessing.image import load_image, img_to_array


### Pseudo Code ###

# load model
model = Xception(weights='imagenet', include_top = False)

img_dir = ''
imgs_array = np.array([])

# image preprocessing
for subdir in glob.glob(img_dir):
    # TODO: create label array
    label = subdir
    img = load_image(img, color_mode='rgb', target_size = (299, 299))
    img = img_to_array(img)
    img = np.expand_dims(img, axis=0)
    img = preprocess_input(img)
    imgs_array.append(img)

# get embeddings
embs = model.predict(imgs_array)

# train test split
X_train, X_test, y_train, y_test = train_test_split(X, y)

# save compressed dataset
numpy.savez_compressed('image_dataset.npz', X_train, X_test, y_train, y_test)