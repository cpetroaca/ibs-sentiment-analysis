import requests
import json
import os
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from flask import Flask
from flask import request, url_for

app = Flask(__name__, static_url_path='', static_folder='static')

@app.route('/analyze_sentiment')
def analyze_sentiment():
    query = request.args.get('query')
    sid = SentimentIntensityAnalyzer()
    r = requests.get("https://api.pushshift.io/reddit/search/submission/?subreddit=ibs&q=" + query)
    posts = json.loads(r.text)['data']
    positive = 0
    neutral = 0
    negative = 0
    
    for post in posts:
        full_link = post['full_link']
        selftext = post['selftext']
        score = sid.polarity_scores(selftext)['compound']
        if score < -0.05:
            negative += 1
        elif score > 0.05:
            positive += 1
        else:
            neutral += 1
    return '{ "positive": ' + str(positive) + ', "neutral": ' + str(neutral) + ', "negative": ' + str(negative) + '}'

if __name__ == '__main__':
    app.run()