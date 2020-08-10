'''
#!/usr/bin/python3.6
or
#!/usr/bin/env python
'''

import sys
import pandas as pd
import json
from merge_dataframes import merge_dfs, check_names
from extract_emoji_data import concatenate_and_save
from extract_personality_data import create_personality_df
from get_top_emojis import get_top_emojis
from demoji import convert_emojis2names
from correlation import personality_emoji_correlations, emoji_correlations
from visualizations import create_boxplot, create_heatmap

'''
Steps:
1. Extract relevant informations about emojis used in instagram captions
1.2 Sort Emojis by percentile occurence and create top n - list
2. Extract big five scores from LIWC output files
3. Create comprehensive dataframe
4. Calculate Correlations between emojis and traits
4.2 Check if emojis correlating with traits also correlate with each other
5. Visulaization
'''


# TODO: what about save params?

def main():
    print('Extracting Emoji Data ...')
    #emoji_df = concatenate_and_save(emoji_dir, output_dir, column_names)
    emoji_df = pd.read_csv('./PersonalityData/Anonymous/Outputs/dfemojis.csv', encoding = 'utf-8-sig', sep =';')
    print(emoji_df)

    print('Sorting Emojis ...')
    emoji_percentages = emoji_df['emoji_percentage']
    top_emojis = get_top_emojis(emoji_percentages, output_dir+'topEmojis.json', top_n = 30)
    print(top_emojis)

    print('Extracting Big Five Data ...')
    personality_df = create_personality_df(personality_dir, output_dir)
    print(personality_df)

    print('Merging Dataframes ...')
    # merge to ensure indices + names match
    naming_difference = check_names(emoji_df, personality_df)
    if not naming_difference:
        complete_df = merge_dfs(emoji_df, personality_df, output_dir)
    else:
        sys.exit('Dataframes could not be merged due to naming incompatibilities.')

    print('Calculating Correlations ...')
    big_five_data = complete_df[['agreeableness', 'conscientiousness', 'extraversion', 'neuroticism', 'openness']]
    emoji_data = complete_df['emoji_percentage']
    # emoji - trait correlations
    rho, rho_sig, p_val = personality_emoji_correlations(big_five_data, emoji_data, top_emojis)
    print('Emoji - Personality Traits Spearman Correlations: \n', rho) 
    print('Correlation p-Values: \n', p_val)
    # emoji - emoji correlations
    personality_traits = rho_sig.columns[:5].tolist()
    emoji_correlations(rho_sig, personality_traits)
    #print('Emoji Correlations: \n', emoji_correlations)
    # save
    rho_sig.to_csv(output_dir+'SignificantSpearmanCorrEmojisTraits.csv', encoding='utf-8-sig', sep=';', index = True)
    p_val.to_csv(output_dir+'pValuesCorrEmojisTraits.csv', encoding='utf-8-sig', sep=';', index = True)

    # visualizations
    emoji_names = convert_emojis2names(top_emojis)
    create_heatmap(rho, emoji_names)

    #return complete_df, top_emojis, rho, rho_sig, p_val

if __name__ == '__main__':

    emoji_dir = './PersonalityData/Anonymous/raw_data/'
    personality_dir = './PersonalityData/Anonymous/liwc_data/'
    output_dir = 'PersonalityData/Anonymous/Outputs/'

    column_names = ['person_id', 'image_id', 'caption'] #(?)

    main()
