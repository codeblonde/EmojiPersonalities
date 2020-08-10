import os
import glob
import pandas as pd
import numpy as np
import emoji
import re

# Preprocessing of Captions to fit Receptiviti API
# Concatenate all Captions of an individual + remove all Emojis
# Max Text Length: 10.000 words

# Read data
directory_in = './PersonalityData/OriginalData/'
directory_out = './PersonalityData/TextOnly/'
sub_dir_clean = 'clean'
sub_dir_short = 'short'
columns = ['person_id', 'image_id', 'caption']


def clean_texts(path):
    '''Remove all emojis from captions for general preprocessing,then combine and cut to 10.000 tokens to fit Receptiviti API maximum requirements'''
    # TODO: get individual captions for later use!
    data = pd.read_csv(path, sep = ";", header = None, names = columns, encoding = 'utf-8-sig')
    text_list = list(data['caption'])
    text = ''.join(text_list)
    
    clean_text = re.sub(emoji.get_emoji_regexp(), r'', text) # remove all emojis
    clean_text = re.sub('⠀', r'', clean_text) # remove unknown spaces symbol
    clean_text = re.sub('\n', r'', clean_text)
    short_text = clean_text.split(' ')
    short_text = short_text[:10000] # adapt to LIWC word limit
    short_text = ' '.join(short_text)
    
    return clean_text, short_text

def save_to_txt(text, path, output_directory, subdir_name): 
    #for path in glob.glob(input_directory+'*'+file_extension):
        # clean and cut captions
        #clean_text, short_text = clean_texts(path)
        # get filename + remove file extension
    name = os.path.split(path)[1]
    name = os.path.splitext(name)[0]
        # create sub directories to organize new files in
    directory_new = os.path.join(output_directory,subdir_name) # global var or in config file
        #directory_short = os.path.join(output_directory,subdir_name)
    if os.path.exists(directory_new) == False:
        os.mkdir(directory_new)
        print('Creating new Directory: %s' %directory_new)
        # if os.path.exists(directory_short) == False:
        #     os.mkdir(directory_short)
        #     print('Creating new Directory: %s' %directory_short)
    print('Currently processing: %s' %name)  
        # save new files
    with open(directory_new+'/'+name+subdir_name+'.txt', 'w+') as f:
        f.write(text)
            #f.close()
        # with open(directory_short+'/'+name+sub_dir_short+'_stxt', 'w+') as f:
        #     f.write(short_text)
            #f.close()
    

def main(input_directory, output_directory):
    for path in glob.glob(input_directory+'*.csv'):
        clean_text, short_text = clean_texts(path)
        save_to_txt(clean_text, path, output_directory, subdir_name='cleaned')
        save_to_txt(short_text, path, output_directory, subdir_name='shortened')


if __name__ == '__main__':
    main(directory_in, directory_out)




