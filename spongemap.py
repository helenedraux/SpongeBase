from flask import Flask
from flask import g, session, request, url_for, flash
from flask import redirect, render_template, jsonify
from flask_oauthlib.client import OAuth

app = Flask(__name__)
app.config['DEBUG'] = True
app.secret_key = 'development'


oauth = OAuth()

twitter = oauth.remote_app(
    'twitter',
    base_url='https://api.twitter.com/1.1/',
    request_token_url='https://api.twitter.com/oauth/request_token',
    access_token_url='https://api.twitter.com/oauth/access_token',
    authorize_url='https://api.twitter.com/oauth/authorize',
    consumer_key='fBmNVseiOzmDdfhoQzxIxAm8s',
    consumer_secret='zVu4dwz2H9m6rMuhxIWnE1hRJ9BlBw05ySJhCViGZj95gTPhQE',
    access_token_method='GET'
)


@twitter.tokengetter
def get_twitter_token(token=None):
        return session.get('twitter_oauth')
        # print(resp['oauth_token'], resp['oauth_token_secret'])
        # return resp['oauth_token'], resp['oauth_token_secret']

# @app.before_request
# def before_request():
#     if 'twitter_oauth' in session:
#         g.user = session['twitter_oauth']

@app.route('/login')
def login():
    callback_url = url_for('oauthorized', next=request.args.get('next'))
    return twitter.authorize(callback=callback_url or request.referrer or None)

@app.route('/')
def index():
    return render_template('spongemap.html')

@app.route('/tweets')
def tweets():
    tweets = None
    geocode = request.args.get('geocode')
    resp = twitter.get('search/tweets.json?geocode=' + geocode)
    if resp.status == 200:
        tweets = resp.data
    else:
        flash('Unable to load tweets from Twitter.')
    return jsonify(tweets)

@app.route('/oauthorized')
def oauthorized():
    resp = twitter.authorized_response()
    if resp is None:
        flash('You denied the request to sign in.')
    else:
        session['twitter_oauth'] = resp
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()
