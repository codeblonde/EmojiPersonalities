import pandas as pd
import numpy as np
import seaborn as sns
import ast
import json
import matplotlib.pyplot as plt

directory = './PersonalityData/EmojiDataframes/'
data = pd.read_csv(directory+'dfcomplete.csv', encoding = 'utf-8-sig', sep =';')
bigFive_data = data[['agreeableness', 'conscientiousness', 'extraversion', 'neuroticism', 'openness']]


def create_boxplot(personalityData):
    sns.set(style = 'whitegrid')
    f, ax = plt.subplots(figsize = (10, 8))
    ax.set(xlabel= 'Big Personality Trait', ylabel = 'Score in Percentiles', ylim = (0, 100))
    
    sns.boxplot(data = personalityData, palette= 'vlag', width = 0.7).set_title('Personality Trait Scores')
    plt.show()


def create_heatmap(correlationDf, emojiNames, threshold=0.2):
    # correlation heat map
    # labels
    labels = list(correlationDf.head())[:5] + emojiNames # personality trait labels + emoji names
    print(labels)
    # set values close to 0 to 0 to improve readability
    correlationDf[correlationDf.isin(np.arange(-threshold, threshold))] = 0
    # mask to show only bottom half of map
    mask = np.zeros_like(rho, dtype = np.bool)
    mask[np.triu_indices_from(mask)] = True
    # plot
    f, ax = plt.subplots(figsize = (10, 8))
    sns.heatmap(correlationDf, ax = ax, cmap = 'YlGnBu', linewidths = 0.1, vmin = -1, vmax = 1, mask = mask, xticklabels = labels, yticklabels = labels).set_title('Emoji Frequency Correlation Heatmap')
    plt.show()


create_boxplot(bigFive_data)