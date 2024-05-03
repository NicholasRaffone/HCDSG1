import os
import csv
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

import numpy as np
import matplotlib.pyplot as plt
class SentimentAnalyzer:
    #create the sentiment analyzer object 
    def __init__(self):
        self.analyzer = SentimentIntensityAnalyzer()

    #analyze the sentiment of the comments appends it as a column to the dataframe 
    def analyze_sentiment_comments(self, filename):
        df = pd.read_csv(filename)
        df["sentiment"] = df["body"].apply(self.get_sentiment)
        return df
    #analyze the sentiment of post titles appends it as a column to the dataframe
    def analyze_sentiment_title(self, filename):
        df = pd.read_csv(filename)
        df["sentiment"] = df["title"].apply(self.get_sentiment)
        return df
    #returns the sentiment score of the text
    def get_sentiment(self, text):
        #checks if the comment body is null or not 
        if pd.isnull(text):
            return np.nan
        else:
            return str(self.analyzer.polarity_scores(text)["compound"])
    #creates a histogram of the sentiment scores of comments 
    def display_scores_comments(self,df):
        scores = df["sentiment"].astype(float)
        plt.hist(scores, bins=20, color='c', edgecolor='black', linewidth=1.2)
        plt.xlabel('Sentiment Score')
        plt.ylabel('Frequency')
        plt.title('Sentiment Analysis of True Crime Comments')
        plt.show()
    def display_scores_titles(self,df):
        scores = df["sentiment"].astype(float)
        plt.hist(scores, bins=20, color='c', edgecolor='black', linewidth=1.2)
        plt.xlabel('Sentiment Score')
        plt.ylabel('Frequency')
        plt.title('Sentiment Analysis of True Crime Titles')
        plt.show()
    
if __name__ == "__main__":
    sa = SentimentAnalyzer()
    df_comments = sa.analyze_sentiment_comments("truecrime_comments.csv")
    df_titles = sa.analyze_sentiment_title("truecrime_submissions_with_fields.csv")
    sa.display_scores_comments(df_comments)
    sa.display_scores_titles(df_titles)