import numpy as np
import pandas as pd
import json
import seaborn as sns
import matplotlib.pyplot as plt
import ast

directory = './PersonalityData/EmojiDataframes/'
data = pd.read_csv(directory+'dfemojis.csv', encoding = 'utf-8-sig', sep =';')
#print(data)


#emoji_percentage = data['emoji_percentage']
emoji_freq_name = data['emoji_name_freq']


def get_top_emojis(pdSeries, pathOut, top_n = 100):
    top_emojis = {}
    for row in pdSeries:
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
    print('Saving Json File to: %s' %pathOut)
    with open(pathOut, 'w', encoding='utf-8-sig') as jf:
        json.dump(top_emojis, jf, indent = 4, ensure_ascii=False)

    return top_emojis

top_emojis = get_top_emojis(emoji_freq_name, directory+'top30NameEmojis.json', top_n = 30) # 953 unique emojis
# sorted_emoji_names = create_sorted_dict(emoji_count_names)




# mean values numerical data
#mean_n_emojis = np.mean(data['num_emoji'])
#mean_emojis_post = np.mean(data['emoji_per_post'])
#mean_unique_emoji = np.mean(data['unique_emoji'])
#mean_mean_cap_len = np.mean(data['mean_caption_length'])

# box plots
#sns.boxplot(y = 'unique_emoji', data = data)
#plt.show()

# emoji frequencies (total)
# emoji_count = data['emoji_freq']
# emoji_count_names = data['emoji_name_freq']