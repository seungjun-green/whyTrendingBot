import Twitter
import Brain
import re
import settings
import keys
import tweepy as twitter

if __name__ == '__main__':
    class IDPrinter(twitter.StreamingClient):
        def on_tweet(self, tweet):
            print(f"new tweet: {tweet.text}")
            curr_id = tweet.id
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

    printer = IDPrinter(keys.bearer_token)
    print(printer.get_rules())
    printer.filter()