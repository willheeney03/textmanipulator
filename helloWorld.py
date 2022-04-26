import tweepy
import AuthKeys as keys
import re
import time
from TextRegenerator import trgnr
from random import randrange
from os import environ


consumer_key = environ['CONSUMER_KEY']
consumer_secret = environ['CONSUMER_SECRET']
access_token = environ['ACCESS_TOKEN']
access_token_secret = environ['ACCESS_TOKEN_SECRET']

auth = tweepy.OAuth1UserHandler(
   consumer_key, consumer_secret, access_token, access_token_secret
)

api = tweepy.API(auth)

#public_tweets = api.home_timeline()
#for tweet in public_tweets:
#    print(tweet.text)
#api.update_status("Hello World!")

mentions = api.mentions_timeline()

listOfIDs = []
for mentionInit in mentions:
    listOfIDs.append(mentionInit.id)

while(True):
    mentions = api.mentions_timeline()
    for mention in mentions:

        statusID = mention.id
        if statusID not in listOfIDs:
            listOfIDs.append(statusID)

            status = api.get_status(statusID, tweet_mode = "extended")
            text = status.full_text.lower()
            print(text)

            #Do work on text here
            print("start work on text")
            text = re.sub(r"@([^\s]+)",'',text)
            variationList = trgnr.generateStrVariations(text)
            print(variationList)
            output = "@" + str(mention.user.screen_name) + " " + variationList[randrange(0,len(variationList))]
            print("finish work on text")

            #send out tweet
            try:
                api.update_status(output,in_reply_to_status_id = mention.id)
                print("tweet sent!")
            except:
                print("tweet did not send properly")
    print("is this working lol")
    time.sleep(25)



