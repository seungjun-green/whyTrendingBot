import tweepy
import Twitter
import Brain
import re
import settings
import keys
import tweepy as twitter


auth = twitter.OAuthHandler(keys.consumer_key, keys.consumer_secret)
auth.set_access_token(keys.oa_key, keys.oa_secret)
api = twitter.API(auth)

class IDPrinter(twitter.StreamingClient):
    def on_tweet(self, tweet):
        print(f"new tweet: {tweet.text}")
        curr_id = tweet.id
        curr_tweet = api.lookup_statuses(id=[tweet.id])
        isOringal = (curr_tweet[0]._json['in_reply_to_status_id'] is None)

        if isOringal:
            try:
                text = Twitter.construct_conv_order(curr_id)
                if re.search(r'#\w+', text):
                    hashtag = re.match(r'#\w+', text).group(0)
                    print(f"The given hashtag is {hashtag}")
                    result = Brain.why_trending(hashtag)
                else:
                    result = "Please provide a hashtag"
                print(result)
                if settings.production:
                    Twitter.reply(result, curr_id)
            except:
                print("Unknown error happened")
        else:
            pass



if __name__ == '__main__':
    printer = IDPrinter(keys.bearer_token)

    while True:
        try:
            printer.filter()
        except:
            continue
