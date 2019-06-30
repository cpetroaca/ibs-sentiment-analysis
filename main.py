import requests
import json
import os
import yaml
from datamodel import SentimentResult
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from flask import Flask
from flask import request, send_from_directory
from nltk.tokenize import sent_tokenize
from waitress import serve

static_file_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'static')
app = Flask(__name__, static_url_path='', static_folder='static')
config = {}

@app.route('/')
def get_main():
    return send_from_directory(static_file_dir, 'index.html')
    
@app.route('/analyze_sentiment')
def analyze_sentiment():
    global config
    query = request.args.get('query')
    sid = SentimentIntensityAnalyzer()
    r = requests.get(config['reddit.api'] + query)
    posts = json.loads(r.text)['data']
    positive = SentimentResult()
    negative = SentimentResult()
    neutral = SentimentResult()
    for post in posts:
        full_link = post['full_link']
        
        if 'selftext' not in post.keys():
            continue
        
        selftext = post['selftext']
        sentences = sent_tokenize(selftext)
        for i in range(len(sentences)):
            sentence = sentences[i]
            if query in sentence:            
                score = sid.polarity_scores(sentence)['compound']
                post_result = dict()
                post_result['score'] = score
                post_result['text'] = sentence
                post_result['link'] = post['full_link']
                
                if score < -0.05:
                    negative.add_post(post_result)
                elif score > 0.05:
                    positive.add_post(post_result)
                else:
                    neutral.add_post(post_result)
    positive.trim_list()
    negative.trim_list()
    neutral.trim_list()
    
    return '{ "positive":' + json.dumps(positive.__dict__) + ', "negative":' + json.dumps(negative.__dict__) + ', "neutral":' + json.dumps(neutral.__dict__) + '}'

def read_config(config_file):
    global config
    with open(config_file, 'r') as stream:
        try:
            config = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            raise exc

if __name__ == '__main__':
    read_config("config.yaml")
    print(config)
    serve(app, host='0.0.0.0', port=5000)