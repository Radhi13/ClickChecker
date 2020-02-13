from pyspark import SparkContext
from pyspark.sql import SQLContext,SparkSession
from pyspark.sql.types import *
#import boto3
   
#s3 = boto3.resource('s3')
#my_bucket = s3.Bucket('testedgardata')
 
#for file in my_bucket.objects.all():
#    print("dt=" + file.key[3:11])


if __name__ == "__main__":

    spark = SparkSession.builder \
        .appName("CSVToParquet") \
        .getOrCreate()


    schema =StructType([
    StructField("ip",StringType(),True),
    StructField("date",StringType(),True),
    StructField("time",StringType(),True),
    StructField("zone",DoubleType(),True),
    StructField("cik",StringType(),True),
    StructField("accession",StringType(),True),
    StructField("extention",StringType(),True),
    StructField("code",DoubleType(),True),
    StructField("size",DoubleType(),True),
    StructField("idx",DoubleType(),True),
    StructField("norefer",DoubleType(),True),
    StructField("noagent",DoubleType(),True),
    StructField("find",DoubleType(),True),
    StructField("crawler",DoubleType(),True)
    ])
 
    df = spark.read \
         .schema(schema) \
         .option("delimiter",",") \
         .csv('s3a://testedgardata/log20170629.csv',header=True)
    
    df.write.format("parquet").mode("overwrite").save('s3a://parquet2016edgarlog/test3')
    #df.write.parquet('s3a://parquet2016edgarlog/test2',mode="overwrite") 
