import tweepy as twitter
import keys
import re
import settings

record = {
    "reply": {"firstTime": True, "lastReplied_id": 0}
}

auth = twitter.OAuthHandler(keys.consumer_key, keys.consumer_secret)
auth.set_access_token(keys.oa_key, keys.oa_secret)
api = twitter.API(auth)

def reply(result, curr_id):
    api.update_status(status=result, in_reply_to_status_id=curr_id, auto_populate_reply_metadata=True)
    print("reply-tweeted! \n")

def get_top_tweets(hashtag):
    result = api.search_tweets(q=hashtag,tweet_mode='extended',lang = "en" ,count=10)
    return result


def construct_conv_order(tw_id):
    chats = []
    rd = api.get_status(id=tw_id)
    while True:
        try:
            data = rd[0]._json
        except:
            data = rd._json

        text = data['text']

        if re.search(r'#\w+', text):
            return re.findall(r'#\w+', text)[0]
        chats.append(f"{text}")
        parent_id = data['in_reply_to_status_id']
        if parent_id is None:
            break

        rd = api.get_status(id=parent_id)
    # reverse chats
    chats.reverse()
    order = ""
    for chat in chats:
        chat = re.sub('\n', '', chat)
        order += chat
        order += ' '

    order = order.replace('@inshortBot', '')

    print("\n-------start of the order-------")
    print(order)
    print("-------end of the order-------\n")
    return order