 
from flask import Flask, render_template, request, redirect
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
import tweepy


app = Flask(__name__)

scheduled_posts = []

TWITTER_API_KEY = 'ZtscmL1VfFFEn97OA89Zv2kdh'
TWITTER_API_SECRET = 'eUPSnPlYSJ7Ty8Xa5btS1M6JUZQtJ6nbho8o3sDBmQdnSCgdEy'
TWITTER_ACCESS_TOKEN = '1745397547181789184-IzgK2T7KF7lcoli45qVEzgfTiz6UbX'
TWITTER_ACCESS_TOKEN_SECRET = 'T9ekbI0vFEDoOVUoPXKKiF9hLSNBbh4WmPaWwwJNSDTTq'

auth = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_SECRET)
auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
twitter_api = tweepy.API(auth)

def fetch_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        soup = BeautifulSoup(response.text, 'html.parser')
        # Placeholder logic for web scraping (replace with actual logic)
        title = soup.title.text if soup.title else 'No title found'
        return f"Data from {url}: {title}"
    except requests.exceptions.RequestException as e:
        raise Exception(f"Error fetching data from {url}: {str(e)}")

def post_to_twitter(content):
    try:
        twitter_api.update_status(status=content)
        print(f"Successfully posted to Twitter: {content}")
    except tweepy.TweepError as e:
        raise Exception(f"Error posting to Twitter: {str(e)}")

def schedule_post(data, scheduled_time):
    scheduler = BackgroundScheduler()
    scheduler.add_job(post_to_twitter, 'date', run_date=scheduled_time, args=[data])
    scheduler.start()

@app.route('/')
def home():
    return render_template('index.html', scheduled_posts=scheduled_posts)

@app.route('/submit', methods=['POST'])
def submit():
    url = request.form.get('url')
    scheduled_time_str = request.form.get('scheduled_time')

    try:
        scheduled_time = datetime.strptime(scheduled_time_str, '%Y-%m-%dT%H:%M')
        data = fetch_data(url)

        scheduled_posts.append({'url': url, 'scheduled_time': scheduled_time})

        schedule_post(data, scheduled_time)

        return redirect('/')
    except Exception as e:
        return {'error': str(e)}

if __name__ == '__main__':
    app.run(debug=True)
