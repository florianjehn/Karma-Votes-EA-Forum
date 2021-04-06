# Getting a feel for karma and votes in the EA Forum

This repository contains the data and code used to analyze how the karma and votes in the EA Forum developed over time. 
 
Workflow:
* Extracted forum post data from GraphiQL with the query in "query_for_all_posts.txt".
* Used "clean_query.py" to bring the output of GraphiQL into a reasonable format and saved it as "cleaned_data.csv".
* Did the calculations and plotting in "plotting.py".
