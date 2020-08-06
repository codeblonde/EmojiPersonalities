import pandas as pd
import numpy as np
import seaborn as sns
import ast
import json
from scipy.stats import spearmanr
import matplotlib.pyplot as plt
import re
import emojis
from visualizations import create_heatmap
#import pingouin as pg

# Calculate correlation between top 100  emojis and personality types

directory = './PersonalityData/EmojiDataframes/'
data = pd.read_csv(directory+'dfcomplete.csv', encoding = 'utf-8-sig', sep =';')

# column names: name;num_emoji;emoji_per_post;unique_emoji;mean_caption_length;total_caption_length;
#               unique_emojis;unique_emoji_names;emoji_freq;emoji_name_freq;emoji_percentage;emoji_per_cap;
#               agreeableness;conscientiousness;extraversion;neuroticism;openness

emoji_data = data['emoji_percentage']
emoji_data_names = data['emoji_name_freq']
bigFive_data = data[['agreeableness', 'conscientiousness', 'extraversion', 'neuroticism', 'openness']]

# load top emoji jsons
with open(directory+'top100EmojisPerc.json', encoding='utf-8-sig') as f: # top100
    top_emojis = json.load(f)

with open(directory+'top30NameEmojisAbs.json', encoding='utf-8-sig') as f: # top30names -> label
    top_names = json.load(f)

top_emojis = list(top_emojis.keys())[:30]
top_names = list(top_names.keys())

mean_personality = dict(bigFive_data.mean(axis=0))
print(mean_personality)


def convert_emojis2names(top_emojis):
    names_list = []
    for emoji in top_emojis:
        demoji = emojis.decode(emoji)
        #print(demoji)
        name = re.findall(':(.*?):', demoji)
        if not name:
            name = ['black_small_square'] # 1 manual exception
        print(name)
        names_list.append(name[0])
    return names_list


def corr(persDataframe, emojiDataframe, topList):
    #filter data for most frequently used emojis
    columns = topList
    df_top = pd.DataFrame(columns = columns)
    for row in emojiDataframe:
        # filter out non top 100 entries
        row = ast.literal_eval(row)
        row = dict(filter(lambda el: el[0] in topList, row))
        df_top = df_top.append(row, ignore_index= True).fillna(0)
        df_corr = pd.concat([persDataframe, df_top], axis = 1)
    
    # calculate correlation (scipy; spearmanr)
    rho = df_corr.corr(method = lambda x,y: spearmanr(x, y)[0])#.iloc[5:, 0:5] #for correlations with big5 only
    p_val = df_corr.corr(method = lambda x,y: spearmanr(x, y)[1])#.iloc[:, 0:5]
    print(rho, p_val)

    # filter for significant correlations (mask)
    rho_sig = rho.mask(p_val > 0.05, '_')
    p_val = round(p_val, 5)
    p_val_sig = p_val.mask(p_val > 0.05, '-')

    return rho, rho_sig, p_val, p_val_sig






emoji_names = convert_emojis2names(top_emojis)

rho, rho_sig, p_val, p_val_sig = corr(bigFive_data, emoji_data, top_emojis)
#rho_sig.to_csv(directory+'SignificantSpearmanEmojiAbsFreqCorr.csv', encoding='utf-8-sig', sep=';', index = True)
#p_val_sig.to_csv(directory+'pValuesEmojiAbsFreqCorr.csv', encoding='utf-8-sig', sep=';', index = True)

create_heatmap(rho, emoji_names)









