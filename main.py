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
                text = re.sub(r'@\w+', '', text)
                if len(text) > 0:
                    given_word = text.lstrip()
                    print(f"The given word is {given_word}")
                    result = Brain.why_trending(given_word)

                    if result == "Unavailable":
                        result = "Please provide a proper word or hashtag"
                else:
                    result = "Please provide a proper word or hashtag"

                print(result)

                if settings.production:
                    Twitter.reply(result, curr_id)
                else:
                    print("tweeted - Development mode")

            except:
                print("Unknown error happened")
        else:
            pass



if __name__ == '__main__':
    if settings.production:
        printer = IDPrinter(keys.bearer_token)

        while True:
            try:
                printer.filter()
            except:
                continue
    else:

        print(Brain.why_trending('iPhone 14'))


'''
production mode
- use real data

debugging mode
- using example data
- use real data
'''
