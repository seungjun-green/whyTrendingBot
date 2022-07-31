import Twitter
import time
import Brain
import re
import settings


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
                if settings.production:
                    Twitter.reply(result, curr_id)
                if i == 0:
                    Twitter.record["reply"]["lastReplied_id"] = mention[0]
        except:
            Twitter.record["reply"]["firstTime"] = True
            print("unknown error happened")

        time.sleep(15)




# start =  {'hand': 1, 'painted': 1, 'oil': 1, 'painting': 1, 'canvas': 1, ',': 3, 'mountains': 1, 'initial': 1, 'game': 1, 'functions': 1, '-mvp': 1, 'more': 2, 'descriptive': 2, 'error': 4, 'messages': 2, '/': 2, 'logging': 3, 'breakage': 1, 'oh-my-posh': 1, 'due': 1, 'removal': 1, 'of': 4, 'config': 1, 'setting': 1, "'n": 1, 'proto': 1, 'this': 2, 'episode': 2, 'programming': 2, 'with': 2, 'palermo': 2, ':': 3, '.net': 2, '6': 2, 'using': 2, 'onion': 2, 'architecture-': 2, 'part': 2, '2': 2, 'see': 2, 'difference': 2, 'between': 2, 'github': 2, 'actions': 2, '&': 2, 'amp': 2, ';': 2, 'azure': 2, 'pipelines': 2, '@': 7, 'jeffreypalermo': 2, 'structures': 3, 'via': 3, 'sheraj99': 3, 'best': 1, 'websites': 1, 'coding': 1, 'use': 1, 'reporting': 1, 'package': 1, 'generate': 1, 'report': 1, 'oerand': 1, 'install': 1, 'instead': 1, 'so': 1, 'today': 1, 'i': 1, 'graduated': 1, 'from': 1, 'mlh': 1, 'prep': 1, 'fellowship': 1, '(': 1, 'july': 1, 'cohort': 1, ')': 1, 'has': 1, 'been': 1, 'an': 1, 'amazing': 1, 'experience.thanks': 1, 'mlhacks': 1, 'githubyou': 1, 'can': 1, 'read': 1, 'my': 1, 'experience': 1, 'here': 1, 'object': 1, 'prototype': 1, 'boost': 1, 'your': 1, 'productivity': 1, '❤connect': 1}
#
# soted_freq = sorted(start.items(), key=lambda item: item[1], reverse=True)[0][1]
# print(soted_freq)