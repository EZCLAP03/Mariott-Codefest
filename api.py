import requests
import pandas as pd
import random
from dotenv import load_dotenv
import os
load_dotenv()


df = pd.read_csv('temperatures.csv', header=None, names=['County', 'State'])
df2 = pd.read_csv('uscounties.csv', header=None, names=['County', 'State', 'Latitude', 'Longitude'])

def get_score(state: str):
    """
    Get environmental score for a state, return the score(int)
    """
    url = f"https://api.w1111am.xyz:8443/get_score?state={state}&password={os.getenv('ESG_SECRET_KEY')}"
    response = requests.get(url)
    data = response.json()
    if 'error' in data:
        return "State not found"
    # example response {'Environmental Score': 0.8799876675480947, 'State': 'West Virginia'}
    # return ENV score
    return data['Environmental Score']

def get_county(state): 
    counties = df[df['State'].str.lower() == state.lower()]['County'].tolist()
    return counties    

def get_latitude(county, state): 
    result = df2[(df2['County'].str.lower() == county.lower()) & (df2['State'].str.lower() == state.lower())]
    
    return result['Latitude'].values[0]

def get_longtitude(county, state):
    result = df2[(df2['County'].str.lower() == county.lower()) & (df2['State'].str.lower() == state.lower())]
    return result['Longitude'].values[0]

def get_news(region: str):
    """
    Get bad news for a region, return the url of the first news article
    """
    if(region == ''):
        return "Invalid input for region"
    badNews = ['hurricane', 'tornado', 'earthquake', 'flood', 'wildfire']
    keyword = random.choice(badNews)
    url = f"https://newsapi.org/v2/everything?q={region}%20{keyword}&sortBy=relevancy&apiKey={os.getenv('NEWS_API_KEY')}"
    response = requests.get(url)
    data = response.json()
    if 'error' in data:
        return "Region not found"
    # if no data gain from api
    if data['totalResults'] == 0:
        return "No news found"
    # example response {"status": "ok", "totalResults": 168, "articles": [ { "source": {  "id": null, "name": "The Conversation Africa" }, "author": "Verna Kale, Associate Editor, The Letters of Ernest Hemingway and Associate Research Professor of English, Penn State","title": "Hemingway, after the hurricane","description": "In 1935, a hurricane devastated the Florida Keys, killing over 400 people, many of them World War I veterans. Ernest Hemingway joined the relief efforts – and became enraged at government inaction.","url": "https://theconversation.com/hemingway-after-the-hurricane-241103","urlToImage": "https://images.theconversation.com/files/626545/original/file-20241017-15-5pkmv4.jpg?ixlib=rb-4.1.0&rect=0%2C408%2C3614%2C1807&q=45&auto=format&w=1356&h=668&fit=crop", "publishedAt": "2024-10-18T12:23:20Z","content": "Rescue workers search debris for victims of the Labor Day hurricane of 1935, a Category 5 storm that devastated parts of the Florida Keys. Bettman/Getty Images\r\nThe 2024 hurricane season has been esp… [+6579 chars]"},etc.
    # extract first news article url
    return data['articles'][0]['title'], data['articles'][0]['url']
