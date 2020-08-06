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
inDirectory = './PersonalityData/OriginalData/'
outDirectory = './PersonalityData/TextOnly/'
subDirClean = 'clean'
subDirShort = 'short'
columns = ['person_id', 'image_id', 'caption']


def clean_texts(path):
    data = pd.read_csv(path, sep = ";", header = None, names = columns, encoding = 'utf-8-sig')
    textList = list(data['caption'])
    text = ''.join(textList)
    #print('text w emojis:', text)
    cleanText = re.sub(emoji.get_emoji_regexp(), r'', text) # remove all emojis
    cleanText = re.sub('⠀', r'', cleanText) # remove unknown spaces symbol
    cleanText = re.sub('\n', r'', cleanText)
    shortText = cleanText.split(' ')
    shortText = shortText[:10000] # adapt to LIWC word limit
    shortText = ' '.join(shortText)
    #print('text no emojis:', cleanText)
    return cleanText, shortText

def save_to_txt(inputDirectory, outputDirectory, fileExtension='.csv'): # default file extension = .csv
    # iterate over files in directory --> migrate outside of function?
    for path in glob.glob(inputDirectory+'*'+fileExtension):
        # clean and cut captions
        cleanText, shortText = clean_texts(path)
        # get filename + remove file extension
        name = os.path.split(path)[1]
        name = os.path.splitext(name)[0]
        # create sub directories to organize new files in
        cleanDirectory = os.path.join(outputDirectory,subDirClean) # global var or in config file
        shortDirectory = os.path.join(outputDirectory,subDirShort)
        if os.path.exists(cleanDirectory) == False:
            os.mkdir(cleanDirectory)
            print('Creating new Directory: %s' %cleanDirectory)
        if os.path.exists(shortDirectory) == False:
            os.mkdir(shortDirectory)
            print('Creating new Directory: %s' %shortDirectory)
        print('Currently processing: %s' %name)  
        # save new files
        with open(cleanDirectory+'/'+name+subDirClean+'.txt', 'w+') as f:
            f.write(cleanText)
            #f.close()
        with open(shortDirectory+'/'+name+subDirShort+'.txt', 'w+') as f:
            f.write(shortText)
            #f.close()
    

#if name == '__main__':
save_to_txt(inDirectory, outDirectory)




