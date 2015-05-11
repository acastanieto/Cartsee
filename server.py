from flask import Flask, render_template, redirect, request, session
from oauth2client.client import OAuth2WebServerFlow
import httplib2 # used in login_callback()
from apiclient.discovery import build
import apiclient # used in login_callback()
import os # to get gmail client secrets from os.environ
from oauth2client.file import Storage # used in login_callback()


app = Flask(__name__)

app.secret_key = "ABC"

def get_oauth_flow():
    """Instantiates an oauth flow object to acquire credentials to authorize
    app access to user data.  Required to kick off oauth step1"""

    flow = OAuth2WebServerFlow( client_id = os.environ['GMAIL_CLIENT_ID'],
                                client_secret = os.environ['GMAIL_CLIENT_SECRET'],
                                scope = 'https://www.googleapis.com/auth/gmail.readonly',
                                redirect_uri = 'http://127.0.0.1:5000/return-from-oauth/')
    return flow

@app.route('/')
def landing_page():
    """Renders landing page html template with Google sign-in button
    and demo button"""

    # TODO special Google sign-in button
    # https://developers.google.com/identity/protocols/OpenIDConnect

    return 'This is the landing page.  <html><body><a href="/login/">Login</a></body></html>'

@app.route('/login/')
def login():
    """OAuth step1 kick off - redirects user to auth_uri on app platform"""

    # TODO if user already authenticated, redirect to ???
    # If user already authenticated, do I need to use AccessTokenCredentials here?
    # To quote the oauth python docs, 'The oauth2client.client.AccessTokenCredentials class
    # is used when you have already obtained an access token by some other means.
    # You can create this object directly without using a Flow object.'
    # https://developers.google.com/api-client-library/python/guide/aaa_oauth#oauth2client

    auth_uri = get_oauth_flow().step1_get_authorize_url()

    return redirect(auth_uri)

@app.route('/return-from-oauth/')
def login_callback():
    """This is the auth_uri.  User redirected here after OAuth step1.
    Here the authorization code obtained when user gives app permissions
    is exchanged for a credentials object"""

    # TODO if user declines authentication, redirect to landing page

    code = request.args.get('code') # the authorization code 'code' is the query
                                    # string parameter
    # code = "4/MumWonD34o51uffVVLROsbBMGx6jjyyDh7veXmVl0Es.EgGo8xgTzhYdEnp6UAPFm0H4A-WImgI#"
    print "()()()()()() CODE: ", code

    # return "get out of here"
    # code = "4/laXxiQW6fMIBybKGbc_GD2Cu9Mu945ZYcz6QJA-3bOQ.MhzPYcnJqeUYEnp6UAPFm0FG4f-ImgI#"
    credentials = get_oauth_flow().step2_exchange(code)

    print "()()()()()() CREDENTIALS: ", credentials

    http = httplib2.Http()
    http = credentials.authorize(http)

    print "()()()()()() HTTP: ", http


    service = build('gmail', 'v1', http=http) # build gmail service
    # TODO: make sure parameters 'gmail' and 'v1' correct
    # really confused as to what's going on here. I grabbed this code from
    # https://developers.google.com/gmail/api/quickstart/quickstart-python
    # and I'm not sure if these paramaters are correct for what i want.

    print "()()()()()() SERVICE: ", service


    storage = Storage('gmail.storage') # TODO: make sure parameter is correct
    storage.put(credentials)

    print "()()()()()() STORAGE is storing credentials: ", storage

    credentials = storage.get() # not sure this goes here

    print "()()()()()() CREDENTIALS RETRIEVED FROM STORAGE."

    print "()()()()()() RETRIEVED CREDENTIALS: ", credentials

    print "()()()()()() REDIRECTING TO /visualization/"

    return redirect('/visualization/')

@app.route('/visualization/')
def visualize():
    """Visualize cart data here"""

    return "This is where I will visualize data"

if __name__ == '__main__':
    # debug=True gives us error messages in the browser and also "reloads" our web app
    # if we change the code.
    app.run(debug=True)
    DebugToolbarExtension(app)
