# ClickChecker... Every Click Matters

# Motivation
SEC has made public its [server log][log] files for its EDGAR system. The data describes how investors about how investors access corporate filings. Currently, it covers all the SEC EDGAR website traffic from 2003 to 2017.My bussiness use case is to understand the behaviors of users
By analyzing log data, enterprises can more readily identify potential threats and other issues, find the root cause, and initiate a rapid response to mitigate risks.

# Data 
##**SEC’s EDGAR Log dataset**
* 750 GB 
* 13M+ Filings/year
* 38K+ FormTypes
* 6B+ Requests

# Pipeline
![GitHub Logo](/docs/pipeline.png)
Format: ![Alt Text](url)

* Initially Logdata is stored in a S3 Bucket
* Spark convets the csv files to parquet
* Dash is used develop the web application
