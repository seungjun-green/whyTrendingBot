import Twitter
import time
import Brain
import re

if __name__ == '__main__':
    while True:
        try:
            mentions = Twitter.get_replies()
            for i, mention in enumerate(mentions):
                curr_id = mention[0]
                text = Twitter.construct_conv_order(curr_id)
                if re.search(r'#\w+', text):
                    hashtag = re.match(r'#\w+', text).group(0)
                    print(f"The given hashtag is {hashtag}")
                    result = Brain.why_trending(hashtag)
                else:
                    result = "Please provide a hashtag"
                print(result)
                Twitter.reply(result, curr_id)
                if i == 0:
                    Twitter.record["reply"]["lastReplied_id"] = mention[0]
        except:
            Twitter.record["reply"]["firstTime"] = True
            print("unknown error happened")

        time.sleep(15)


