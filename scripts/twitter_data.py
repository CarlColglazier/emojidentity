import twitter
from secret import *

api = twitter.Api(consumer_key=CONSUMER_KEY,
                  consumer_secret=CONSUMER_SECRET,
                  access_token_key=AT_KEY,
                  access_token_secret=AT_SECRET,
                  sleep_on_rate_limit=True)
