import json
import os
import emojis
import re

directory= './PersonalityData/EmojiDataframes/'


with open(directory+'top100Emojis.json', encoding='utf-8-sig') as f: # top100
    top_emojis = json.load(f)

emojiList = list(top_emojis.keys())[:30]
print(emojiList)

names_list = []
for emoji in emojiList:
    demoji = emojis.decode(emoji)
    #print(demoji)
    name = re.findall(':(.*?):', demoji)
    if not name:
        name = ['black_small_square']
    print(name)
    names_list.append(name[0])

print(names_list)