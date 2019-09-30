# FootyDash

### A Soccer Analytics Dashboard and a Capstone Project.

## Introduction
The purpose of this dashboard is to display soccer data in a digestible way. In the past few years we've finally seen an explosion within the soccer community to actually use and digest data on the great game to better the performance of our favorite teams. With that being said, I want to build out my own analysis on the teams of each major European league (only because this is the easiest to get information on). I had previously built this dashboard using the tools I knew before taking the Data Engineering course on Udacity, but now with my new found skills I believe I can create something much more robust and concise. 

## The Process 
Getting soccer data isn't necessarily easy to come by unfortunately. Soccer has yet to reach that level of data authenticity where people are using it for their own analysis or their own projects, which doesn't mirror American sports at all. To start we obviously need information, and where do we get information? The internet! Fortunately for us we have this phenomenal website [http://www.football-data.co.uk/data.php] which has a ton of CSV's worth of historical data and current weekly match data (think things like wins, draws. losses, shots, fouls etc). Now I know this isn't the greatest bit of information but for now this will do. Now for the steps:

1. Get the initial data. Now this can be done one of two ways. Write a selenium script to go through each link and click the CSV downloads to then save the CSV, or just manually grabbing each CSV for each league. This in some way will need to get automated in the future.
2. Once we have the CSV's we need (Serie A, Bundesliga, Premier League ETC) we can then create an S3 bucket in AWS to store all of this information. For this we can use python to iterate through a directory and upload them individually relative to the league and division (Prem or Championship)
3. So, now that we have all this information we need to create the subset of tables to warehouse into an RDS instance or Redshift. For right now, I want to upload all this data into one table, as it isn't too much information to begin with. Then from there split it up into tables we can pull from quicker and easier. 
4. Now that the queries are all set we can focus on actually inserting the information into our tables from S3. 
5. Possibly creating an Airflow DAG to run these tasks as the season continues throughout the year as we would obviously like real time data. 
6. Using our queries we've inserted the data and it lives! Now we can build a web app to display the information in either Plotly Dash or Django 

## The ETL Pipeline
An Image of what I believe will be the data pipeline:

CSV's -> S3 -> Creating tables/inserts -> Redshift/RDS -> Airflow tasks -> Analytics Application (plotly dash/django app) 


## What you need.
First and foremost you will need to create an AWS account with Amazon and you will need python 3.x on your machine. This should take no time at all. From there you will also need 
to create an IAM user, since we will need special permissions for this account. Specifically, read/write to S3 and read/write to
Redshift. The code will handle actually creating the bucket/DB. Remember that the Key and Secret comes from your IAM role credentials, 
so make sure to save those somewhere safe when you create the user. 

Lastly make sure to install everything from the requirements.txt file as you will need it. 


    KEY = {'Enter Access Key Here'}
    SECRET = {'Enter Secret Key Here'}
    BUCKETNAME = {'Enter Bucket Name Here'}
    REDSHIFT_NAME = {'Enter Name Here}
    
This will be updated as I work on this project. 