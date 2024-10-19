import requests

def get_score(state):
    url = f"https://api.w1111am.xyz:8443/get_score?state={state}"
    response = requests.get(url)
    # example response {'Environmental Score': 0.8799876675480947, 'State': 'West Virginia'}
    # return ENV score
    return response.json()['Environmental Score']
