#!/your/absolute/path/personality-venv/bin/python

import pandas as pd
import numpy as np
import seaborn as sns
import ast
import json
from scipy.stats import spearmanr
import matplotlib.pyplot as plt
import re
import emojis
from itertools import product
from visualizations import create_heatmap
from demoji import convert_emojis2names


# Calculate correlation between top 30  emojis and personality types

def personality_emoji_correlations(personality_series, emoji_series, top_list):
    #filter correlation_df for most frequently used emojis
    columns = top_list
    df_top = pd.DataFrame(columns = columns)
    for row in emoji_series:
        # filter out non top entries + assign each emojis its own column
        row = ast.literal_eval(row)
        row = dict(filter(lambda el: el[0] in top_list, row))
        df_top = df_top.append(row, ignore_index= True).fillna(0)
        df_corr = pd.concat([personality_series, df_top], axis = 1)
    
    # calculate correlation (scipy; spearmanr)
    rho = df_corr.corr(method = lambda x,y: spearmanr(x, y)[0])#.iloc[5:, 0:5] #for correlations with big5 only
    p_val = df_corr.corr(method = lambda x,y: spearmanr(x, y)[1])#.iloc[:, 0:5]
    print(rho, p_val)

    # filter for significant correlations (mask)
    rho_sig = rho.mask(p_val > 0.05, '_')
    p_val = round(p_val, 5)
    #p_val_sig = p_val.mask(p_val > 0.05, '-')

    return rho, rho_sig, p_val #p_val_sig


def emoji_correlations(correlation_df, traits):
    # check if emojis not only correlate with personality traits but also among themselves
    # find all emojis correlating with a given personality trait
    # for each given personality trait create emoji (index, col) pairs
    tuple_dict = {}
    for column in traits:
        indices = correlation_df.index[correlation_df[column] != '_'].tolist()
        indices = list(filter(lambda el : len(el) < 2, indices))
        print(indices)
        tuples = list(product(indices, indices))
        for (i,j) in tuples:
            if i == j:
                tuples.remove((i,j))
        for (i,j) in tuples:
            if (j,i) in tuples:
                tuples.remove((j,i))
        tuple_dict[column] = tuples
    print(tuple_dict)
    # check if emoji pairs correlate 
    dict_new = {}
    for key, value in tuple_dict.items():
        new_values = []
        #value = list(filter(lambda tupel: correlation_df.at[tupel[0], tupel[1]] != '_', value))
        for tupel in value:
            #print(tupel)
            #print(correlation_df.at[tupel[0], tupel[1]])
            if correlation_df.at[tupel[0], tupel[1]] != '_':
                rho = correlation_df.at[tupel[0], tupel[1]]
                new_tupel = (tupel[0], tupel[1], rho)
                new_values.append(new_tupel)
        dict_new[key] = new_values
    print(dict_new)
    return dict_new



if __name__ == '__main__':

    directory = './AnonymizedData/Outputs/'
    correlation_df = pd.read_csv(directory+'dfcomplete.csv', encoding = 'utf-8-sig', sep =';')

    # column names: name;num_emoji;emoji_per_post;unique_emoji;mean_caption_length;total_caption_length;
    #               unique_emojis;unique_emoji_names;emoji_freq;emoji_name_freq;emoji_percentage;emoji_per_cap;
    #               agreeableness;conscientiousness;extraversion;neuroticism;openness

    emoji_data = correlation_df['emoji_percentage']
    #emoji_data_names = correlation_df['emoji_name_freq']
    bigFive_data = correlation_df[['agreeableness', 'conscientiousness', 'extraversion', 'neuroticism', 'openness']]

    # load top emoji jsons
    with open(directory+'top100EmojisPerc.json', encoding='utf-8-sig') as f: # top100
        top_emojis = json.load(f)

    #with open(directory+'top30NameEmojisAbs.json', encoding='utf-8-sig') as f: # top30names -> label
        #top_names = json.load(f)

    top_emojis = list(top_emojis.keys())[:30]
    #top_names = list(top_names.keys())

    emoji_names = convert_emojis2names(top_emojis)

    rho, rho_sig, p_val, p_val_sig = personality_emoji_correlations(bigFive_data, emoji_data, top_emojis)
    #rho_sig.to_csv(directory+'SignificantSpearmanEmojiAbsFreqCorr.csv', encoding='utf-8-sig', sep=';', index = True)
    #p_val_sig.to_csv(directory+'pValuesEmojiAbsFreqCorr.csv', encoding='utf-8-sig', sep=';', index = True)

    create_heatmap(rho, emoji_names)


    #directory = './PersonalityData/EmojiDataframes/'
    #correlation_df = pd.read_csv(directory+'SignificantSpearmanEmojiPercentageCorr.csv', encoding = 'utf-8-sig', sep =';', index_col=0)
    traits = rho_sig.columns[:5].tolist()
    intercorrs = emoji_correlations(rho_sig, traits)
    with open('./AnonymizedData/Outputs/EmojiIntercorrelations.json', 'w', encoding='utf-8-sig') as jf:
        json.dump(intercorrs, jf, indent = 4, ensure_ascii=False)









