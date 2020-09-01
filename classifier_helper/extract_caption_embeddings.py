import emoji
import re
import pandas as pd
import flair
from advertools import extract_emoji
import numpy as np

import gensim.models as gsm

from flair.embeddings import WordEmbeddings, DocumentPoolEmbeddings
from flair.embeddings import TransformerWordEmbeddings
from flair.data import Sentence


import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.preprocessing.sequence import pad_sequences


# extract emojis from captions
# filter for significant emojis (?)
# clean captions
# embed captions

#fastText_emb = FastTextEmbeddings('https://dl.fbaipublicfiles.com/fasttext/vectors-crawl/cc.en.300.bin.gz', use_local=False) # too big
#https://dl.fbaipublicfiles.com/fasttext/vectors-english/wiki-news-300d-1M-subword.vec.zip # too big
#glove_emb = WordEmbeddings('twitter') # 'glove' # not available at the moment
#document_emb = DocumentPoolEmbeddings([glove_emb])

def get_emojis(caption):
    emoji_summary = extract_emoji([caption])
    emoji_list = emoji_summary['emoji'][0] # emoji_text
    #print(emoji_list, len(emoji_list))
    #emoji_set = np.unique(emoji_list)
    #clean_emojis = [re.sub(r'\*?', '', emoji_string) for emoji_string in emoji_set]
    #emoji_set = list(filter(lambda x: len(x) == 1, emoji_set))
    # clean_emojis = [re.sub('[@#$%^&*+:]', '', emoji_string) for emoji_string in emoji_list]
    # print(clean_emojis)
    # emoji_set = np.unique(clean_emojis)
    # emoji_set = ' '.join(emoji_set)
    return emoji_list

def clean_caption(caption):
    #print(caption)
    # clean_caption = [word for word in caption.split() if word.isalpha()] # words only
    # print(len(clean_caption))
    # clean_caption = ' '.join(clean_caption)
    # print(caption)
    clean_caption = re.sub(emoji.get_emoji_regexp(), r'', caption) # remove all emojis
    clean_caption = re.sub('⠀', '', clean_caption) # remove unknown spaces symbol; keep punctuation (?)
    clean_caption = re.sub('[0-9]', '', clean_caption) # remove numbers
    clean_caption = re.sub('[@#$%^&*+-:]', '', clean_caption)
    # print(clean_caption)
    return clean_caption

def get_text_embedding(clean_caption, embedding_model):
    embeddings_array = []
    sentence = Sentence(clean_caption) # may also take more than one sentence
    embedding_model.embed(sentence) # outputs tensor object
    #print(sentence, type(sentence))
    embeddings_array.append([t.embedding.numpy() for t in sentence]) # embeddings_array = np.array([....])
    #embeddings_array = np.expand_dims(embeddings_array, axis=0) # new
    #print(embeddings_array)
    return embeddings_array

def get_emoji_embeddings(emoji_list, model):
    #embeddings = np.array([model[emoji[0]] for emoji in emoji_list])
    embeddings = []
    for emoji in emoji_list:
        try:
            emb = model[emoji]
            embeddings.append(emb)
        except:
            pass
    #embeddings = np.array(embeddings)
    embeddings_array = np.expand_dims(embeddings, axis=0) 
    #print(embeddings_array.shape)
    return embeddings_array

def pad_embeddings(embeddings_array, max_length):
    padded_array = pad_sequences(embeddings_array, padding = 'post', dtype = 'float32', truncating = 'post', maxlen = max_length)
    return padded_array



if __name__ == '__main__':

    test_dir = '../Insta_pics/instagram-scrapper/abcdefghijkleila_/abcdefghijkleila_.csv'
    columns = ['person_id', 'image_id', 'caption']
    data = pd.read_csv(test_dir, sep = ";", header = None, names = columns, encoding = 'utf-8-sig')

    transformer_model = TransformerWordEmbeddings('bert-base-uncased', layers = '-1') #for BERT # 
    emoji_model = gsm.KeyedVectors.load_word2vec_format('./emoji2vec.bin', binary=True)

    captions = data['caption'][:4]

    emoji_array = []
    text_array = []

    for cap in captions:
        emoji_list = get_emojis(cap)
        print(emoji_list)
        emoji_embeddings = get_emoji_embeddings(emoji_list, emoji_model)
        emoji_array.extend(emoji_embeddings)

        clean_cap = clean_caption(cap)
        embedding = get_text_embedding(clean_cap, transformer_model) # yields embeddings of 768 dims
        print(np.array(embedding).shape)
        text_array.extend(embedding)
    
    padded = pad_embeddings(text_array, max_length = 350)
    print(padded.shape)
    padded_emojis = pad_embeddings(emoji_array, max_length = 35)
    print(padded_emojis.shape)