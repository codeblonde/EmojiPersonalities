import json
import pandas as pd
import glob
import os
import shutil

directory = './PersonalityData/LIWCJson/'
outDirectory = './PersonalityData/Anonymous/'
test = 'abcdefghijkleila_.csv'

names = [name[:-4] for name in os.listdir(directory) if name != '.DS_Store']
anonymes = {name: 'user_'+str(index) for index, name in enumerate(names)}

#with open('./PersonalityData/key.json', 'w', encoding='utf-8-sig') as jf:
        #json.dump(anonymes, jf, indent = 4, ensure_ascii=False)

with open('./PersonalityData/key.json', encoding='utf-8-sig') as jf:
    key = json.load(jf)

columns = ['person_id', 'image_id', 'caption']

def encrypt_instagram_data(inDirectory, key, outDirectory):
    for path in glob.glob(inDirectory+'*'):
        # get filename + remove file extension
        name = os.path.split(path)[1]
        name = os.path.splitext(name)[0]
        # new anonymous name
        anonym = key[name]
        print(name, anonym)
        # load data
        data = pd.read_csv(path, sep = ";", header = None, names = columns, encoding = 'utf-8-sig')
        data_encrypted = data.replace(name, anonym, regex = True)
        print(data_encrypted)

        data_encrypted.to_csv(outDirectory+anonym+'.csv', encoding='utf-8-sig', sep=';', index = False)

def encrypt_liwc_data(inDirectory, key, outDirectory):
    for path in glob.glob(inDirectory+'*'):
        # get filename + remove file extension
        name = os.path.split(path)[1]
        name = os.path.splitext(name)[0]
        name = name[:-4]
        # new anonymous name
        anonym = key[name]
        print(name, anonym)
        # load
        with open(path) as jf:
            data = json.load(jf)
        # rename + save
        with open(outDirectory+anonym+'.json', 'w', encoding='utf-8-sig') as jf:
            json.dump(data, jf, indent = 4, ensure_ascii=False)
        
        


#encryptInstaData(directory, key, outDirectory)

encryptLiwc(directory, key, outDirectory)

#string = 'abc_1'
#print(string.replace('abc', 'd'))