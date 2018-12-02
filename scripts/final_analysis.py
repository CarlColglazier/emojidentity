import numpy as np
import pandas as pd
from scipy import stats
from scrape_emoji import emoji_list
from itertools import chain
import math

users = pd.read_csv("../data/users.csv", engine='c', lineterminator='\n')
sample = pd.read_csv("../data/sample.csv")
control = pd.read_csv("../data/control.csv")

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


sample_follower_ids = set(chain.from_iterable([x.split(',') for x in list(sample["followers"]) if type(x) == str]))
control_follower_ids = set(chain.from_iterable([x.split(',') for x in list(control["followers"]) if type(x) == str]))

sample_following_ids = set(chain.from_iterable([x.split(',') for x in list(sample["following"]) if type(x) == str]))
control_following_ids = set(chain.from_iterable([x.split(',') for x in list(control["following"]) if type(x) == str]))

sec = pd.read_csv("../data/second.csv", lineterminator='\n')

sample_followers = sec[sec["id"].isin(sample_follower_ids)]
control_followers = sec[sec["id"].isin(control_follower_ids)]
sample_following = sec[sec["id"].isin(sample_following_ids)]
control_following = sec[sec["id"].isin(control_following_ids)]


emoji_df = pd.DataFrame(0, index=emoji_list(), columns=emoji_list())
sample = sample.merge(users, on="id")
name_emoji = [get_emoji(str(x)) for x in sec["name"]]
sec["id"] = sec["id"].astype("str")
sec["name_emoji"] = name_emoji
for i, row in sample.iterrows():
    if i > 10:
        break
    if not type(row["followers"]) == str:
        continue
    followers = row["followers"].split(',')
    followers_df = sec[sec["id"].isin(list(followers))]
    for value in followers_df["name_emoji"].values:
        for emoji in value:
            c[emoji] += 1
    for e in list(row["name_emoji"]):
        for x, y in c.most_common():
            emoji_df[e][x] += y

elist = [(e, emoji_df[e][e] / emoji_df[e].sum()) for e in emoji_list()]            
print(sorted((filter(lambda x: not math.isnan(x[1]), elist)), key=lambda x: x[1], reverse=True)[0:15])
#
