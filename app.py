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
    pylonii = Markup('<iframe height=\"315\" src=\"https://www.youtube.com/embed/XVbN-YTI5Go?rel=0&amp;controls=0&amp;showinfo=0\" frameborder=\"0\" style=\"width: 100%;\" allow=\"autoplay; encrypted-media\" allowfullscreen></iframe>')

    pyloniii = Markup('<img src=\"/static/img/pyloniii.png\" style=\"width: 100%;\"> </img>')

    hm = Markup('<iframe width=\"100%\" height=\"300\" scrolling=\"no\" frameborder=\"no\" allow=\"autoplay\" src=\"https://w.soundcloud.com/player/?url=https%3A//api.soundcloud.com/playlists/449589075%3Fsecret_token%3Ds-CNv2b&amp;color=%23dc2c2e&amp;auto_play=false&amp;hide_related=false&amp;show_comments=true&amp;show_user=true&amp;show_reposts=false&amp;show_teaser=true&amp;visual=true\"></iframe>')

    bicycle_wheel = Markup('<iframe src=\"https://player.vimeo.com/video/127686370?title=0&byline=0&portrait=0\" width=\"100%\" height=\"360\" frameborder=\"0\" webkitallowfullscreen mozallowfullscreen allowfullscreen></iframe>')

    solipsistic_sines = Markup('<iframe src=\"https://player.vimeo.com/video/152095899?title=0&byline=0&portrait=0\" width=\"100%\" height=\"360\" frameborder=\"0\" webkitallowfullscreen mozallowfullscreen allowfullscreen></iframe>')


    events = [
	      {'title': "PYLON III", 'content': pyloniii, 'description': "Score to PYLON III--the final work in a trilogy of full-length dance performances choreographed by Coleman Pester. The PYLON series examines complex systems of control and a journey towards utopia, using highly physical choreography, architectural set pieces, and a variety of analog and digital technologies altogether in a tense relationship."}
        ,{'title': "Jodorowsky's The Holy Mountain re-score", 'content': hm, 'description': "A commissioned live score with Jodorowsky's The Holy Mountain for the Puget Soundtrack Residency, a Cue Northwest project in partnership by Brick Lane Records and Northwest Film Forum."}
       ,{'title': "PYLON II", 'content': pylonii, 'description': "Score to PYLON II--explores themes of systematic fear and control placed on human bodies operating within a quagmire of technological systems essential to modern society (i.e. surveillance, the internet, architectural design). PYLON II incorporates live surveillance feeds to explore questions of observation and consent. Audiences for PYLON II enter into an immersive environment featuring, a cast of five dancers engaged in highly physical choreographed movement, a live sound score, and a complex surveillance system which is simultaneously recording and projecting visual information coming from cameras throughout the space."}
       ,{'title': "Bicycle Wheels", 'content': bicycle_wheel, 'description': "Bicycle wheel instrument used live and made to act like a tremolo by spinning the wheel in-between a photoresistor and a bright light."}
       ,{'title': "Solipsistic Sines", 'content': solipsistic_sines, 'description': "Score to experimental short 'Nineteen 96 Ounces' by Mariel Andersen, first performed by a Computer Music Ensemble as part of Digitalis 2014, using a graphical score and a Max-MSP patch built for the performers."}
      ]
    return render_template('consume.html')


@app.route('/cv')
def cv():
    return render_template('cv.html')


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
