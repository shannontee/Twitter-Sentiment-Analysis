# import necessary libraries
import tweepy
import string

# Define keys and token
customer_key = 'vPP21jiYB2yA5psegV8AnMpT1'
customer_secret = 'cONCNWe403nxXpmet2W7dq4Udhx52xfjTBBnNBMk3l4sTuJF2N'
access_token = '1317743546-gCvFOYgZD1clQfDpzqrsedj3J6SowcfL0K87CMW'
access_token_secret = 'GiqKQQz9AHQFYm8HHD5WOCLDJ4PnqZqyleSLVwvEBZKDX'

# Use above keys and token to perform authentication
auth = tweepy.OAuthHandler(customer_key, customer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# Open file to write
fout = open('myData.csv', 'w')

# Write headers of CSV to the file
fout.write('message_date,tweet_ID,language,location,user_screen_name,followers_count,friends_count,retweeted,retweet_count,source,message')
fout.write('\n')

# Define replacements for punctuation and newline
translator = str.maketrans('','', '\n')
translator2 = str.maketrans('','', string.punctuation)


# Use the tweepy cursor to fetch messages in extended mode for the given date and in english
# 1000 messages collected for each keyword
fetch_AppleWatch_4 = tweepy.Cursor(api.search, q='Apple Watch 4 since:2018-10-31 until:2018-11-30', lang = 'en', tweet_mode = 'extended').items(1000)
fetch_AppleWatch4 = tweepy.Cursor(api.search, q='AppleWatch4 since:2018-10-31 until:2018-11-30', lang = 'en', tweet_mode = 'extended').items(1000)

# Iterate through each JSON fetched to extract desired data
for i in fetch_AppleWatch4:
    if ('RT ' not in i.full_text): # Remove messages that start with RT to filter out retweets
        # Identify desired data to store
        current_date = str(i.created_at)
        current_ID = str(i.id)
        language = str(i.lang)
        location = str(i.user.location).replace(',', '.') # Replace "," in location with "." so that it does not create problems in the CSV file
        user_screen_name = str(i.user.screen_name)
        follower_count = str(i.user.followers_count)
        friends_count = str(i.user.friends_count)
        retweeted = str(i.retweeted)
        retweet_count = str(i.retweet_count)
        source = str(i.source)
        message = str(i.full_text).translate(translator) # Replace undesired punctuation and newline in messages
        message = message.translate(translator2).replace('‚', '')

        # Store tweet data collected as a list
        x = [current_date, current_ID, language, location, user_screen_name, follower_count,friends_count, retweeted, retweet_count, source, message]
        string = ','.join(x) # Join the list together with "," such that it is in CSV format
        fout.write(string) # Write out string of message and associated information to the file
        fout.write('\n')

# Same as the for loop above except for different fetch of different keywords
for i in fetch_AppleWatch_4:
    if ('RT ' not in i.full_text):
        current_date = str(i.created_at)
        current_ID = str(i.id)
        language = str(i.lang)
        location = str(i.user.location).replace(',', '.')
        user_screen_name = str(i.user.screen_name)
        follower_count = str(i.user.followers_count)
        friends_count = str(i.user.friends_count)
        retweeted = str(i.retweeted)
        retweet_count = str(i.retweet_count)
        source = str(i.source)
        message = str(i.full_text).translate(translator)
        message = message.translate(translator2).replace('‚', '')
        x = [current_date, current_ID, language, location, user_screen_name, follower_count, friends_count, retweeted, retweet_count, source, message]
        string = ','.join(x)
        fout.write(string)
        fout.write('\n')

# Same code as above but to collect data for iPhoneXS
fetch_iPhoneXS = tweepy.Cursor(api.search, q='iPhoneXS since:2018-10-31 until:2018-11-01',lang = 'en', tweet_mode = 'extended').items(1000)
fetch_iPhone_XS = tweepy.Cursor(api.search, q='iPhone XS since:2018-10-31 until:2018-11-01', lang = 'en', tweet_mode = 'extended').items(1000)

for i in fetch_iPhoneXS:
    if ('RT ' not in i.full_text):
        current_date = str(i.created_at)
        current_ID = str(i.id)
        language = str(i.lang)
        location = str(i.user.location).replace(',', '.')
        user_screen_name = str(i.user.screen_name)
        follower_count = str(i.user.followers_count)
        friends_count = str(i.user.friends_count)
        retweeted = str(i.retweeted)
        retweet_count = str(i.retweet_count)
        source = str(i.source)
        message = str(i.full_text).translate(translator)
        message = message.translate(translator2).replace('‚', '')
        x = [current_date, current_ID, language, location, user_screen_name, follower_count, friends_count, retweeted, retweet_count, source, message]
        string = ','.join(x)
        fout.write(string)
        fout.write('\n')

for i in fetch_iPhone_XS:
    if ('RT ' not in i.full_text):
        current_date = str(i.created_at)
        current_ID = str(i.id)
        language = str(i.lang)
        location = str(i.user.location).replace(',', '.')
        user_screen_name = str(i.user.screen_name)
        follower_count = str(i.user.followers_count)
        friends_count = str(i.user.friends_count)
        retweeted = str(i.retweeted)
        retweet_count = str(i.retweet_count)
        source = str(i.source)
        message = str(i.full_text).translate(translator)
        message = message.translate(translator2).replace('‚', '')
        x = [current_date, current_ID, language, location, user_screen_name, follower_count, friends_count, retweeted, retweet_count, source, message]
        string = ','.join(x)
        fout.write(string)
        fout.write('\n')

# Same code as above but to collect data for iPhoneXS Max
fetch_iPhoneXSMax = tweepy.Cursor(api.search, q='iPhoneXSMax since:2018-10-31 until:2018-11-01', lang = 'en', tweet_mode = 'extended').items(1000)
fetch_iPhoneXS_Max = tweepy.Cursor(api.search, q='iPhone XS Max since:2018-10-31 until:2018-11-01', lang = 'en', tweet_mode = 'extended').items(1000)

for i in fetch_iPhoneXSMax:
    if ('RT ' not in i.full_text):
            current_date = str(i.created_at)
            current_ID = str(i.id)
            language = str(i.lang)
            location = str(i.user.location).replace(',', '.')
            user_screen_name = str(i.user.screen_name)
            follower_count = str(i.user.followers_count)
            friends_count = str(i.user.friends_count)
            retweeted = str(i.retweeted)
            retweet_count = str(i.retweet_count)
            source = str(i.source)
            message = str(i.full_text).translate(translator)
            message = message.translate(translator2).replace('‚', '')
            x = [current_date, current_ID, language, location, user_screen_name, follower_count, friends_count, retweeted, retweet_count, source, message]
            string = ','.join(x)
            fout.write(string)
            fout.write('\n')

for i in fetch_iPhoneXS_Max:
    if ('RT ' not in i.full_text):
            current_date = str(i.created_at)
            current_ID = str(i.id)
            language = str(i.lang)
            location = str(i.user.location).replace(',', '.')
            user_screen_name = str(i.user.screen_name)
            follower_count = str(i.user.followers_count)
            friends_count = str(i.user.friends_count)
            retweeted = str(i.retweeted)
            retweet_count = str(i.retweet_count)
            source = str(i.source)
            message = str(i.full_text).translate(translator)
            message = message.translate(translator2).replace('‚', '')
            x = [current_date, current_ID, language, location, user_screen_name, follower_count, friends_count, retweeted, retweet_count, source, message]
            string = ','.join(x)
            fout.write(string)
            fout.write('\n')

# Close open file
fout.close()

