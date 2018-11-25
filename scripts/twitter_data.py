import configparser

import twitter
import pandas as pd
# from secret import *

def get_api(keynum):
    config = configparser.ConfigParser()
    config.read('twitter' + str(keynum) + '.cfg')
    return twitter.Api(consumer_key=config["default"]["consumerKey"],
                  consumer_secret=config["default"]["consumerSecret"],
                  access_token_key=config["default"]["accessToken"],
                  access_token_secret=config["default"]["accessTokenSecret"],
                  sleep_on_rate_limit=True)


if __name__ == '__main__':
    df = pd.read_csv("../data/emoji_users_201811251616.csv", encoding="utf-8")
    apis = [get_api(i) for i in range(2)]
    try:
        for i, row in df.iterrows():
            api = apis[i % len(apis)]
            uid = int(row["id"])
            print(i, "Getting followers/following for", uid)
            # print(row["id"])
            followers = api.GetFollowers(user_id=uid)
            following = api.GetFriends(user_id=uid)
            df.loc[i,"followers"] = ",".join(str(f.id) for f in followers)
            df.loc[i,"following"] = ",".join(str(f.id) for f in following)
    finally:
        print(df)
        df.to_csv("../data/results.csv", index=False)
        # print(dir(api))

