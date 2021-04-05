# -*- coding: utf-8 -*-
"""
Created on Wed Mar 31 15:38:32 2021

@author: Florian Jehn
"""

import pandas as pd
import matplotlib.pyplot as plt

# Get the data
df = pd.read_csv("cleaned_data.csv", sep=";", index_col=0)
df.index = pd.to_datetime(df.index)

def controversy(upvotes, downvotes):
    """
    Calculates controversy based on the reddit approach
    https://github.com/reddit-archive/reddit/blob/master/r2/r2/lib/db/_sorts.pyx#L60
    """
    if downvotes <= 0 or upvotes <= 0:
        return 0
    
    magnitude = downvotes + upvotes
    balance = downvotes / upvotes if upvotes > downvotes else upvotes / downvotes
    
    return magnitude ** balance

# prep data
# Only use data beginning in 2014
df = df[df.index.year > 2013]
# Calc total votes
df["Upvotes"] = df["Big Upvote"] + df["Small Upvote"]
df["Downvotes"] = df["Big Downvote"] + df["Small Downvote"]
df["Controversy"] = df[["Upvotes", "Downvotes"]].apply(lambda x: controversy(*x), axis=1)





df["Controversy"].groupby([df.index.year, df.index.month]).mean().rolling(5).mean().plot()