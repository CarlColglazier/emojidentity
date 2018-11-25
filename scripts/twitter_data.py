import configparser

import twitter
import pandas as pd
# from secret import *

def get_api():
    config = configparser.ConfigParser()
    config.read('twitter.cfg')
    return twitter.Api(consumer_key=config["default"]["consumerKey"],
                  consumer_secret=config["default"]["consumerSecret"],
                  access_token_key=config["default"]["accessToken"],
                  access_token_secret=config["default"]["accessTokenSecret"],
                  sleep_on_rate_limit=True)

if __name__ == '__main__':
    df = pd.read_csv("../data/emoji_users_201811251616.csv", encoding="utf-8")
    api = get_api()
    for r in df.iterrows():
        print(r)
    # api.get_friends(user_id=132)
    # print(dir(api))

