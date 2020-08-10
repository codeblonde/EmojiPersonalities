## Summary and Soft Statistics of Scraped Personality Data ##
import os
import glob
import pandas as pd
import emojis
import advertools
import re
import numpy as np


'''
Given input in csv files:
Instagram caption posts containing text + emojis, corresponding image ids

Desired output per User:
- length of caption 
- word count 
- overall number of emojis used -> overview
- number of emojis per post -> overview
- n unique emojis -> overview 
- all emojis used  -> emojis flat; emojis flat text
- unique emojis --> unique(emojis flat); unique(emojis flat text); 

Desired output whole Data:
- unique Emojis, 
- emoji frequencies
'''

# extract captions into list
def get_captions_list(path, column_names):
    data = pd.read_csv(path, sep = ";", header = None, names = column_names, encoding = 'utf-8-sig')
    captions = list(data['caption'])
    return captions

# get basic statistical information
def get_numerical_summary(captions):
    emoji_data = advertools.extract_emoji(captions) # dictionary containing unique emojis, emoji frequence, emojis per post etc
    numerical_dict = emoji_data['overview'] # dict: n posts, n emojis, emojis / post, n unique emojis
    numerical_dict.pop('num_posts')
    mean_cap_length = np.mean([len(cap.split(' ')) for cap in captions])
    total_cap_length = sum([len(cap.split(' ')) for cap in captions])
    numerical_dict['mean_caption_length'] = mean_cap_length
    numerical_dict['total_caption_length'] = total_cap_length
    return numerical_dict

# get unqiue emojis and frequencies
def get_emoji_summary(captions):
    emoji_data = advertools.extract_emoji(captions) 
    emoji_list = emoji_data['emoji_flat'] # emojis
    emoji_list_text = emoji_data['emoji_flat_text'] # emojis by name
    unique_emojis = np.unique(emoji_list) # unique emojis
    unique_emojis_text = np.unique(emoji_list_text) # unique emoji names
    freq_emojis = [(emoji, emoji_list.count(emoji)) for emoji in set(emoji_list)] # unqiue emoji + count
    freq_emojis_text = [(emoji, emoji_list_text.count(emoji)) for emoji in set(emoji_list_text)] # unqiue emoji name + count
    # sort max to min
    freq_emojis.sort(key = lambda tupel: tupel[1], reverse = True)
    freq_emojis_text.sort(key = lambda tupel: tupel[1], reverse = True)
    emoji_dict = {'unique_emojis': [unique_emojis], 'unique_emoji_names': [unique_emojis_text], # put variables in list to create single entry
                'emoji_freq': [freq_emojis], 'emoji_name_freq': [freq_emojis_text]}
    return emoji_dict

# store all extracted information in dataframe
def create_summary_df(numerical_dict, emoji_dict): # add param for file extension?
    summary_dict = {**numerical_dict, **emoji_dict}
    emoji_percentage = [(tupel[0], round(tupel[1] / summary_dict['total_caption_length'] * 100, 4)) for tupel in summary_dict['emoji_freq'][0]]
    emoji_per_cap = [(tupel[0], round(tupel[1] /200, 2)) for tupel in summary_dict['emoji_freq'][0]]
    summary_dict['emoji_percentage'] = [emoji_percentage]
    summary_dict['emoji_per_cap'] = [emoji_per_cap]
    summary_df = pd.DataFrame(summary_dict)
    return summary_df

# save to csv file
def concatenate_and_save(input_directory, output_directory, column_names): # save param?
    df_all = pd.DataFrame()
    # iterate over files in directory
    for path in glob.glob(input_directory+'*'):
        # get filename + remove file extension
        name = os.path.split(path)[1]
        name = os.path.splitext(name)[0]
        print('Currently processing: %s' %name)
        ## add name column ##
        captions = get_captions_list(path, column_names)
        numerical_dict = get_numerical_summary(captions)
        emoji_dict = get_emoji_summary(captions)
        summary_df = create_summary_df(numerical_dict, emoji_dict)
        summary_df.insert(0, 'name', name)
        #df_all['name'] = name
        #print(summary_df)
        df_all = df_all.append(summary_df, ignore_index = True)
        # save to csv file    
    df_all.to_csv(output_directory+'dfemojis.csv', encoding='utf-8-sig', sep=';', index = False)
    return df_all

if __name__ == '__main__':
    # Read data
    directory_in = './PersonalityData/OriginalData/'
    directory_out = './PersonalityData/EmojiDataframes/'

    column_names = ['person_id', 'image_id', 'caption']

    df_all = concatenate_and_save(directory_in, directory_out, column_names)
