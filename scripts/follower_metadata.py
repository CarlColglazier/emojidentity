import pandas as pd
from scipy import stats
from itertools import chain
from secret import *
from twython import Twython
import math
import time
import json

client = Twython(CONSUMER_KEY, CONSUMER_SECRET,
                 AT_KEY, AT_SECRET)


sample = pd.read_csv("../data/sample.csv")
control = pd.read_csv("../data/control.csv")
# Using Welch's t-test because we can't assume equal variance.

# Not significant
stats.ttest_ind(control["followers_count"], sample["followers_count"], equal_var=False)

# Significant
stats.ttest_ind(control["friends_count"], sample["friends_count"], equal_var=False)
stats.ttest_ind(control["listed_count"], sample["listed_count"], equal_var=False)

#all_ids = set(chain.from_iterable([x.split(',') for x in list(sample["followers"]) if type(x) == str])).union(set(chain.from_iterable([x.split(',') for x in list(control["followers"]) if type(x) == str])))
all_ids = set(sample["id"]).union(set(control["id"]))

id_list = list(all_ids)

users = open('samplecontrol120118.txt', 'a')

columns = [
    "id", "name", "screen_name", "description", "followers_count",
    "friends_count", "favorites_count", "listed_count",
    "created_at"
]
for i in range(0, math.ceil(len(id_list) / 100)):
    try:
        ids = id_list[i*100:i*100 + 100]
        response = client.lookup_user(user_id=ids)
        users.writelines([json.dumps({key:value for key, value in x.items() if key in columns})+'\n' for x in response])
        print(i, client.get_lastfunction_header('x-rate-limit-remaining'))
        time.sleep(0.25)
        if int(client.get_lastfunction_header('x-rate-limit-remaining')) < 10:
            t = int(client.get_lastfunction_header('x-rate-limit-reset')) - int(time.time()) + 1
            if t > 0:
                time.sleep(t)
                print("sleeping")
    except:
        print("Error", i, client.get_lastfunction_header('x-rate-limit-remaining'))
        time.sleep(10)
