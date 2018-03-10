The module twitter_download.py
1. Downloads the tweets as specified in the twitter.tab file.
2. Each downloaded tweet is stored in a separate uid.json file where uid is the unique id read from the twitter.tab file
3. All these tweet files as are added into a twitter_data.zip file.

Output files
1. twitter_data.zip -  is the zip of all the json files created for the tweets.
2. stats.txt - contains the information of the tweets which could not be downloaded along with their uid(s) and twitter id.
3. twitter_download.py -  module which contains all the code carrying out the above tasks.
4. README.txt