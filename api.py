import requests
import pandas as pd

df = pd.read_csv('temperatures.csv', header=None, names=['County', 'State'])
df2 = pd.read_csv('uscounties.csv', header=None, names=['County', 'State', 'Latitude', 'Longitude'])

def get_score(state):
    url = f"https://api.w1111am.xyz:8443/get_score?state={state}"
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
