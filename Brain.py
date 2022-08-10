from nltk.tokenize import word_tokenize, sent_tokenize
import re
import settings
import Twitter
from nltk.corpus import stopwords
stop_words = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"]

def why_trending(hashtag):
    if settings.production == False and settings.use_example:
        cleaned_data = settings.example_data4
    else:
        print("getting raw data")
        raw_data = Twitter.get_top_tweets(hashtag)
        print("Got the raw data")
        if len(raw_data) == 0:
            return "Unavailable"
        print("getting the raw data")
        cleaned_data = process_data(raw_data, hashtag)
        print("Got the clean data")
        # for row in cleaned_data:
        #     print(row)

    print("not getting final data")
    final_data = extract_summary(cleaned_data, hashtag)
    print("we got the final data")
    print("-" * 10)


    top_id = find_top(final_data, cleaned_data)
    print("-" * 10)

    print(top_id)
    return f"This tweet might represent what people are talking about '{hashtag}' at this moment:\nhttps://twitter.com/twitter/status/{top_id}"

def find_top(final_data, cleaned_data):
    global_max = -1
    top_id = 0
    for row in cleaned_data:
        for sentence in sent_tokenize(row['text']):
            if sentence in final_data:
                row['score'] += final_data[sentence]
                if row['score'] > global_max:
                    top_id = row['tweet_id']
                    global_max = row['score']
                else:
                    pass
            else:
                print("This means this sentence is a useless")
                print(f"**{sentence}**")
                pass

    final_result = sorted(cleaned_data, key=lambda i: i['score'], reverse=True)

    print(f"Last result: \n {final_result}")

    return final_result[0]['tweet_id']

def extract_summary(data, hashtag):
    words = []

    seen_text = set()

    for row in data:
        curr_text = re.sub(r'[^(A-Za-z0-9 )]', '', row['text'])
        curr_text = re.sub(r'\(', '', curr_text)
        curr_text = re.sub(r'\)', '', curr_text)
        if curr_text not in seen_text:
            curr = word_tokenize(curr_text.lower())
            words += curr
            seen_text.add(curr_text)
        else:
            pass

    # creating freqTable for every word in the given text, except stop words
    freqTable = dict()
    for word in words:
        if word in stop_words:
            pass
        elif word in freqTable:
            freqTable[word] += 1
        else:
            freqTable[word] = 1

    print(f"Total number of words: {len(words)} \n {words}")
    print(f"The freqTable: \n {sorted(freqTable.items(), key=lambda item: item[1], reverse=True)}" )

    # creating a dictionary to keep the score of each sentence
    sentences = []
    for row in data:
        curr = sent_tokenize(row['text'])

        for sub_curr in curr:
            if sub_curr not in sentences:
                sentences += curr
            else:
                pass

    highest_freq = sorted(freqTable.items(), key=lambda item: item[1], reverse=True)[0][1]

    # sort the freq table
    scoreboard=dict()

    ds = hashtag.split()
    dddd = []
    for d in ds:
        dddd.append(d.lower())

    for sentence in sentences:
        for word, freq in freqTable.items():
            curr_text = re.sub(r'[^(A-Za-z0-9 )]', '', sentence)
            curr_text = re.sub(r'\(', '', curr_text)
            curr_text = re.sub(r'\)', '', curr_text)
            if word in word_tokenize(curr_text.lower()):
                if freq > 1 and word.lower() not in dddd:
                    if sentence in scoreboard:
                        scoreboard[sentence] += freq/highest_freq
                    else:
                        scoreboard[sentence] = freq/highest_freq



    print(f"final data: \n {scoreboard}")
    print("\n\n")

    return scoreboard

def get_textOnly(data):
    text = []
    for i, row in enumerate(data):
        text.append(row['text'])
    return text

def process_data(data, hashtag):
    scoreboard = []

    for i in range(0, len(data)):
        curr_raw = data[i]._json
        curr = {}
        curr['tweet_id'] = curr_raw['id']
        if 'retweeted_status' in curr_raw:
            raw_text = curr_raw['retweeted_status']['full_text']
        else:
            raw_text = curr_raw['full_text']


        processed_text = re.sub(r'RT', "", raw_text)
        processed_text = re.sub(r'@\w+:', "", processed_text)
        processed_text = re.sub(r'@\w+', "", processed_text)
        processed_text = re.sub(r'@:', "", processed_text)
        processed_text = re.sub(r'@', "", processed_text)
        processed_text = re.sub(r'https://t.co/\w+', "", processed_text)
        processed_text = re.sub(r'#\w+', "", processed_text)
        processed_text = re.sub(r'#', "", processed_text)
        processed_text = re.sub(r'\n', "", processed_text)
        processed_text = re.sub(' +', ' ', processed_text)
        processed_text = re.sub(r'\[Feature]', "", processed_text)
        curr['text'] = processed_text.strip()
        curr['score'] = 0

        scoreboard.append(curr)

    # print("cleaned_data: ")
    # print(scoreboard)
    # print("\n\n")

    return scoreboard