with open("/Users/seungjunlee/Downloads/GetMarketDataKeys.txt") as f:
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
            weather_key = lines[1].replace("\n", "").replace(" ","")