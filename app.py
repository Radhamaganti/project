from flask import Flask, render_template, request
import requests
import base64

app = Flask(__name__)

# API keys (replace with your actual keys)
TMDB_API_KEY = '940c3886755ed6d46291d5415f379996'
NEWS_API_KEY = '7e5e66e9e25e4b2eb38859fafe543461'
SPOTIFY_CLIENT_ID = 'dfd34b53aeae40b5a92897301dc09751'
SPOTIFY_CLIENT_SECRET = '820b8ef73f7940bea3f7e78d4ccb90df'
YOUTUBE_API_KEY = 'AIzaSyClQq1xRP5B2fUiMBb62Ki5vLBw1vB4l-M'
WIKIPEDIA_API_URL = 'https://en.wikipedia.org/w/api.php'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.form['query']
    tmdb_data = search_tmdb(query)
    youtube_data = search_youtube(query)
    news_data = search_news(query)
    spotify_data = search_spotify(query)
    wikipedia_data = search_wikipedia(query)
    return render_template('index.html', query=query, tmdb_data=tmdb_data, youtube_data=youtube_data, news_data=news_data, spotify_data=spotify_data, wikipedia_data=wikipedia_data)

def search_tmdb(query):
    url = f'https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={query}'
    response = requests.get(url)
    return response.json().get('results', [])

def search_youtube(query):
    url = f'https://www.googleapis.com/youtube/v3/search?part=snippet&q={query}&key={YOUTUBE_API_KEY}'
    response = requests.get(url)
    return response.json().get('items', [])

def search_news(query):
    url = f'https://newsapi.org/v2/everything?q={query}&apiKey={NEWS_API_KEY}'
    response = requests.get(url)
    return response.json().get('articles', [])

def get_spotify_token():
    url = 'https://accounts.spotify.com/api/token'
    auth_str = f'{SPOTIFY_CLIENT_ID}:{SPOTIFY_CLIENT_SECRET}'
    b64_auth_str = base64.b64encode(auth_str.encode()).decode()
    headers = {
        'Authorization': f'Basic {b64_auth_str}'
    }
    data = {
        'grant_type': 'client_credentials'
    }
    response = requests.post(url, headers=headers, data=data)
    return response.json().get('access_token')

def search_spotify(query):
    token = get_spotify_token()
    headers = {
        'Authorization': f'Bearer {token}'
    }
    url = f'https://api.spotify.com/v1/search?q={query}&type=track'
    response = requests.get(url, headers=headers)
    return response.json().get('tracks', {}).get('items', [])

def search_wikipedia(query):
    params = {
        'action': 'query',
        'format': 'json',
        'list': 'search',
        'srsearch': query
    }
    response = requests.get(WIKIPEDIA_API_URL, params=params)
    return response.json().get('query', {}).get('search', [])

if __name__ == '__main__':
    app.run(debug=True)
