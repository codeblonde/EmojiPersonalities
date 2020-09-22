
#!/your/absolute/path/personality-venv/bin/python

import pandas as pd
import numpy as np
import json

'''
Load extracted emoji and personality data and concatenate into on big dataframe for later analyses.

Emoji dataframe columns:
name;  # emoji ; emoji / post ; # unique emoji ; mean caption length ; unique emoji ; unique emoji text ; u emoji + count ; u emoji + count text

Personality dataframe columns:
name ; [big five trait names]
'''

# check for non-matching values before attempting merge
def check_names(df1, df2):
    names1 = df1['name']
    names2 = df2['name']
    differences = list(set(names1).symmetric_difference(set(names2)))
    # new_list = [list(set(list1).difference(list2))]
    # [list(set(b) - set(a)), list(set(a) - set(b))]
    print('Non-matching name entries:', differences)
    return differences

# merge dataframes + save
def merge_dfs(df1, df2, output_directory):
    complete_df = pd.merge(df1, df2, on='name')
    complete_df.to_csv(output_directory+'dfcomplete.csv', encoding='utf-8-sig', sep=';', index = False)
    return complete_df

if __name__ == '__main__':

    directory = './AnonymizedData/Eutputs/'
    
    emoji_df = pd.read_csv(directory+'dfemojis.csv', encoding = 'utf-8-sig', sep =';')
    personality_df = pd.read_csv(directory+'dfpersonality.csv', encoding = 'utf-8-sig', sep =';')

    name_differences = check_names(emoji_df, personality_df)
    if not name_differences: 
        df_complete = merge_dfs(emoji_df, personality_df, directory)
    

