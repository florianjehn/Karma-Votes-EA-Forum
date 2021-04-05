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


def plot_nicer(ax):
    """Takes an axis objects and makes it look nicer"""
    alpha=0.7
    for spine in ax.spines.values():
      spine.set_color("white")
    # Make text grey
    plt.setp(ax.get_yticklabels(), alpha=alpha)
    plt.setp(ax.get_xticklabels(), alpha=alpha)
    ax.set_xlabel(ax.get_xlabel(), alpha=alpha)
    ax.set_ylabel(ax.get_ylabel(), alpha=alpha)
    ax.set_title(ax.get_title(), alpha=alpha)
    ax.set_xticklabels(ax.get_xticklabels(),rotation=90)
    ax.grid(True, color="lightgrey")
    ax.tick_params(axis=u'both', which=u'both',color="white")
    legend = ax.get_legend()
    for text in legend.get_texts():
        text.set_color("#676767")
    fig = plt.gcf()
    fig.set_size_inches(10,5)


# prep data
# Only use data beginning in 2014
df = df[df.index.year > 2013]

# Calculate relative base score (karma of posts normalized by mean of the month)
monthly_mean_score_karma = df["baseScore"].groupby([df.index.year, df.index.month]).mean()
df["Index Year Month"] = list(zip(df.index.year, df.index.month))
df["Monthly Mean Karma"] = df["Index Year Month"].map(monthly_mean_score_karma)
df["Scaled Karma"] = df["baseScore"] / df["Monthly Mean Karma"]

# Calc controversy
df["Upvotes"] = df["Big Upvote"] + df["Small Upvote"]
df["Downvotes"] = df["Big Downvote"] + df["Small Downvote"]
df["Controversy"] = df[["Upvotes", "Downvotes"]].apply(lambda x: controversy(*x), axis=1)

# Plot 
# Karma
ax1 = df["baseScore"].groupby([df.index.year, df.index.month]).mean().rolling(3).mean().plot(label="Three month rolling mean")
ax1.set_title("Karma in the EA Forum over time")
ax1.legend()
ax1.set_ylabel("Relative Karma")
ax1.set_xlabel("Date")
ax1.set_ylim(0,36)

plot_nicer(ax1)
plt.savefig("karma.png", dpi=300, bbox_inches="tight")
plt.close()

# Controversy
ax2 = df["Controversy"].groupby([df.index.year, df.index.month]).mean().rolling(3).mean().plot(label="Three month rolling mean")
ax2.set_title("Controversy in the EA Forum over time")
ax2.set_ylabel("Controversy")
ax2.legend()
ax2.set_xlabel("Date")
ax2.set_ylim(0,1.7)
plot_nicer(ax2)
plt.savefig("controversy.png", dpi=300, bbox_inches="tight")
plt.close()

