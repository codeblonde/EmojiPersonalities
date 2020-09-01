import pandas as pd
import numpy as np
import glob
import os
import json

from extract_img_embeddings import process_img, get_embedding, save_compressed_dataset
from extract_caption_embeddings import get_emojis, clean_caption, get_text_embedding, get_emoji_embeddings, pad_embeddings

from tensorflow.keras.applications.xception import Xception
import gensim.models as gsm
from flair.embeddings import WordEmbeddings
from flair.embeddings import TransformerWordEmbeddings

# transform personality traits into binary markers
# use csv file to extract all images and captions (+ labels)


def to_binary(score):
    if score >= 50:
        score = 1
    else:
        score = 0
    return score

def transform_labels(liwc_dir, username):
    with open(liwc_dir+username+'liwc.json', encoding='utf-8-sig') as jf:
            data = json.load(jf)
    scores = data['receptiviti_scores']['percentiles'] #['raw_scores']
    big_five = list(scores.items())[:5]
    print(big_five)
    # openness, conscientiousness, extraversion, agreeableness, neuroticism
    categorical_scores = list(map(lambda x: to_binary(x[1]), big_five))
    return categorical_scores


def create_dataset(directory, word_model, emoji_model, img_model, required_size, liwc_dir):

    text_embeddings_array = []
    emoji_embeddings_array = []
    img_embeddings_array = []
    label_array = []

    for path in glob.glob(directory):
        # load csv
        columns = ['person_id', 'image_id', 'caption']
        data = pd.read_csv(path, sep = ";", header = None, names = columns, encoding = 'utf-8-sig')

        username = data['person_id'][0]
        image_ids = data['image_id']
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
            emoji_embeddings_array.extend(emoji_embeddings) # extend; expand dim before using extend?

        # preprocess images
        print('Preparing images ...')
        for img in image_ids:
            processed_image = process_img(img_path+'/'+img, required_size)
            img_embedding = get_embedding(img_model, processed_image)
            img_embeddings_array.extend(img_embedding)

        # transform labels into binary / categorical values (multi-class output vector)
        print('Transforming labels ...')
        labels = transform_labels(liwc_dir, username) 
        label_vec = [labels] * len(image_ids)
        label_array.extend(label_vec)
        #print(np.array(label_array).shape)

    # pad sequences
    padded_text_embeddings = pad_embeddings(text_embeddings_array, max_length = 350)
    padded_emoji_embeddings = pad_embeddings(emoji_embeddings_array, max_length = 30)

    #print(padded_emoji_embeddings.shape)
    #print(padded_text_embeddings.shape)

    return padded_text_embeddings, padded_emoji_embeddings, img_embeddings_array, label_array
    

if __name__ == '__main__':

    test_dir = '../Insta_pics/instagram-scrapper/abcdefghijkleila_/abcdefghijkleila_.csv'

    directory = '../Insta_pics/instagram-scrapper/*/*.csv'
    liwc_dir = './PersonalityData/OriginalData/LIWCJson/'

    required_size = (299, 299)

    img_model = Xception(weights='imagenet', include_top = False)
    transformer_model = TransformerWordEmbeddings('bert-base-uncased', layers = '-1')  
    emoji_model = gsm.KeyedVectors.load_word2vec_format('./emoji2vec.bin', binary=True)


    #X_text, X_emoji, X_img, Y = list(), list(), list(), list()

    #for csv_file in glob.glob(directory):
    padded_text_embeddings, padded_emoji_embeddings, img_embeddings_array, label_array = create_dataset(directory, 
                                                                                        transformer_model, emoji_model, img_model, 
                                                                                        required_size, liwc_dir)

    print(padded_text_embeddings.shape)
    print(padded_emoji_embeddings.shape)
    print(np.array(img_embeddings_array).shape)
    print(np.array(label_array).shape)
    
    np.savez_compressed('./PersonalityData/instagram_dataset.npz', padded_text_embeddings, padded_emoji_embeddings, img_embeddings_array, label_array)