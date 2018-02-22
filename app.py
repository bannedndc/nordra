#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
from flask import Flask, render_template, request, redirect
from flask import Markup
from postmonkey import PostMonkey
from postmonkey import MailChimpException
# from flask.ext.sqlalchemy import SQLAlchemy
import requests
import logging
from logging import Formatter, FileHandler
import os

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
app.config.from_object('config')
pm = PostMonkey('5eb1d21efa1f1f5f6e11f1c9c8213e51-us14')
#db = SQLAlchemy(app)

# Automatically tear down SQLAlchemy.
'''
@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()
'''

# Login required decorator.
'''
def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap
'''
#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#


@app.route('/')
def home():
    posts = []
    upcoming_shows =\
      requests.get("http://api.songkick.com/api/3.0/artists/8823199/calendar.json?apikey=zdpZeMNcromcrzB4&order=desc")
    past_shows =\
      requests.get("http://api.songkick.com/api/3.0/artists/8823199/gigography.json?apikey=zdpZeMNcromcrzB4&order=desc")
    return render_template('home.html',
               posts=posts,
			   upcoming_shows=upcoming_shows.json(),
			   past_shows=past_shows.json())


@app.route('/consume')
def consume():
    return render_template('consume.html')


@app.route('/cv')
def cv():
    return render_template('cv.html')


@app.route('/mta_epk')
def mta_epk():
    return render_template('mta_epk.html')


@app.route('/signup_post', methods=['POST'])
def signup_post():
    try:
        email = request.form['email']
        #email = request.args.get('email')
        if email:
            pm.listSubscribe(id="4f96a5641b", email_address=email, double_optin=False)

    except MailChimpException, e:
        print e.code
        print e.error
        return redirect("/")

    return redirect("/")

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
