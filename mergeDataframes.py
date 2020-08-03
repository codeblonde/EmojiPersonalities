
import pandas as pd
import numpy as np
import json


# TODO: emoji count df -> column = emoji; index = person, row = count
# TODO: normalize / scale /  mean top emoji list?


# columns:
# n emoji # emoji / post # n unique emoji # mean caption length # unique emoji # unique emoji text # u emoji + count # u emoji + count text

directory = './PersonalityData/EmojiDataframes/'

# emoji df
emoji_df = pd.read_csv(directory+'dfemojis.csv', encoding = 'utf-8-sig', sep =';')
personality_df = pd.read_csv(directory+'dfpersonality.csv', encoding = 'utf-8-sig', sep =';')


print(emoji_df.iloc[0])
print(personality_df)

# check for non-matching values before hand
# new_list = [list(set(list1).difference(list2))]
# [list(set(b) - set(a)), list(set(a) - set(b))]
complete_df = pd.merge(emoji_df, personality_df, on='name')
print(complete_df)
complete_df.to_csv(directory+'dfcomplete.csv', encoding='utf-8-sig', sep=';', index = False)

