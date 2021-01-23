import datetime

def timeConverter(value):
    return datetime.datetime.fromtimestamp(int(value)).strftime("%Y-%m-%d %H:%M:%S")