import os
import json
import tweepy
from zipfile import *
import shutil

consumer_key = "5LSrNshaKejTXNZBVe862duoE"
consumer_secret = "DIffWlrW5GlpCsNStjUwZgnFlWMbHYjxhRuJmchPqha2d9HdRc"
access_token = "972188754713522177-3kFUwewWYdk7pzURDf3aJFBRakWYI8p"
access_token_secret = "lWNY8wFJJSKe54NGVQjRCzgW5Jl6Cbcqz3aBlEcHCm1X7"
name_of_data_directory = 'twitter_data'


def main():
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    tweepy_obj = tweepy.API(auth, wait_on_rate_limit=True)
    stat_file, zip_file = create_data_directory_stat_file(name_of_data_directory, 'stats.txt')
    dict_uid_tweetid = read_the_file('twitter.tab')
    download_tweets_create_files(dict_uid_tweetid, tweepy_obj, stat_file, zip_file, name_of_data_directory)
    release_resources(stat_file, zip_file)


def release_resources(stat_file, zip_file):
    # closes the relevant files and deletes the temporary twitter_data folder
    stat_file.close()
    zip_file.close()
    shutil.rmtree(os.getcwd() + '/' + name_of_data_directory)


def download_tweets_create_files(dict_uid_tweetid:dict, tweepy_obj, stat_file, zip_file, name_of_data_directory):
    added, erred = 0, 0
    print('Total Unique = ',len(dict_uid_tweetid))
    for key, value in dict_uid_tweetid.items():
        try:
            tweet = tweepy_obj.get_status(value)._json
            path_to_write = os.getcwd() + '/' + name_of_data_directory + '/'
            file_name = key + ".json"
            outfile = open(path_to_write + file_name, "w")
            json.dump(tweet, outfile, indent=4)
            outfile.close()
            zip_file.write(path_to_write + file_name, file_name)
            added += 1
        except tweepy.TweepError as e:
            print(e.reason)
            stat_file.write("FAILED FOR UID = "+key+' TWITTER_ID = '+value+" Reason - "+e.reason+"\n")
            erred += 1

    print("COMPLETED DOWNLOADING")
    stat_file.write("===========================================================\n")
    stat_file.write("SUMMARY - \n"+"Added = "+str(added)+"\n"+"Erred = "+str(erred))


def read_the_file(path_to_file:str):
    '''
    :param path_to_file:
    :return: a dictionary of {'uid','tweet_id'}
    '''
    dict_uid_tweetid = {}
    with open(path_to_file, 'r') as twitter_file:
        # skipping the header row
        next(twitter_file)
        for line in twitter_file:
            list_entry = line.split("\t")
            dict_uid_tweetid[list_entry[0]] = list_entry[1]
    return dict_uid_tweetid


def create_data_directory_stat_file(dir_name:str, stat_file:str):
    '''
    creates the directory twitter_data, stats.txt and twitter_data.zip
    :param dir_name:
    :param stat_file:
    :return:
    object reference to stats.txt and twitter.zip
    '''
    data_directory = os.path.join(os.getcwd(), dir_name)
    if not os.path.exists(data_directory):
        os.makedirs(data_directory)

    stat_file = open(stat_file,"w")
    zip_file = ZipFile(dir_name+'.zip', 'w', ZIP_DEFLATED)
    return stat_file, zip_file


if __name__ == '__main__':
    main()



