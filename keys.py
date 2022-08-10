file_url = ""

from settings import production

if production:
    file_url = "/home/lsj3285007/WTBkeys.txt"
else:
    file_url = "/Users/seungjunlee/Downloads/GetMarketDataKeys.txt"

with open(file_url) as f:
    for i in range(5):
        lines = f.readline().split("=")
        if i == 0:
            consumer_key = lines[1].replace("\n", "").replace(" ","")
        if i == 1:
            consumer_secret = lines[1].replace("\n", "").replace(" ","")
        if i == 2:
            oa_key = lines[1].replace("\n", "").replace(" ","")
        if i==3:
            oa_secret = lines[1].replace("\n", "").replace(" ","")
        if i==4:
            bearer_token = lines[1].replace("\n", "").replace(" ","")