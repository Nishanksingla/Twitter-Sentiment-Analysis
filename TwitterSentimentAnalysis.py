from TwitterAPI import TwitterAPI
from textblob import TextBlob
import plotly.plotly as py
import plotly.graph_objs as go
import geocoder
import sys

consumer_key=""
consumer_secret=""
access_token_key=""
access_token_secret=""
api = TwitterAPI(consumer_key, consumer_secret, access_token_key, access_token_secret)
queryText = sys.argv[1]
location = sys.argv[2]
g = geocoder.google(location)
geocode = [str(i) for i in g.latlng]
geocode.append('40mi')
geocode=','.join(geocode)
searchquery={'q':queryText,
             'result_type':'recent',
             'count':100,
             'include_entities':'false',
             'lang':'en',
             'geocode':geocode
             }
r = api.request('search/tweets', searchquery)
index=1
positiveCount=0
negativeCount=0
neutralCount=0

for item in r:
    sentimentValue = TextBlob(item['text']).sentiment.polarity
    if sentimentValue < 0:
        negativeCount=negativeCount+1
    elif sentimentValue == 0.0:
        neutralCount=neutralCount+1
    elif sentimentValue > 0:
        positiveCount=positiveCount+1

data = [
    go.Bar(
        x=['Negative', 'Neutral', 'Positive'],
        y=[negativeCount, neutralCount, positiveCount]
    )
]
layout = go.Layout(
    title="Query Text = "+queryText+" ; Location = "+location,
)
fig = go.Figure(data=data, layout=layout)
plot_url = py.plot(fig, filename='basic-bar')

    
