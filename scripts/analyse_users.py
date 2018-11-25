import pandas as pd
import emoji
import emoji_data_python
from collections import Counter
import regex
from scrape_emoji import emoji_list

users = pd.read_csv("users.csv", engine='c', lineterminator='\n')
em = list(emoji_list())
em.sort(key=len, reverse=True)

def text_has_emoji(text):
    for e in em:
        if e in text:
            return True
    return False

def get_emoji(text):
    s = set()
    t = text
    for e in em:
        if e in t:
            s.add(e)
            t = t.replace(e, '')
    return s

name_emoji = [get_emoji(str(x)) for x in users["name"] if x]
desc_emoji = [get_emoji(str(x)) for x in users["description"] if x]
c = Counter()
for e in name_emoji:
    for emo in e:
        c[emo] += 1
print(c.most_common(10))
users["name_emoji"] = name_emoji
users["desc_emoji"] = desc_emoji

#sample = users.sample(1000, random_state=100)
sample = users[users["name_emoji"].str.len() > 0].sample(100, random_state=1000)
"""
emoji_followers = []
total_followers = []
for user_id in list(sample["id"]):
    followers = api.GetFollowers(user_id)
    emoji_followers.append(sum([len(get_emoji(x.name)) > 0 for x in followers]))
    total_followers.append(len(followers))
"""
