# import necessary libraries
import pandas as pd
import os
import re
import string
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import nltk
nltk.download('stopwords')
nltk.download('wordnet')

# Initialize Empty Dataframe
col = ['message_date', 'location', 'source', 'message']
df = pd.DataFrame(columns=col)

# Iterate through all csv files in the directory and concatenate into pandas dataframe
for file in os.listdir(): 
    filename = file.rsplit('.') 
    if filename[len(filename)-1] == 'csv': 
        df2 = pd.read_csv(file, usecols=[0,2,3,9,10], error_bad_lines=False)
        df = pd.concat([df, df2], axis=0, sort=False)
        
# Print entire message when displaying dataframe
pd.set_option('display.max_colwidth', -1)

# Reset index after concatenation of all data
df = df.reset_index()
del df['index']

# Delete messages that are related to giveaways
drop_rows = [] # Create empty list to rows to be dropped
for i in df.index:
    if df.message.iloc[i].startswith('Win ') or 'giveaway' in df.message.iloc[i].lower(): # Find all rows that start with "Win" or contain "giveaway"
        drop_rows.append(i) # Append the index number of the row
df = df[~df.index.isin(drop_rows)] # Drop rows then reset index
df = df.reset_index()
del df['index']

# Remove weblink from message
for i in df.index:
    tweet = df.message.iloc[i]
    tweet = ' '.join([word for word in tweet.split() if ('http' not in word)]) # Find all words that do not contain 'http'
    df.message.iloc[i] = tweet

# Delete rows which are repetitive messages as the previous rows
previous = df.message.iloc[0] # Set previous to the first message
drop_rows = []
for i in range(1, df.shape[0]):
    if df.message.iloc[i] == previous: # Check if message is the same as the previous message
        drop_rows.append(i) # If message is the same, add index to list of rows to drop
    previous = df.message.iloc[i]
df = df[~df.index.isin(drop_rows)] # Drop rows then reset index
df = df.reset_index()
del df['index']    

# Function that convert date to month and day columns
def time_day(message_date):
    months = []
    days = []
    for date in message_date:
        months.append(int(date.split('-')[1]))
        days.append(int(date.split('-')[2].split(' ')[0]))
    return(months,days)

# Call function to determine month/day then create new columns in dataframe
month_day = time_day(df.message_date)
df['month'] = month_day[0]
df['day'] = month_day[1]

# Select relevant columns from dataframe
df = df[['month', 'day', 'location', 'source', 'message']]

# Function that performs data cleaning on message
lmt = WordNetLemmatizer()
def text_process(text):
    remove_characters = string.punctuation + '“”—ðŸ‘‡˜Šâœï¤ï€¦„àªà™à´à¹ˆà¡¯ツ¯'
    tweet = ''.join([char for char in text if char not in remove_characters]) # Remove punctuation and random characters
    tweet = re.sub(r'\s\s+', ' ', tweet) # Remove whitespace (including new line characters)
    tweet = tweet.lstrip(' ')  # Remove single space remaining at the front of the tweet.
    tweet = tweet.replace('\u2060\u2060', '') # Remove random tabs
    tweet = ''.join(c for c in tweet if c <= '\uFFFF') # Remove emoji
    tweet = tweet.lower() # Convert to lower case
    tweet = ' '.join ([lmt.lemmatize(word) for word in tweet.split()])  # Lemmatization of tweet
    tweet = ' '.join([word for word in tweet.split() if (word not in stopwords.words('english'))]) # Remove stopwords
    return(tweet)

# Perform data cleaning on each message and store as new column
for i in df.index:
    df.at[i, 'new_message'] = text_process(df.message.iloc[i])

# Identify which products are associated to each message
# For iPhone XS, check if 'iphone xs' or 'iphonexs' is in tweet and if the word following it is "max"
def iphone_xs_check(tweet):
    if 'iphonexs' in tweet or 'iphone xs' in tweet:
        tweet = tweet.split()
        for i in range(0, len(tweet)-1):
            if (tweet[i] == 'xs' or tweet[i] == 'iphonexs') and tweet[i+1] != 'max':
                return True
    return False

# For Apple Watch and iPhone XS Max, check of one of the following words is in the tweet
apple_watch_list = ['applewatch4', 'apple watch 4', 'apple watch series 4', 'applewatchseries4', 'applewatch 4', 'apple watch4','applewatch series 4', 'apple watchseries4']
xs_max_list = ['iphone xs max', 'iphonexs max', 'iphonexsmax', 'iphone xsmax', 'xs max', 'xsmax']

# Iterate through each message and identify what products it is associated to
for i in df.index:
    if any(word in df.new_message.iloc[i] for word in xs_max_list):
        df.at[i,"iphone_xs_max"] = True
    else:
        df.at[i,"iphone_xs_max"] = False
        
    if any(word in df.new_message.iloc[i] for word in apple_watch_list):
        df.at[i,"apple_watch"] = True
    else: 
        df.at[i,"apple_watch"] = False
    
    df.at[i, 'iphone_xs'] = iphone_xs_check(df.new_message.iloc[i])

# Drop all rows that aren't associated to one of the products
no_products = []
for i in df.index:
    if df.apple_watch.iloc[i] == False and df.iphone_xs.iloc[i] == False and df.iphone_xs_max.iloc[i] == False: # Check of false for all three product columns
        no_products.append(i) # Append index to list of drop rows
df = df[~df.index.isin(no_products)]  # Drop rows and reset index
df = df.reset_index() #
del df['index']

# Find polarity of message using TextBlob and store as new column in dataframe
from textblob import TextBlob
for i in df.index:
    df.at[i, 'polarity'] = TextBlob(df.new_message.iloc[i]).sentiment[0]

# Write dataframe to CSV to be used for visualization in Excel and Tableau
df.to_csv('final_data.csv', encoding='utf-8', index=False)

# Find frequency of words in the table
word_dictionary = {}
remove_words = ['apple', 'watch', '4', 'series', 'iphonex','phone', 'x','iphonexs', 'iphonexsmax', 'xs', 'max', 'xr', 'iphone', 'iphonexr'] # Don't include words of product name

for i in df.index: # Iterate through each message
    if df.polarity.iloc[i] < 0: # Only consider negative messages (for positive messages, change to '>')
        message = df.new_message.iloc[i].split()
        for word in message:
            if word in remove_words: # Continue if word is in remove words
                continue

            if word not in word_dictionary: # Otherwise add word to the dictionary or increment its frequency if it is already in the dictionary
                word_dictionary[word] = 1
            else:
                word_dictionary[word] += 1
            
words = []
for key, value in word_dictionary.items():
    words.append((value,key))
words.sort(reverse = True) # Sort in reverse frequency to determine the most common words

# Create word cloud
import matplotlib.pyplot as plt
from wordcloud import WordCloud

wordcloud = WordCloud( max_words=500,
                      max_font_size=50,
                      relative_scaling=0.5,
                      colormap='Blues')
wordcloud.generate_from_frequencies(frequencies=word_dictionary)
plt.figure()
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.show()

