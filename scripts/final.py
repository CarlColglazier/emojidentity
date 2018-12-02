import numpy as np
import pandas as pd
from scipy import stats
from scrape_emoji import emoji_list
from itertools import chain
import math
import statsmodels
import statsmodels.api as sm
from statsmodels.formula.api import ols
from collections import Counter

users = pd.read_csv("../data/users.csv", engine='c', lineterminator='\n')
original_sample = pd.read_csv("../data/sample.csv")
original_control = pd.read_csv("../data/control.csv")
updated = pd.read_csv("../data/updatedsamplecontrol.csv", lineterminator='\n')

def get_emoji(text):
    s = set()
    t = text
    for e in em:
        if e in t:
            s.add(e)
            t = t.replace(e, '')
    return s

em = list(emoji_list())
em.sort(key=len, reverse=True)

updated["name_emoji"] = [get_emoji(str(x)) for x in updated["name"]]

sample = updated[(updated["name_emoji"].str.len() > 0) & (updated.index.isin(original_sample.index))]
sample = sample.sample(1000, random_state=31415926)

control = updated[(updated["name_emoji"].str.len() == 0) & (updated.index.isin(original_control.index))]
control = control.sample(1000, random_state=31415926)

# Not significant
stats.ttest_ind(control["listed_count"], sample["listed_count"], equal_var=False)


# Significant
stats.ttest_ind(control["followers_count"], sample["followers_count"], equal_var=False)
stats.ttest_ind(control["friends_count"], sample["friends_count"], equal_var=False)


sample["sample"] = True
control["sample"] = False

all_sampled = sample.append(control)
all_sampled["emoji_count"] = [len(x) for x in all_sampled["name_emoji"]]

ols("followers_count~sample:friends_count + friends_count", data=all_sampled).fit().summary()
ols("friends_count~sample*followers_count", data=all_sampled).fit().summary()

emoji_df = pd.DataFrame(0, index=emoji_list(), columns=emoji_list())

sec = pd.read_csv("../data/second.csv", lineterminator='\n')

sample_follower_ids = set(chain.from_iterable([x.split(',') for x in list(sample.merge(original_sample, on="id", how='left')["followers"]) if type(x) == str]))

control_follower_ids = set(chain.from_iterable([x.split(',') for x in list(control.merge(original_control, on="id", how='left')["followers"]) if type(x) == str]))

sample_followers["name_emoji"] = [get_emoji(str(x)) for x in sample_followers["name"]]

c = Counter()
for val in sample_followers["name_emoji"].values:
    for e in val:
        c[e] += 1

c.most_common(10)

control_followers["name_emoji"] = [get_emoji(str(x)) for x in control_followers["name"]]

c_control = Counter()
for val in control_followers["name_emoji"].values:
    for e in val:
        c_control[e] += 1

len(sample_followers[sample_followers["name_emoji"].str.len() > 0]) / len(sample_followers)
len(control_followers[control_followers["name_emoji"].str.len() > 0]) / len(control_followers)

contingency = [[len(control_followers[control_followers["name_emoji"].str.len() > 0]), len(control_followers[control_followers["name_emoji"].str.len() == 0])],[len(sample_followers[sample_followers["name_emoji"].str.len() > 0]), len(sample_followers[sample_followers["name_emoji"].str.len() == 0])]]
stats.fisher_exact(contingency)
