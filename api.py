import requests

def get_score(state):
    url = f"https://api.w1111am.xyz:8443/get_score?state={state}"
    response = requests.get(url)
    data = response.json()
    if 'error' in data:
        return "State not found"
    # example response {'Environmental Score': 0.8799876675480947, 'State': 'West Virginia'}
    # return ENV score
    return data['Environmental Score']
