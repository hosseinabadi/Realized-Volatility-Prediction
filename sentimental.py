"""
    code which was run on EPFL's GPU
"""


from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
nltk.download('vader_lexicon')
import pandas as pd


def text_sentimental(df):
    
    """
    function to compute sentimental analysis on the headlines of financial news
    'SentimentIntensityAnalyzer' is used for this task

    Args:
        pd.DataFrame: dataframe which containes in a column the link of the text that has to be analyzed
        

    Returns:
        pd.DataFrame: same dataframe as the one in the input, with financial sentimental analysis added
    """
    
    for index, row in df.iterrows():

        text = row['title']
        
        # Initialise sentiment analyser    
        sid = SentimentIntensityAnalyzer()
        # Get positive, negative, neutral and compound scores
        polarity = sid.polarity_scores(text)

        # Update the DataFrame with the sentiment scores
        df.loc[index, 'positivity_text'] = polarity['pos']
        df.loc[index, 'neutrality_text'] = polarity['neu']
        df.loc[index, 'negativity_text'] = polarity['neg']
        df.loc[index, 'compound_text'] = polarity['compound']    
    
    return df

df = pd.read_csv('/home/aolarite/JOB/sp500_news.csv')

df = text_sentimental(df)

df.to_csv('/home/aolarite/JOB/sp500_news_and_sentimental.csv')