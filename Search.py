import nltk
import csv 
from nltk.tag import CRFTagger
import re
import json
import tweepy
from datetime import datetime, timedelta
from itertools import islice
import pandas as pd
from pytz import timezone
from datetime import datetime
from nltk.tokenize import word_tokenize
# from nltk.tokenize.treebank import TreebankWordTokenizer

# Pembentukan Kalimat 
# ex : Carikan kondisi jalan di daerah jakarta 
# ex : Lakukan pencarian kondisi jalan Sudirman    
class Search:
   # Initialion
   def __init__(self, search, waktu):
      self.search = search
      self.waktu = waktu
      self.perintah = ["coba","lakukan", "cari.*", "beri*", "*kasih*", "*info*", "*keluar*", "*tampil*"]
      self.objek = ["jalan","lalulintas", "lalu","lintas","flyover", "tol","jembatan", "daerah", "drh", "jl", "perempatan", "bundaran", "lalin", "wilayah"]       
      self.objek_dua = ["pondok", "pasar", "yos", "karet", "hasyim", "gunung", "hj", "wr"]
      self.data_ekstraksi = []
      self.tz = timezone("UTC")
      # Tweepy variables key 
      self.twt_api_key = "JgWqH9Yr8ajFJ3EE0ZCFK3tCU"
      self.twt_api_secret = "IBpmjwvzqFuHEvrodn2E4iHp7YGCLJVUnFEqayF8s7QTYyreLJ"
      self.twt_bearer_token = "AAAAAAAAAAAAAAAAAAAAANwiiwEAAAAA1eJhS4N%2BLLdDLzQTSHyA2vnEw8s%3De7Ucftzc7j3Poef4YBW4HrlHfEgpnJlNXesgqt1JubkRUapX6U"
      self.twt_access_token = "1582412007017689088-0S9fOlNOsSHRstbRtJLZIodcIU53sH"
      self.twt_access_token_secret = "89wBNIM9gXmUlDDP0LS030TKyFUn4bLy2Q9CHkln3gSzQ"
      
      self.auth = tweepy.OAuthHandler(self.twt_api_key, self.twt_api_secret)
      self.auth.set_access_token(self.twt_access_token, self.twt_access_token_secret)
      self.tweet_api = tweepy.API(self.auth)

      # get json pencarian 
      with open("Dataset/pencarian.json", "r") as f:
         # Read the JSON string from the file
         json_str = f.read()
         # Parse the JSON string
         self.json_data = json.loads(json_str)

      # Get data from ekstraksi data csv
      with open("Dataset/ekstaksi_data_traffic.csv", "r") as file:
         reader = csv.reader(file)
         for row in islice(reader, 1, None):
            self.data_ekstraksi.append(row)

   def search_word(self):     
      # Preprocessing function
      # lower text
      lower_text = self.search.lower()
      print("======CaseFolding ====================")
      print(self.search)
      print(lower_text)
      # convert waktu ke get jam
      hour = self.select_hour_for_input(self.waktu)
      # Tokenize words
      tokenize_word = word_tokenize(lower_text)
      flag = False
      object_key = []
      perintah_key = []
      detail_key = []
      match_data = []
      flag_dataset = False
      flag_twitter = False
      for i in range(len(tokenize_word) - 1):
         for objek in self.objek:
            
            if re.search(objek, tokenize_word[i]):
               # print(tokenize_word[i])
                # get Word Object
               object_key.append(tokenize_word[i]) 
               # Then after getting the first key, need to get command word
               for j in range(i-1, -1,-1):
                  perintah_key.append(tokenize_word[j])
               # Get object 2 contoh seperti ex: Pondok, pasar, gunung
               for objekdua in self.objek_dua:
                  # print( tokenize_word[i +1])
                  if re.search(objekdua, tokenize_word[i +1]):
                     print( tokenize_word[i +1])
                     # get Word Object 2
                     object_key.append(tokenize_word[i+1]) 
                     # Get street name
                     object_key.append(tokenize_word[i+2]) 
                     detail_key.append(tokenize_word[i+2])
                     flag = True
                     break
               if flag == False:
                  object_key.append(tokenize_word[i+1]) 
                  detail_key.append(tokenize_word[i+1])
               break
      # Save data to josn file for datasets
      json_search_object = {}
      json_search_object['command'] = {}
      json_search_object['street'] = {}


      # Save Street data
      for i, item in enumerate(object_key):
         json_search_object['street'][f"object_key{i+1}"] = item

      # Save command data 
      for i, perintah_key in enumerate(reversed(perintah_key)):
         json_search_object['command'][f"command_key{i+1}"] = perintah_key

      # Save data input pencarian 
      self.json_data['pencarian_data'].append(json_search_object)
      # json_data = json.dumps(self.json_data)
      # json_search_object['search_data'].append()
      # json_search = [json_search_object]
     
      with open("Dataset/ekstaksi_data_traffic.csv", "r") as file:
         # Create a DictReader object
         reader = csv.reader(file)
         # Get the header
         header = next(reader)
         # Find the index of the column we want to search
         column_index = header.index("jalan")
         # Create a list to store the rows that match the search value
         matching_rows = []
         # Iterate over the rows in the CSV file
         for row in reader:
            # Check if the value in the column we want to search contains the search value
            if detail_key[0] in row[column_index]:
               matching_rows.append(row)
         # Print the matching rows
         for row in matching_rows:
            # Search using time 
            row_hour = self.select_hour(row[1])
            row_time = self.select_time(row[1])
            row.append(row_hour)
            row.append(row_time)
            print(row)
            if hour == row[3]:
               match_data.append(row)
               # flag_twitter = True
               # flag_dataset = True
               # jika tidak ada data jalan yang dicari match dengan waktu maka cari 
               # data dari hasil ekstraksi dengan waktu yang sama dengan waktu pencarian 
            # elif len(match_data) == 0:
            #    for data_ekstraksi in self.data_ekstraksi:
            #       print(data_ekstraksi)
            #       # select jam
            #       row_hour2 = self.select_hour(data_ekstraksi[1])
            #       # select time
            #       data_ekstraksi.append(self.select_time(data_ekstraksi[1]))
            #       data_ekstraksi.append(row_hour2)
            #       if hour == data_ekstraksi[1]:
            #           match_data.append(data_ekstraksi)
            #       # elif len(match_data) == 0:
            #       #    data_tweet = self.search_traffic_from_twitter()
      if len(match_data) == 0 and flag_dataset == False:
         for data_ekstraksi in self.data_ekstraksi:
            print("cari di ekstraksi")
            print(data_ekstraksi)
            # select jam
            row_hour2 = self.select_hour(data_ekstraksi[1])
            # select time
            data_ekstraksi.append(self.select_time(data_ekstraksi[1]))
            data_ekstraksi.append(row_hour2)
            if hour == data_ekstraksi[4]:
               match_data.append(data_ekstraksi)  
         flag_dataset = True     

      if len(match_data) == 0 and flag_twitter == False:
         print("-----------------------------------------------------------------------------")
         print("data dicari")
         data_tweet = self.search_traffic_from_twitter()
         print("=============================get inner data=========================")
         # for tweet in data_tweet:
         #    if len(tweet) != 0:
         match_data.append(data_tweet)
         match_data = list(filter(None, match_data[0]))
         print(match_data)
         
         #Filter time is same cause sometime is not same in twitter search 
         match_data = [[inner_list[0], inner_list[1], inner_list[2]] for inner_list in match_data if int(inner_list[2].split(".")[0]) == int(self.select_hour_for_input(self.waktu))]
         flag_twitter = True

     



   
      # print (filtered_rows)

      # Console log 
      # print("================= Data Ekstraksi =============================")
      # print(self.data_ekstraksi)
      print("==============================================================")
      print(self.json_data)
      print(object_key)
      print("=======================Tokenize Word===============================")
      print(tokenize_word)
      print("=================Data Match============================")
      print(match_data)
      # print(json_search_list)
      print("================= Row =============================")
      print(row)
   
      return match_data, flag_dataset, flag_twitter

   def search_traffic_from_twitter(self):
      username = "TMCPoldaMetro"
      time = self.select_hour_for_input(self.waktu)
      # word = "specific_word"
      traffic_tweet = []
  
      # start_time = datetime.now(self.tz) - timedelta(hours=1)
      # end_time = datetime.now(self.tz)
      tweets = self.tweet_api.search_tweets(q=f"{time} AND from:{username}", count=10)
      for tweet in tweets:
         print(tweet.text)
         # created_at = tweet.created_at.replace(tzinfo=None)
         # if start_time <= tweet.created_at <= end_time:
         traffic_tweet.append(self.clean_tweet_and_processing(tweet.text))
     
      # print("================================ Traffic Tweets =================================")
      # print(traffic_tweet)
      return traffic_tweet





   # mendaptakan data kondisi pada twitter data traffic
   def clean_tweet_and_processing(self, text):
      tweet = []
      tweets = []
      # lowcasing
      text = text.lower()
      # Cleaning link 
      text = self.cleaning_text(text)
      words = text.split()
      
      if "terpantau" in words:
         index = words.index("terpantau")
         if index < len(words) - 1:
            for i in range(index+1, len(words)):
                  if "." in words[i]:
                     tweet.append("terpantau "+ " ".join(words[index+1:i]))
                     break
                  elif i == len(words)-1:
                     tweet.append("terpantau "+ " ".join(words[index+1:]))
            tweet.append(" ".join(words[1:index]))
            tweet.append(words[0])
         else:
            print("There is no word after 'terpantau'.")
      return tweet


   # Clean link
   def cleaning_text(self, text):
      
      url_pattern = re.compile(r'https?://\S+|www\.\S+')
      text =  url_pattern.sub(r'', text)

      # remove spasi berlebih dan enter 
      text = text.replace('\\t'," ") .replace('\\n'," ").replace('\\u'," ").replace('\\',"")

      return text

   def select_hour_for_input(self, time):
      date_time_obj = datetime.strptime(time, '%H:%M:%S')
      time_str = date_time_obj.strftime("%H")
      return time_str

   def select_hour(self, time):
      date_time_obj = datetime.strptime(time, '%d %B %Y %H:%M:%S')
      time_str = date_time_obj.strftime("%H")
      return time_str
   
   def select_time(self, time):
      date_time_obj = datetime.strptime(time, '%d %B %Y %H:%M:%S')
      time_str = date_time_obj.strftime("%H:%M:%S")
      return time_str