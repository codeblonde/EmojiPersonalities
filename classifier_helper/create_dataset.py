#!/your/absolute/path/personality-venv/bin/python


import pandas as pd
import numpy as np
import glob
import os
import json

# from extract_img_embeddings import process_img, get_embedding
from extract_caption_embeddings import get_emojis, clean_caption, get_text_embedding, get_emoji_embeddings, pad_embeddings

from tensorflow.keras.applications.xception import Xception
import gensim.models as gsm
from flair.embeddings import WordEmbeddings
from flair.embeddings import TransformerWordEmbeddings

# transform personality traits into categorical markers
# use csv file to extract all images, emojis and captions (+ labels)

def to_cat(score):
    if score >= 65:
        score = 'high'
    elif score <= 35:
        score = 'low'
    else:
        score = 'neutral'
    return score

def transform_labels(liwc_dir, username):
    with open(liwc_dir+username+'liwc.json', encoding='utf-8-sig') as jf:
            data = json.load(jf)
    scores = data['receptiviti_scores']['percentiles'] #['raw_scores']
    big_five = list(scores.items())[:5]
    # print(big_five)
    # openness, conscientiousness, extraversion, agreeableness, neuroticism
    categorical_scores = list(map(lambda x: to_cat(x[1]), big_five))
    return categorical_scores


def create_dataset(directory, word_model, emoji_model, liwc_dir): # img_model, required_size

    text_embeddings_array = []
    emoji_embeddings_array = []
    # img_embeddings_array = []
    label_array = []

    for path in glob.glob(directory):
        # load csv
        columns = ['person_id', 'image_id', 'caption']
        data = pd.read_csv(path, sep = ";", header = None, names = columns, encoding = 'utf-8-sig')

        username = data['person_id'][0]
        # image_ids = data['image_id']
        captions = data['caption']

        print('Currently processing: %s' %username)

        img_path = os.path.split(path)[0]

        # preprocess captions + emojis
        print('Preparing captions ...')
        for cap in captions:
            clean_cap = clean_caption(cap)
            cap_embedding = get_text_embedding(clean_cap, word_model)
            text_embeddings_array.extend(cap_embedding)

            emojis = get_emojis(cap)
            emoji_embeddings = get_emoji_embeddings(emojis, emoji_model)
            emoji_embeddings_array.extend(emoji_embeddings) 

        # # preprocess images
        # print('Preparing images ...')
        # for img in image_ids:
        #     processed_image = process_img(img_path+'/'+img, required_size)
        #     img_embedding = get_embedding(img_model, processed_image)
        #     img_embeddings_array.extend(img_embedding)

        # transform labels into categorical values (multi-class output vector)
        print('Transforming labels ...')
        labels = transform_labels(liwc_dir, username) 
        label_vec = [labels] * len(captions) # ?
        label_array.extend(label_vec)
        

    # pad sequences
    padded_text_embeddings = pad_embeddings(text_embeddings_array, max_length = 350)
    padded_emoji_embeddings = pad_embeddings(emoji_embeddings_array, max_length = 30)

    
    return padded_text_embeddings, padded_emoji_embeddings, label_array #img_embeddings_array
    

if __name__ == '__main__':

    # instagram and liwc data directories
    #directory = '../Insta_pics/instagram-scrapper/*/*.csv'
    directory = 'AnonymizedData/raw_data/*.csv'
    #liwc_dir = './PersonalityData/OriginalData/LIWCJson/'
    liwc_dir = 'AnonymizedData/liwc_data/'

    # load models
    # currently no image data available
    # required_size = (299, 299)
    # img_model = Xception(weights='imagenet', include_top = False)
    transformer_model = TransformerWordEmbeddings('bert-base-uncased', layers = '-1')  
    emoji_model = gsm.KeyedVectors.load_word2vec_format('./emoji2vec.bin', binary=True)

    # pad generated embeddings
    padded_text_embeddings, padded_emoji_embeddings, label_array = create_dataset(directory, 
                                                                                transformer_model, emoji_model, 
                                                                                liwc_dir) #img_embeddings_array, required_size, img_model

    print(padded_text_embeddings.shape)
    print(padded_emoji_embeddings.shape)
    #print(np.array(img_embeddings_array).shape)
    print(np.array(label_array).shape)
    
    np.savez_compressed('./AnonymizedData/Outputs/instagram_dataset.npz', padded_text_embeddings, padded_emoji_embeddings, label_array) #img_embeddings_array