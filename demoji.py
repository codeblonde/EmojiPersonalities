import emojis
import re

# convert unicode emojis to proper names ('demoji')
def convert_emojis2names(top_emojis_list):
    names_list = []
    for emoji in top_emojis_list:
        demoji = emojis.decode(emoji)
        #print(demoji)
        name = re.findall(':(.*?):', demoji)
        if not name:
            name = ['black_small_square'] # 1 manual exception
        #print(name)
        names_list.append(name[0])
    return names_list