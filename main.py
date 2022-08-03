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
    print(printer.get_rules())

    while True:
        try:
            printer.filter()
        except:
            continue

d = {'created_at': 'Wed Aug 03 02:20:55 +0000 2022', 'id': 1554653511870136325, 'id_str': '1554653511870136325', 'text': '@whyTrendingBot jdjdjdis', 'truncated': False, 'entities': {'hashtags': [], 'symbols': [], 'user_mentions': [{'screen_name': 'whyTrendingBot', 'name': 'Why Trending Bot', 'id': 1462979696807710722, 'id_str': '1462979696807710722', 'indices': [0, 15]}], 'urls': []}, 'source': '<a href="http://twitter.com/download/iphone" rel="nofollow">Twitter for iPhone</a>', 'in_reply_to_status_id': None, 'in_reply_to_status_id_str': None, 'in_reply_to_user_id': 1462979696807710722, 'in_reply_to_user_id_str': '1462979696807710722', 'in_reply_to_screen_name': 'whyTrendingBot', 'user': {'id': 1551121430519042049, 'id_str': '1551121430519042049', 'name': 'testing account', 'screen_name': 'PualLacus', 'location': '', 'description': '', 'url': None, 'entities': {'description': {'urls': []}}, 'protected': False, 'followers_count': 0, 'friends_count': 0, 'listed_count': 0, 'created_at': 'Sun Jul 24 08:25:53 +0000 2022', 'favourites_count': 3, 'utc_offset': None, 'time_zone': None, 'geo_enabled': False, 'verified': False, 'statuses_count': 74, 'lang': None, 'contributors_enabled': False, 'is_translator': False, 'is_translation_enabled': False, 'profile_background_color': 'F5F8FA', 'profile_background_image_url': None, 'profile_background_image_url_https': None, 'profile_background_tile': False, 'profile_image_url': 'http://pbs.twimg.com/profile_images/1551121478652899328/Qjgzt1Me_normal.png', 'profile_image_url_https': 'https://pbs.twimg.com/profile_images/1551121478652899328/Qjgzt1Me_normal.png', 'profile_link_color': '1DA1F2', 'profile_sidebar_border_color': 'C0DEED', 'profile_sidebar_fill_color': 'DDEEF6', 'profile_text_color': '333333', 'profile_use_background_image': True, 'has_extended_profile': True, 'default_profile': True, 'default_profile_image': False, 'following': False, 'follow_request_sent': False, 'notifications': False, 'translator_type': 'none', 'withheld_in_countries': []}, 'geo': None, 'coordinates': None, 'place': None, 'contributors': None, 'is_quote_status': False, 'retweet_count': 0, 'favorite_count': 0, 'favorited': False, 'retweeted': False, 'lang': 'ca'}
