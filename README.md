progether
==============
Reuben Castelino - projectdelphai@gmail.com

Description
-------------
A python script that checks reddit for new posts to [/r/progether](http://www.reddit.com/r/progether) and posts the link to #reddit-progether on irc.foonetic.net.

Installation
------------
**On a local computer**

The only dependency needed is:

 1. requests

You can install it with (assuming you have pip):

    pip install requests

All you need to do to run this script is:

    python progether_reddit_bot.py

**On app-engine**

using the appcfg.py script provided with the appengine python sdk, upload your data with:

    appcfg.py update appengine

appengine being the folder holding all the code.

Because it uses sockets, you'll need a paid account app.

**On heroku**

Log in with your heroku toolbelt and create an app:

    heroku create

Edit the Procfile to the desired wait time.

Initialize a git repo with:

    git init
    git add .
    git commit -m 'Initial commit'

Then push to your heroku repo with:

    git push heroku master
