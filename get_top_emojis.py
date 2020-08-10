import numpy as np
import pandas as pd
import json
import ast

'''
Get a summary of the top used emojis and save as dictionary containing the emojis as key and the emoji's percentile occurence as value.
Sort and save as json.
'''

def get_top_emojis(pd_series, output_path, top_n = 100):
    top_emojis = {}
    for row in pd_series:
        row = ast.literal_eval(row)
        for tupel in row:
            if tupel[0] not in top_emojis.keys():
                top_emojis[tupel[0]] = [tupel[1]]
            else:
                #top_emojis[tupel[0]] = top_emojis[tupel[0]] + tupel[1]
                top_emojis[tupel[0]].append(tupel[1])

    for key, value in top_emojis.items():
        top_emojis[key] = round(sum(value),4) #/ len(value)

    # sort emoji occurences and cut after top n
    top_emojis = sorted(top_emojis.items(), key = lambda pair: pair[1], reverse=True)
    top_emojis = dict(top_emojis[:top_n])
    #print(top_emojis)

    # save to json file
    print('Saving Json File to: %s' %output_path)
    with open(output_path, 'w', encoding='utf-8-sig') as jf:
        json.dump(top_emojis, jf, indent = 4, ensure_ascii=False)

    return top_emojis


if __name__ == '__main__':

    directory = './PersonalityData/Anonymous/Outputs/'
    data = pd.read_csv(directory+'dfemojis.csv', encoding = 'utf-8-sig', sep =';')
    
    emoji_percentage = data['emoji_percentage']
    print(emoji_percentage)
    #emoji_freq_name = data['emoji_name_freq'] #absolute emojis occurences with names

    top_emojis = get_top_emojis(emoji_percentage, directory+'topEmojis.json', top_n = 30) # 953 unique emojis