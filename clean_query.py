# -*- coding: utf-8 -*-
"""
Created on Wed Mar 31 14:04:56 2021

@author: Florian Jehn
"""

import pandas as pd

# Read the file
with open("query_results_posts.txt", "r", encoding='utf-8') as all_posts_file:
    text = all_posts_file.read()

# Seperate the posts from the rest
posts, extensions = text.split('"extensions"')

# Split into single posts
seperated_posts = posts.strip().replace("\t","").replace("\n","").replace("{","").replace("}","").split('"meta": false')

all_posts_dict = {}

# Create a dictionary of all posts
for i, post in enumerate(seperated_posts):
    # Skipy empty ones
    if "allVotes" in post:
        meta_stuff, votes = post.split('"allVotes"')
    else:
        continue
    all_meta = meta_stuff.split(",")
    # Skip the fluff at the beginning of the file
    if i == 0:
        all_meta = all_meta[1:]
    # Remove the double mentioning of user
    all_meta[-2] = all_meta[-2].replace('"username":',"")
    single_post_dict = {}
    for meta in all_meta:            
        meta = meta.strip()
        # skip emtpy entries
        if len(meta) < 3:
            continue
        # skip entries without colon, as they contain only some random characters
        # as some titles contain commas
        if ": " in meta:
            splitted = meta.split(": ")    
            single_post_dict[splitted[0].replace('"',"")] = splitted[1].strip()
    # Save the votes as list of up and downvotes
    cleaned_votes = votes.replace('"voteType"',"").replace("[","").replace("]","").replace(" ","").replace(":","").replace('"',"").split(",")
    single_post_dict["Big Upvote"] = cleaned_votes.count("bigUpvote")
    single_post_dict["Big Downvote"] = cleaned_votes.count("bigDownvote")
    single_post_dict["Small Upvote"] = cleaned_votes.count("smallUpvote")
    single_post_dict["Small Downvote"] = cleaned_votes.count("smallDownvote")

    all_posts_dict[i] = single_post_dict
    
    
all_posts_df = pd.DataFrame(all_posts_dict).transpose()
# Remove id column
del(all_posts_df["_id"])
# Get the date right
all_posts_df.index = pd.to_datetime(all_posts_df["postedAt"], format='"%Y-%m-%dT%H:%M:%S.%fZ"')
del(all_posts_df["postedAt"])
# Remove the clutter we accumlated on the ride
all_posts_df = all_posts_df[all_posts_df.columns[:9]]
# Save
all_posts_df.to_csv("cleaned_data.csv",sep=";")

#all_posts_df.groupby(all_posts_df.index.year).count().plot(kind="bar")
        
        
        
    
