import os, requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("TMDB_API_KEY")
API_BASE = "https://api.themoviedb.org/3"

def call(endpoint, params = None):
    params = params or {} #create params dictionary 
    params["api_key"] = API_KEY
    url = f"{API_BASE}{endpoint}" #create url
    resp = requests.get(url, params=params, timeout=10) #send a get request
    resp.raise_for_status() #raise error on invalid url
    return resp.json()
