import configparser
import time
import math

from twython import Twython
import pandas as pd
# from secret import *

def get_api(keynum):
    config = configparser.ConfigParser()
    config.read('twitter' + str(keynum) + '.cfg')
    return Twython(config["default"]["consumerKey"],
                  config["default"]["consumerSecret"],
                  config["default"]["accessToken"],
                  config["default"]["accessTokenSecret"])



if __name__ == '__main__':
    df = pd.read_csv("../data/results.csv", encoding="utf-8")
    apis = [get_api(i) for i in range(2)]
    try:
        for i, row in df.iloc[[162 ,1082,1318,1532,1542,1600,1778]].iterrows():
            api = apis[i % len(apis)]
            uid = int(row["id"])
            if type(row["followers"]) is str:
                print("Skipping", uid)
                continue
            print(i, "Getting followers/following for", uid)
            try:
                followers = api.get_followers_ids(user_id=uid)
                following = api.get_friends_ids(user_id=uid)
            except Exception as e:
                print("failed:", e)
                continue
            finally:
                time.sleep(math.ceil(60 / len(apis))+5)
            df.loc[i,"followers"] = ",".join(str(f) for f in followers["ids"])
            df.loc[i,"following"] = ",".join(str(f) for f in following["ids"])
    finally:
        # print(df)
        df.to_csv("../data/results.csv", index=False)
        # print(dir(api))
