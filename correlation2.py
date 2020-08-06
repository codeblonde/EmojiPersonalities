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

directory = './PersonalityData/EmojiDataframes/'
data = pd.read_csv(directory+'SignificantSpearmanEmojiPercentageCorr.csv', encoding = 'utf-8-sig', sep =';', index_col=0)

traits = data.columns[:5].tolist()

def emojiCorrelations(dataframe, traits):
    # check if emojis not only correlate with personality traits but also among themselves
    # find all emojis correlating with a given personality trait
    # for each given personality trait create emoji (index, col) pairs
    tuple_dict = {}
    for column in traits:
        indices = data.index[data[column] != '_'].tolist()
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
        #value = list(filter(lambda tupel: data.at[tupel[0], tupel[1]] != '_', value))
        for tupel in value:
            print(tupel)
            print(data.at[tupel[0], tupel[1]])
            if data.at[tupel[0], tupel[1]] != '_':
                rho = data.at[tupel[0], tupel[1]]
                new_tupel = (tupel[0], tupel[1], rho)
                new_values.append(new_tupel)
        dict_new[key] = new_values

    print(dict_new)
    return dict_new

intercorrs = emojiCorrelations(data, traits)
with open('./PersonalityData/EmojiDataframes/EmojiIntercorrelations.json', 'w', encoding='utf-8-sig') as jf:
        json.dump(intercorrs, jf, indent = 4, ensure_ascii=False)