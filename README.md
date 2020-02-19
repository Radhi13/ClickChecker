# ClickChecker... Every Click Matters
# Table of Content
1. [Motivation](#Motivation)
2. [Data](#Data)
2. [Pipeline](#Pipeline)
## Motivation
SEC has made public its [server log][log] files for its EDGAR system. The data describes how investors about how investors access corporate filings. Currently, it covers all the SEC EDGAR website traffic from 2003 to 2017.My bussiness use case is to understand the behaviors of users
By analyzing log data, enterprises can more readily identify potential threats and other issues, find the root cause, and initiate a rapid response to mitigate risks.

## Data 
**SEC’s EDGAR Log dataset**
* 750 GB 
* 13M+ Filings/year
* 38K+ FormTypes
* 6B+ Requests

## Pipeline
![GitHub Logo](/docs/pipeline.png)

* Initially SEC's EDGAR Logdata is stored in a S3 Bucket 
* Spark convets the csv files to parquet file format
* AWS Athena is use to query the partioned data
* Dash is used to develop the web application

# Presentation link
* Link to the presentation: [ClickChecker](https://docs.google.com/presentation/d/1Wpjc7b85ut5BtaOwysQbTulW6dZ_S2j5ONbN9iG-YVk/edit#slide=id.p)
* Link to my websites: [strategicanalytics](http://strategicanalytics.club/)

