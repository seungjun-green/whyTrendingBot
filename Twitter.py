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

def get_replies():
    replies = []
    if record["reply"]["firstTime"]:
        try:
            rd = api.search_tweets(settings.user_id, count=1)
            print(f"reply-first Time: {len(rd)}")
            for dot in rd:
                replies.append((dot._json['id'], dot._json['text'], dot._json['user']['screen_name']))
            record["reply"]["firstTime"] = False
        except twitter.errors.TweepyException as e:
            print(f"[get_replies] (First time) Twitter Error: {e}\n")
    else:
        try:
            rd = api.search_tweets(settings.user_id, since_id=record["reply"]["lastReplied_id"])
            if (len(rd) > 0):
                print(f"reply-second Time: {len(rd)}")
            for dot in rd:
                replies.append((dot._json['id'], dot._json['text'], dot._json['user']['screen_name']))
        except twitter.errors.TweepyException as e:
            print(f"[get_replies] (Second time) Twitter Error: {e}\n")
    return replies

def reply(result, curr_id):
    api.update_status(status=result, in_reply_to_status_id=curr_id, auto_populate_reply_metadata=True)
    print("reply-tweeted! \n")

def get_top_tweets(hashtag):
    result = api.search_tweets(q=hashtag,tweet_mode='extended', count=15)
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