import json
import pandas as pd
import glob
import os

'''
The LIWC API outputs a comprehensive estimation of over 100 personality traits + emotional tone and offers additional communication advice.
Since this reserach is only interested in the big five traits (openness, extraversion, conscientiousness, neuroticism, agreeableness), these have to be filtered out 
and stored for later use. Scores are given in percentiles as well as raw scores (scale from -5 to 5).
The scope of which traits are to be investigated may be adapted for further analyses.
'''

def create_personality_df(input_directory, output_directory): # save param?
    df_personality = pd.DataFrame()
    # iterate over files in directory
    for path in glob.glob(input_directory+'*.json'):
        # get filename + remove file extension
        name = os.path.split(path)[1]
        name = os.path.splitext(name)[0]#[:-4]
        print('Currently processing %s' %name)
        with open(path, encoding='utf-8-sig') as jf:
            data = json.load(jf)
        scores = data['receptiviti_scores']['percentiles'] #['raw_scores']
        big_five = list(scores.items())[:5] # first 5 traits in summary
        big_five = dict(big_five)
        big_five['name'] = name
        df_personality = df_personality.append(big_five, ignore_index = True)
    names = df_personality.pop('name') # pop and insert at first index
    df_personality.insert(0, names.name, names)
    df_personality.to_csv(output_directory+'dfpersonality_percentiles.csv', encoding='utf-8-sig', sep=';', index = False)
    return df_personality

if __name__ == '__main__':

    directory_in = './PersonalityData/LIWCJson/'
    directory_out= './PersonalityData/EmojiDataframes/'

    df_personality = create_personality_df(directory_in, directory_out)
    print(df_personality)

    #mean_personality = dict(df_personality.mean(axis=0))
    #print(mean_personality)