#!/your/absolute/path/personality-venv/bin/python


import pandas as pd
import numpy as np
import seaborn as sns
import ast
import json
import matplotlib.pyplot as plt

'''
Create a boxplot showing the mean and std scores of each personality trait among the dataset.

Create a heatmap for the calculated correlations between personality traits + emoji occurences.
'''

def create_boxplot(personality_data):
    sns.set(style = 'whitegrid')
    f, ax = plt.subplots(figsize = (10, 8))
    ax.set(xlabel= 'Big Personality Trait', ylabel = 'Score in Percentiles', ylim = (0, 100))
    
    sns.boxplot(data = personality_data, palette= 'vlag', width = 0.7).set_title('Personality Trait Scores')
    plt.show()


def create_heatmap(correlation_df, emoji_names, threshold=0.2):
    # correlation heat map
    # labels
    labels = list(correlation_df.head())[:5] + emoji_names # personality trait labels + emoji names
    #print(labels)
    # set values close to 0 to 0 to improve readability
    correlation_df[correlation_df.isin(np.arange(-threshold, threshold))] = 0
    # mask to show only bottom half of map
    mask = np.zeros_like(correlation_df, dtype = np.bool)
    mask[np.triu_indices_from(mask)] = True
    # plot
    f, ax = plt.subplots(figsize = (10, 8))
    sns.heatmap(correlation_df, ax = ax, cmap = 'YlGnBu', linewidths = 0.1, vmin = -1, vmax = 1, mask = mask, xticklabels = labels, yticklabels = labels).set_title('Emoji Frequency Correlation Heatmap')
    #plt.savefig('./PersonalityData/Anonymous/Outputs/correlationHeatmap.png')
    plt.show()

if __name__ == '__main__':

    directory = './AnonymizedData/Outputs/'

    data = pd.read_csv(directory+'dfcomplete.csv', encoding = 'utf-8-sig', sep =';')
    bigFive_data = data[['agreeableness', 'conscientiousness', 'extraversion', 'neuroticism', 'openness']]

    create_boxplot(bigFive_data)