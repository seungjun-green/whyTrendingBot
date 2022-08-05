from nltk.tokenize import word_tokenize, sent_tokenize
import re
import settings
import Twitter
from nltk.corpus import stopwords
stop_words = stopwords.words('english') # why this is trending

def why_trending(hashtag):
    if settings.production:
        raw_data = Twitter.get_top_tweets(hashtag)

        if len(raw_data) == 0:
            return "Unavailable"

        cleaned_data = process_data(raw_data)
    else:
        cleaned_data = settings.example_data2
        for row in cleaned_data:
            print(row)


    final_data = extract_summary(cleaned_data)
    top_id = find_top(final_data, cleaned_data)
    print(top_id)
    return f"This tweet might represent what people are talking about '{hashtag}' at this moment:\nhttps://twitter.com/twitter/status/{top_id}"

def find_top(final_data, cleaned_data):
    count = 0
    for row in cleaned_data:
        for sentence in sent_tokenize(row['text']):
            if sentence in final_data:
                row['score'] += final_data[sentence]
                count+=1
            else:
                print("This means this sentence is a useless")
                print(f"**{sentence}**")
                pass

        if count > 0:
            row['score'] = row['score'] / count

        count = 0

    final_result = sorted(cleaned_data, key=lambda i: i['score'], reverse=True)

    print("\n Last result: ")
    print(final_result)
    print("\n")

    return final_result[0]['tweet_id']

def extract_summary(data):
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

    print(f"Total number of words: {len(words)}")
    print(words)

    print(f"The freqTable: \n {freqTable}" )

    # creating a dictionary to keep the score of each sentence
    sentences = []
    for row in data:
        curr = sent_tokenize(row['text'])

        for sub_curr in curr:
            if sub_curr not in sentences:
                sentences += curr
            else:
                print("나왔다")



    print(f"Total number of sentences: {len(sentences)}, {len(seen_text)}")
    print("===========")
    print(sentences)
    print("===========")
    print(seen_text)
    print("===========")
    print("\n\n")

    highest_freq = sorted(freqTable.items(), key=lambda item: item[1], reverse=True)[0][1]
    print(sorted(freqTable.items(), key=lambda item: item[1], reverse=True))
    print(f"HIGHEST: {highest_freq}")
    # sort the freq table
    scoreboard=dict()
    for sentence in sentences:
        for word, freq in freqTable.items():
            curr_text = re.sub(r'[^(A-Za-z0-9 )]', '', sentence)
            curr_text = re.sub(r'\(', '', curr_text)
            curr_text = re.sub(r'\)', '', curr_text)
            if word in word_tokenize(curr_text.lower()):
                if sentence in scoreboard:
                    scoreboard[sentence] += freq/highest_freq
                else:
                    scoreboard[sentence] = freq/highest_freq




    print("final data: ")
    print(len(scoreboard))
    print(scoreboard)
    print("\n\n")

    return scoreboard

def get_textOnly(data):
    text = []
    for i, row in enumerate(data):
        text.append(row['text'])
    return text

def process_data(data):
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

    print("cleaned_data: ")
    print(scoreboard)
    print("\n\n")

    return scoreboard