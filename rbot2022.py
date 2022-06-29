import tweepy
import time
import random
import heapq as hq
import datetime
from dotenv import load_dotenv
import os

load_dotenv()

def _get_auth_():
    auth = tweepy.OAuthHandler(os.getenv('ACCESS_KEY'),os.getenv('TWITTER_API_KEY'))
    auth.set_access_token(os.getenv('TWITTER_API_SECRET_KEY'),os.getenv('TWITTER_ACCESS_TOKEN'))
    return auth

api = tweepy.API(_get_auth_(), wait_on_rate_limit=True)
# # verification
# try:
#     api.verify_credentials()
#     print("verified")
# except:
#     print("couldn't verify")

''' Variables: '''
# Arrays for guy who ratiod, guy who got ratiod and for no ratio found
WratioArr = ["ratio + no one cares about that tweet + guy who tweeted it needs to get a job 💀","ratio + YB better + delete cringe tweet + no one really asked 💀","ratio + tweet's not even funny + didn't laugh 😐 + cancelled","after checking VAR 🎥 I have carefully decided to award the ratio.","after reviewing the tweets, me and my team of officials have detected a ratio!","immaculate ratio must be framed 🖼","someone took the L and is down horrendously","tell that guy he got ratio'd + the tweet is irrelevant + no one cares","ratio bot decides to award the ratio here.","what an outstanding ratio. buddy above got cooked 😩","ratio so fire it needs to be framed","ice cold ratio", "outstanding ratio", "ratiooooo", "ratio detected!","W","fire ratio", "VAR DECISION: ratio", "ratio identified + W", "we have uncovered a remarkable ratio","successful ratio!"]
NoRatioArr = ["hmmmmm 🤔that doesn't look like a ratio to me","failed ratio + YB better","ratio is no good + not found","ratio nowhere to be found","stop wasting my time there's no ratio","stop being silly there's no ratio", "no ratio as of rn", "no ratio found","come on there's no ratio there...", "no ratio g", "ratio denied", "failed ratio lol"]

# had to stop using LratioArr because twitter complained that it violated the guidelines
LratioArr = ["L + ratio + YB better", "hold this L", "ratio + L + get a job", "ratiooood","hold this L respectfully", "ratio + L", "down bad", "down horrendoulsy", "invalid argument + ratio","hold this L son", "ratio bozo","hold this L buddy", "buddy got cooked","failed ratio"]

# array with images
ratio_img_arr = ["pics/ratio/checkingratio.png","pics/ratio/decisionratio.jpeg","pics/ratio/rratio.jpg","pics/ratio/ratio10.png","pics/ratio/IMG_0303.JPG"]
no_ratio_img_arr = ["pics/noratio/no ratio.jpeg","pics/noratio/noratio1.jpeg","pics/noratio/ratiodenied.jpeg","pics/noratio/vardecision_noratio.jpeg","pics/noratio/IMG_0302.JPG"]

# maps to keep track of wins, losses and draws
wmap = {}
lmap = {}
dmap = {}

# was going to use to count how many ratios, but not needed since i can see how many tweets the bot has put out
ratiocounter = 1 

# check if tweet is protected because bot cant reply to those
def _isprotected_(tweet):
    if tweet.user.protected:
        return True
    return False

''' Functions: '''

def validateRatioFormat(tweet): # validates that there are two tweets above (correct format)
    if tweet.in_reply_to_status_id is not None: 
        temp1 = status(tweet.in_reply_to_status_id) 
        if not _isprotected_(temp1):
            if temp1.in_reply_to_status_id is not None: 
                temp2 = status(tweet.in_reply_to_status_id)
                if not _isprotected_(temp2):
                    return True 
    return False

# checks if the map is empty, would be used for the weekly wrapped, if i did it
def isMapEmpty(map):
    if not map:
        return True
    return False

# adding to map
def mapcount(id, RatioMap): # given an "id_str" will return count of that id
    if id not in RatioMap:
        RatioMap[id] = 1
    else:
        RatioMap[id] += 1
    return RatioMap[id]

# takes the id of an account and returns their score in an array format: [Ws,Ls, Detections]
def acc_status(id): 
    resW,resL,resD = 0,0,0
    if id in wmap:
        resW = wmap[id]
    if id in lmap:
        resL = lmap[id]
    if id in dmap:
        resD = dmap[id]
    return [resW,resL,resD]

# gives random index from array: done by pratuln (his contribution)
def RSFromArray(Arr):
    Ridx = random.randint(0,len(Arr)-1)
    return Arr[Ridx]

# Was planning on doing a weekly wrapped, where every Friday at 6pm, it would give the top3 users with Wins, Losses and Detections, however, twitter is not okay
# with mentioning people without them mentioning the bot first
# given a map (Win,Loss or Detect) the function returns a list of the top 3 things in the map
def weeklywrapped(givenmap):
    topRatios = []
    hq.heapify(topRatios)
    for key,val in givenmap.items():
        tmp = [val*-1,key]
        hq.heappush(topRatios, tmp)
    top3 = []
    # add checks to make sure its not out of bounds
    for i in range(3):
        top3.append(hq.heappop(topRatios))
    return top3

# creates the weekly message
def messageWeekly():
    #checks that map isnt empty and its length is greater than 3, otherwise we get an error
    if isMapEmpty(wmap) or len(wmap) < 3:
        return ""
    top3 = weeklywrapped(wmap)
    content = "top ratio accounts for this week 🔝\n\n"
    sayings = []
    for val, acc in top3:
        tmpuser = api.get_user(user_id=acc)
        tmp = f"@{tmpuser.screen_name} with {val*-1} ratio(s)"
        sayings.append(tmp)
    content += f"[🥇] {sayings[0]}\n[🥈] {sayings[1]}\n[🥉] {sayings[-1]}\n\nit resets every day at 6pm"
    return content

# would be used to determine when its time to post, but changed the function
# will now use it for when its 6pm, so bot clears map - for memory purposes
def timetopostWeekly():
    # post on fridays at 6pm
    dow = datetime.datetime.today().weekday()
    t = datetime.datetime.today().time().strftime("%H:%M:%S")
    if t == "18:00:00": #dow == 4 and 
        return True
    return False

# def time_to_reset_map():
#     dow = datetime.datetime.today().weekday()
#     t = datetime.datetime.today().time().strftime("%H:%M:%S")
#     if dow == 4 and (t)
# def testpost():
#     if timetopostWeekly():
#         api.update_status("posted today at 22:21:00")

def checkiffollowing():
    pass

#to clear all maps at once
def clearmaps():
    wmap.clear()
    lmap.clear()
    dmap.clear()

# would post weekly post but not doing it anymore
def makeWeeklypost():
    if messageWeekly()!="":
        api.update_status(messageWeekly())
        clearmaps()

# posting a reply with picture
def reply_with_media(tweet_id, message, imagepath):
    # media = api.media_upload(imagepath)
    api.update_status_with_media(message,imagepath,in_reply_to_status_id=tweet_id,auto_populate_reply_metadata=True)
    # api.update_status(message,media,in_reply_to_status_id=tweet_id,auto_populate_reply_metadata=True) #,auto_populate_reply_metadata=True
    print("tweeted with media")

# posting a reply without picture
def reply_no_media(tweet_id,message):
    api.update_status(message, in_reply_to_status_id=tweet_id,auto_populate_reply_metadata=True)
    print("tweeted no media")

# makes the format of the message, depending on what case it is
def messageformat(id,option):
    content = ""
    if option == 1: # check ratio
        content = f"{RSFromArray(WratioArr)} 🐐✅"
        # content = f"{RSFromArray(WratioArr)} 🐐✅\n\n{id.user.screen_name} {RSFromArray(LratioArr)} 💀"
    elif option == 2: #ratio account status
        stats = acc_status(id.user.id)
        content = f"@{id.user.screen_name} ratio status:\n\nWins: {stats[0]} ✅\nLosses: {stats[1]} ⬇️\nRatios reported: {stats[2]} 💯"
    elif option == 3: # incorrect format
        content = f"use the correct format\n\n@ me with 'check ratio' to report a ratio (anyone's) or 'ratio account status' to see your account's ratio score"
    else:# no ratio
        content = f"{RSFromArray(NoRatioArr)} 😐"
    return content

# adding to maps at once
def addToMaps(W,L,R):
    mapcount(W.user.id,wmap)
    mapcount(L.user.id,lmap)
    mapcount(R.user.id,dmap)

# calculates if theres a ratio
def calculateratio(tweetID,prevtweetID):
    if tweetID.favorite_count > prevtweetID.favorite_count:
        return True
    else:
        return False

# given an ID, returns the status/tweet
def status(tweetID):
    return api.get_status(tweetID)

def validQuoteRatioFormat(mention):
    if mention.in_reply_to_status_id is not None:
        ratiotwt = status(mention.in_reply_to_status_id)
        if ratiotwt.is_quote_status:
            return True
    return False

# like the random saying array, redundant i know but i forgot i had the other function 
def _randomratiopic_(arr):
    rand = random.choice(arr)
    return rand

# functionality of the code
def applyRatio(mentionedtwt, ratiotwt, ratioedtwt):
    if calculateratio(ratiotwt,ratioedtwt):
        addToMaps(ratiotwt,ratioedtwt,mentionedtwt)
        message = messageformat(ratioedtwt,1)
        reply_with_media(mentionedtwt.id,message, _randomratiopic_(ratio_img_arr))
        print(f"ratio\n{ratiotwt.text}\n{ratioedtwt.text}\n")
    else:
        message = messageformat(mentionedtwt,4)
        reply_with_media(mentionedtwt.id,message,_randomratiopic_(no_ratio_img_arr))
        print(f"no ratio\n{ratiotwt.text}\n{ratioedtwt.text}\n")

# writes current mention ID on a text file so that if the program crashes, it doesnt start from the old mentions
# goes back to the most recent mention
file_name = "last_tweet.txt"
def set_last_seen(last_seen, file_name):
    f_write = open(file_name, 'w')
    f_write.write(last_seen)
    f_write.close()
    print(f"last seen set: {last_seen}")
    return

def retrieve_last_seen_id(file_name):
    f_read = open(file_name, 'r')
    last_seen_id = int(f_read.read().strip())
    f_read.close()
    print(f"last seen found {last_seen_id}")
    return last_seen_id

# needed
def _me_(tweet):
    botid = 1537546826026319872
    if tweet.user.id != botid:
        return False
    return True

def verify_tweet(tweet_id):
    pass
 
# execution of functionality
def replyratio(lastseen):
    # last_seen_id = retrieve_last_seen_id(file_name)
    timeline = api.mentions_timeline(since_id=lastseen) #since_id=last_seen_id
    for mention in reversed(timeline):
        # set_last_seen(mention.id_str,file_name)
        set_last_seen(mention.id_str,file_name)
        
        #checks:
        if (_isprotected_(mention)): # avoid replying to protected tweets
            print("tweet is protected")
            continue
        if (mention.author.id == 1537546826026319872): # avoid replying to itself
            print("i made the mention")
            continue

        if ("check ratio" in (mention.text).lower()):
            if validateRatioFormat(mention):
                prev_tweet = status(mention.in_reply_to_status_id)
                prevprev = status(prev_tweet.in_reply_to_status_id)
                applyRatio(mention,prev_tweet,prevprev)
            elif validQuoteRatioFormat(mention):
                ratio = status(mention.in_reply_to_status_id)
                quote = status(ratio.quoted_status_id_str)
                applyRatio(mention,ratio,quote)
        elif "ratio account status" in (mention.text).lower():
            message = messageformat(mention,2)
            print(f"ratio account status targeted - {mention.user.screen_name}")
            reply_no_media(mention.id_str,message)

    # Had to give up on this. Twitter didnt like it. Tbf, I get it. It spammed. It kept spamming everytime it was mentioned and the correct format wasnt there. 
        # else: # incorrect format
        #     if mention.in_reply_to_status_id is not None:
        #         check1 = status(mention.in_reply_to_status_id)
        #         if not _me_(check1):
        #             message = messageformat(mention,3)
        #             print(f"incorrect format 1 - {mention.text} - {mention.user.screen_name}")
        #             # reply_no_media(mention.id_str,message)
        #     else:
        #         message = messageformat(mention,3)
        #         print(f"incorrect format 2 - {mention.text} - {mention.user.screen_name}")
        #         # reply_no_media(mention.id_str,message)

# for testing purposes
def deleteMentions4testpurposes():
    t = api.user_timeline()
    for i,t1 in enumerate(t):
        if (t1.in_reply_to_status_id is not None) and (t1.in_reply_to_user_id != 1537546826026319872):
            api.destroy_status(t1.id)

def run():
    while True:
        if timetopostWeekly():
            clearmaps()
            # makeWeeklypost()
        replyratio(retrieve_last_seen_id(file_name))
        time.sleep(15)

try:
    run()
except Exception as err:
    print(err)
