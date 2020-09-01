import numpy as np
import glob
import os
import matplotlib.pyplot as plt
import pydot

# from sklearn.pipeline import make_pipeline
# from sklearn.ensemble import StackingClassifier
# from sklearn.linear_model import LogisticRegression
# from sklearn.svm import LinearSVC
# from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Model
from tensorflow.keras.layers import GlobalMaxPooling1D, GlobalMaxPooling2D, Input, Dense, Flatten, Dropout, concatenate
from tensorflow.keras.utils import plot_model, to_categorical
from tensorflow.keras import optimizers


### shapes:
# (7600, 350, 768)
# (7600, 30, 300)
# (7600, 10, 10, 2048)
# (7600, 5)

### work in progress ###

# -> use neural network or linear clf (log reg)? 
# concatenate feature vectors vs concatenate clf results (stacked gen)

## stacked generalization approach

# def stack_predictions(trained_models, predict_list, row):
#     stacked_row = []
#     for i in range(len(trained_models)):
#         prediction = predict_list[i](models[i], row)
#         stacked_row.append(prediction)
#     stacked_row.append(row[-1])
#     result = row[0:len(row)-1] + stacked_row
#     return result

# def stacked_generalization(train, test, model_list):
#     predict_list = [model1_predict, model2_predict]
#     trained_models = []
#     for i in range(len(model_list)):
#         trained_model = model_list[i](train)
#         trained_models.append(trained_model) # trained model?
#     stacked_data = []
#     for row in train:
#         stacked_row = stack_predictions(trained_models, predict_list, row)
#         stacked_data.append(stacked_row)
#     stacked_model = model_x(stacked_data) # final model
#     predictions = []
#     for row in test:
#         stacked_row = stack_predictions(trained_models, predict_list, row)
#         stacked_data.append(stacked_row)
#         prediction = model_x_predict(stacked_model, stacked_row)
#         prediction = round(prediction)
#         predictions.append(prediction)
#     return predictions




## mixed data / mulit input cnn approach



def define_model(input_shape_text, input_shape_emoji):#, input_shape_img): #sequence length, vocab size/embedding dims
    # TODO: adapt filters, etc.
    # channel 1 : textual features
    input1 = Input(shape=input_shape_text)
    #conv1 = Conv1D(filters = 128, kernel_size = 4, activation = 'relu')(inputs1)#(embedding1) #filter size 4
    #drop1 = Dropout(0.5)(conv1) # higher drop out = slower and more consistent learning
    pool1 = GlobalMaxPooling1D()(input1)
    drop1 = Dropout(0.5)(pool1)
    flat1 = Flatten()(drop1)
    #dense1 = Dense(256, activation = 'relu')
    

    # channel 2: emoji features
    input2 = Input(shape=input_shape_emoji)
    #conv2 = Conv1D(filters = 128, kernel_size = 3, activation = 'relu')(inputs2)#(embedding2) #filter size 6
    #drop2 = Dropout(0.5)(conv2)
    pool2 = GlobalMaxPooling1D()(input2)
    drop2 = Dropout(0.5)(pool2)
    flat2 = Flatten()(drop2)
    #dense2 = Dense(256, activation = 'relu')
    
    

    # # channel 3: image features
    # input3 = Input(shape=input_shape_img)
    # #conv3 = Conv2D(filters = 128, kernel_size = 1, activation = 'relu')(inputs3) #(embedding3) #filter size 8
    # #conv4 = Conv2D(filters = 128, kernel_size = 3, activation = 'relu')(inputs3)
    # #drop3 = Dropout(0.5)(input4)
    # pool3 = GlobalMaxPooling2D()(input3)
    # drop3 = Dropout(0.5)(pool3)
    # flat3 = Flatten()(drop3)
    # #dense3 = Dense(256, activation = 'relu')
    

    # merge layer
    merged = concatenate([flat1, flat2])#, flat3]) # vs add layer
    dense1 = Dense(128, activation = 'relu')(merged) #reg!
    dropout = Dropout(0.5)(dense1)
    outputs = Dense(2, activation = 'sigmoid')(dropout) # regularizer slows down learning

    model = Model(inputs = [input1, input2], outputs  = outputs)
    # compile
    model.compile(loss = 'binary_crossentropy', optimizer = optimizers.RMSprop(learning_rate = 0.005), metrics = ['accuracy']) 
    # summary 
    print(model.summary())

    return model


if __name__ == '__main__':

    input_shape_text = (350, 768)
    input_shape_emoji = (30, 300)
    input_shape_img = (10, 10, 2048)

    mixed_data_model = define_model(input_shape_text, input_shape_emoji)#, input_shape_img)
    #plot_model(mixed_data_model, show_shapes = True)

    data = data = np.load('./PersonalityData/instagram_dataset.npz', allow_pickle=True)
    

    X_text, x_text, X_emoji, x_emoji, X_img, x_img, Y_train, y_test = train_test_split(data['arr_0'], data['arr_1'], data['arr_2'], data['arr_3'], 
                                                                                    test_size = 0.33, random_state = 42)

    Y_neuro = to_categorical(Y_train[:, -1], num_classes=2)
    y_neuro = to_categorical(y_test[:, -1], num_classes=2)

    
    history = mixed_data_model.fit(x = [X_text, X_emoji], y = Y_neuro, validation_data = ([x_text, x_emoji], y_neuro), 
                                                                                            shuffle = True, epochs = 10, batch_size = 16)