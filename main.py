##Imports 
from datetime import datetime
import tweepy               ##Required library for working with twitter api
import configparser         ##Required  library for reading credentials from the config file
import json                 ##required for reading the output in a pretty json format


###Imports for sending the email
from email.message import EmailMessage   ##Library for creating the email
import ssl   ##Library for adding an additional security layer as SMTP is non-secure porotocol
import smtplib  ##standard protocl for emial services, simple mail transfer protocol

##First of all all the info from the config file

### Create an instanc of configparse
config = configparser.ConfigParser()
###Read the config file
config.read('config.ini')

api_key = config['twitter']['api_key']
api_Key_secret = config['twitter']['api_Key_secret']
acess_token = config['twitter']['acess_token']
acess_token_secret = config['twitter']['acess_token_secret']

# print(acess_token_secret)


## authentication
auth = tweepy.OAuth1UserHandler(api_key,api_Key_secret)
auth.set_access_token(acess_token,acess_token_secret)


api = tweepy.API(auth)

print(api)

user= 'Naval'
limit = 100

tweets = api.user_timeline(screen_name=user,count=limit,include_rts = False, tweet_mode = 'extended')
# tweets = api.user_timeline(usercount=limit,include_rts = False, tweet_mode = 'extended')

# print("some stuff")
# now = datetime.now()
# month_name = "Tweets for month of " + now.strftime('%B')

mytweets = []

for tweet in tweets:
    if tweet.created_at.month == datetime.now().month and tweet.full_text[0] != '@':
        # print("create at:", tweet.created_at)
        # print(tweet.full_text)
        mytweets.append(tweet.full_text)

mystring = '\n\n'.join(mytweets)

# print(mystring)

 ########### Here is the sending Email part #################
email_sender = 'developer.gursevak@gmail.com'
email_password = config['twitter']['email_password']
email_receiver = 'gursevaks2001@gmail.com'

print(email_password)

subject = 'testing email for twitter bot'
body = mystring

em = EmailMessage()
em['From'] = email_sender
em['To'] = email_receiver
em['Subject'] = subject
em.set_content(body)

context = ssl.create_default_context()

with smtplib.SMTP_SSL('smtp.gmail.com', 465, context = context) as smtp:
    smtp.login(email_sender,email_password)
    smtp.sendmail(email_sender,email_receiver,em.as_string())
