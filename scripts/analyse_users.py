import pandas as pd
import emoji
import emoji_data_python
from collections import Counter
import regex

users = pd.read_csv("users.csv", engine='c', lineterminator='\n')
em = list(emoji.UNICODE_EMOJI)
em.sort(key=len, reverse=True)

def text_has_emoji(text):
    for e in em:
        if e in text:
            return True
    return False

def get_emoji(text, fast=True):
    if fast:
        s = set()
        t = text
        for e in em:
            if e in t:
                s.add(e)
                t = t.replace(e, '')
        return s
    #return regex.findall(r'\X', text)
    return emoji_data_python.get_emoji_regex().findall(text)

name_emoji = [get_emoji(str(x)) for x in users["name"] if x]
desc_emoji = [get_emoji(str(x)) for x in users["description"] if x]
c = Counter()
for e in name_emoji:
    for emo in e:
        c[emo] += 1
print(c.most_common(10))
