#!/your/absolute/path/personality-venv/bin/python


import numpy as np
import glob
import os
import matplotlib.pyplot as plt
import pydot
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, classification_report

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Model
from tensorflow.keras.layers import GlobalMaxPooling1D, GlobalMaxPooling2D, Input, Dense, Flatten, Dropout, concatenate, Conv1D, Conv2D
from tensorflow.keras.utils import plot_model, to_categorical
from tensorflow.keras import optimizers


# input shapes:
# (7600, 350, 768)
# (7600, 30, 300)
# (7600, 10, 10, 2048)
# (7600, 5)


# mixed data / mulit input cnn approach

def prepare_labels(encoder, labels):
    cat_encoded = encoder.transform(labels)
    onehot_encoded = to_categorical(np.array(cat_encoded), num_classes=3)
    return onehot_encoded

def define_model(input_shape_text, input_shape_emoji): #input_shape = embeddings dimensions
    # TODO: adapt filters, add regularizers

    # channel 1 : textual features
    input1 = Input(shape=input_shape_text)
    conv1 = Conv1D(filters = 128, kernel_size = 4, activation = 'relu')(input1)#(embedding1) #filter size 4
    #drop1 = Dropout(0.5)(conv1) # higher drop out = often slower and more consistent learning
    pool1 = GlobalMaxPooling1D()(conv1)
    drop1 = Dropout(0.2)(pool1)
    flat1 = Flatten()(drop1)
    #dense1 = Dense(256, activation = 'relu')

    # channel 2: emoji features
    input2 = Input(shape=input_shape_emoji)
    conv2 = Conv1D(filters = 64, kernel_size = 2, activation = 'relu')(input2)#(embedding2) #filter size 6
    # drop2 = Dropout(0.5)(conv2)
    pool2 = GlobalMaxPooling1D()(conv2)
    drop2 = Dropout(0.2)(pool2)
    flat2 = Flatten()(drop2)
    #d ense2 = Dense(256, activation = 'relu')
    
    # # channel 3: image features
    # input3 = Input(shape=input_shape_img)
    # conv3 = Conv2D(filters = 128, kernel_size = 1, activation = 'relu')(input3) #(embedding3) #filter size 8
    # conv4 = Conv2D(filters = 128, kernel_size = 3, activation = 'relu')(conv3)
    # # drop3 = Dropout(0.5)(input4)
    # pool3 = GlobalMaxPooling2D()(conv4)
    # drop3 = Dropout(0.2)(pool3)
    # flat3 = Flatten()(drop3)
    # #dense3 = Dense(256, activation = 'relu')
    
    # merge + classification layer
    merged = concatenate([flat1, flat2]) 
    dense1 = Dense(128, activation = 'relu')(merged) 
    dropout = Dropout(0.5)(dense1)
    outputs = Dense(3, activation = 'softmax')(dropout)

    model = Model(inputs = [input1, input2], outputs  = outputs)
    # compile
    model.compile(loss = 'categorical_crossentropy', optimizer = optimizers.RMSprop(learning_rate = 0.001), metrics = ['accuracy']) 
    # summary 
    print(model.summary())

    return model


if __name__ == '__main__':

    # input shapes
    input_shape_text = (350, 768)
    input_shape_emoji = (30, 300)
    input_shape_img = (10, 10, 2048)
    
    # load preprocessed data
    data = data = np.load('./AnonymizedData/Outputs/instagram_dataset.npz', allow_pickle=True)
    
    # train test (dev) split
    X_text, x_text, X_emoji, x_emoji, Y_train, y_test = train_test_split(data['arr_0'], data['arr_1'], data['arr_2'], 
                                                                                    test_size = 0.33, random_state = 42)
                                                                                    # X_img, x_img, data['arr_2']

    # separate individual personality dimensions
    # labels openness
    Y_open = Y_train[:, 0]
    y_open = y_test[:, 0]
    # labels conscientiousness
    Y_cons = Y_train[:, 1]
    y_cons = y_test[:, 1]
    # labels extraversion
    Y_extra = Y_train[:, 2]
    y_extra = y_test[:, 2]
    # labels agreeableness
    Y_agree = Y_train[:, 3]
    y_agree = y_test[:, 3]
    # labels neuroticism
    Y_neuro = Y_train[:, -1]
    y_neuro = y_test[:, -1]

    #label enocder
    label_encoder = LabelEncoder()
    label_encoder.fit(Y_neuro)

    # training loop
    for tupel in [(Y_open, y_open), (Y_cons, y_cons), (Y_extra, y_extra), (Y_agree, y_agree), (Y_neuro, y_neuro)]:
        # transform lables for each personality dimension individually
        Y = prepare_labels(label_encoder, tupel[0])
        y = prepare_labels(label_encoder, tupel[1])

        # initiated model
        mixed_data_model = define_model(input_shape_text, input_shape_emoji)
        # start training
        history = mixed_data_model.fit(x = [X_text, X_emoji], y = Y, validation_data = ([x_text, x_emoji], y), shuffle = True, epochs = 10, batch_size = 16)
        
        # model evaluation
        y_hat = mixed_data_model.predict([x_text, x_emoji]) # predictions
        y_hat_rounded = np.argmax(y_hat, axis = 1)
        y_rounded = np.argmax(y, axis = 1) # true labels
        target_names = label_encoder.classes_ # sub-class names
        confusion = confusion_matrix(y_rounded, y_hat_rounded)
        print('Confusion matrix:', confusion)
        report = classification_report(y_rounded, y_hat_rounded)
        print('Classification report:', report)

        # save model for later use
        # 