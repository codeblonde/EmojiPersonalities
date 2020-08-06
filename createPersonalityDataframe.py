import json
import pandas as pd
import glob
import os

inDirectory = './PersonalityData/LIWCJson/'
outDirectory= './PersonalityData/EmojiDataframes/'

def create_personality_df(inputDirectory, outputDirectory): # save param?
    df_personality = pd.DataFrame()
    # iterate over files in directory
    for path in glob.glob(inDirectory+'*.json'):
        # get filename + remove file extension
        name = os.path.split(path)[1]
        name = os.path.splitext(name)[0][:-4]
        #print(path)
        print('Currently processing %s' %name)
        
        with open(path) as jf:
            data = json.load(jf)
        scores = data['receptiviti_scores']['percentiles'] #['raw_scores']
        #print('scores:', scores)
        bigFive = list(scores.items())[:5]
        bigFive = dict(bigFive)
        bigFive['name'] = name
        #print('bigFive', bigFive)
        df_personality = df_personality.append(bigFive, ignore_index = True)
    names = df_personality.pop('name')
    df_personality.insert(0, names.name, names)
    df_personality.to_csv(outputDirectory+'dfpersonality_raw.csv', encoding='utf-8-sig', sep=';', index = False)
    return df_personality

df_personality = create_personality_df(inDirectory, outDirectory)
print(df_personality)

    