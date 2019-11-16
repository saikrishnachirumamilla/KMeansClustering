#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Created on Fri Nov  8 11:52:39 2019

@author: saikrishnachirumamilla
"""

import pandas as pd
from pwd import getpwnam
from grp import getgrnam
import os, sys, re, string


class K_Means_Clustering:

    def __init__(
        self,
        k=5,
        tolerance=0.0001,
        max_iterations=500,
        ):
        self.k = k
        self.tolerance = tolerance
        self.max_iterations = max_iterations
    
    def jaccard_distance(self,x,y):
        x = x.split(" ")
        y = y.split(" ")
        j_distance = 1 - ((len(set(x).intersection(set(y))))/(len(set(x).union(set(y)))))
        return j_distance
    
    def calculate_sse(self,cluster):
        sse = 0
        for key_tweet,value_tweets in cluster.items():
            for tweet in value_tweets:
                sse_dist = self.jaccard_distance(key_tweet,tweet)
                sse = sse + sse_dist * sse_dist 
        return sse
    
    def kmeans(self,tweet_data,seeds,final_clusters):
        cluster = {}
        
        for i in range(len(seeds)):
            cluster[seeds[i]] = []
        
        for tweet in tweet_data:
            min_distance = sys.maxsize
            min_seed = ''
            for i in range(len(seeds)):
                j_distance = self.jaccard_distance(seeds[i],tweet)
                if(j_distance < min_distance):
                    min_distance = j_distance
                    min_seed = seeds[i]        
            cluster[min_seed].append(tweet)
        
        seeds = []
        
        for key_tweet,value_tweets in cluster.items():
             best_centroid_distance = 1
             best_centroid = ''
             for tweet in value_tweets:
                  distance = 0
                  for next_tweet in value_tweets:
                      distance = distance + self.jaccard_distance(tweet,next_tweet)
                  mean = distance/len(value_tweets)
                  if(mean < best_centroid_distance):
                      best_centroid_distance = distance
                      best_centroid = tweet
             seeds.append(best_centroid)
             
        
        if final_clusters == str(cluster):
            cluster_no = 1;
            for key,value in cluster.items():
                print(str(cluster_no) + '        ')
                for tweet in value:
                    print(tweet + ', ')
                print('\n')
                cluster_no = cluster_no + 1
            
            print("Value of K : "+ str(self.k))
            print("SSE : "+ str(self.calculate_sse(cluster)))
            print("Size of each cluster : ")
            cluster_no = 1;
            for key,value in cluster.items():
                cluster_count = 1;
                for tweet in value:
                    cluster_count = cluster_count + 1
                print(str(cluster_no) + ' : '+str(cluster_count))
                cluster_no = cluster_no + 1
            print('\n')
            return 
            
        final_clusters = str(cluster)
        self.kmeans(tweet_data,seeds,final_clusters)       
                    


def main():

    uid = getpwnam('saikrishnachirumamilla')[2]
    gid = getgrnam('staff')[2]
    os.chown('usnewshealth.txt'
             , uid, gid)

    with open('usnewshealth.txt'
              ) as file:
        tweets = file.readlines()
        
    def strip_links(text):
        url_regex = \
            re.compile('((https?):((//)|(\\\\))+([\w\d:#@%/;$()~_?\+-=\\\.&](#!)?)*)'
                       , re.DOTALL)
        occurences = re.findall(url_regex, text)
        for instance in occurences:
            text = text.replace(instance[0], ', ')
        return text

    def strip_all_entities(text):
        characters = ['@', '#']
        for character in string.punctuation:
            if character not in characters:
                text = text.replace(character, ' ')
        words = []
        for word in text.split():
            word = word.strip()
            if word:
                if word[0] not in characters:
                    words.append(word)
        return ' '.join(words)

    def strip_tweet_id_timestamp(text):
        return re.sub("^[0-9]*\|.*\|", '', text)
        
    clusters = [100,250,500,1000,1300]
    
    for i in range(len(tweets)):
            tweets[i] = tweets[i].lower()
            tweets[i] = strip_tweet_id_timestamp(tweets[i])
            tweets[i] = strip_links(tweets[i])
            tweets[i] = strip_all_entities(tweets[i])

    for cluster in clusters:
        km = K_Means_Clustering(cluster)
        seeds = []
        for i in range(km.k):
            seeds.append(tweets[i])
        km.kmeans(tweets,seeds,final_clusters='')    
        
if __name__ == "__main__":
	main()