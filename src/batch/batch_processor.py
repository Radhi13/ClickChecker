from  pyspark.sql import SparkSession,SQLContext
from pyspark.sql import functions as f
import boto3
from pyspark.sql.functions import regexp_replace, trim, lower

class BatchProcessor(object):
    def __int__(self):
        self.spark = SparkSession.builder.master("spark://ec2-18-210-3-218.compute-1.amazonaws.com:7077").appName("ClickerTicker").config("spark.executor.memory", "6gb").getOrCreate()
        self.sqlContext=SQLContext(self.spark)
        
    def sql_read(self):
        departments=[]
        s3= boto3.client('s3')
        response = s3.list_objects_v2(Bucket='queryresultsedgar', Delimiter='/')
        obj=response.get('CommonPrefixes')
        for obj in response.get('CommonPrefixes'):
            print(obj)
        
        for obj in response.get('CommonPrefixes'):
            print(str(obj.get('Prefix'))) 
            department = str(obj.get('Prefix')).replace("createEdgarSchema/","")
            print(department)
            departments.append(department)
        for i in range(0,len(departments)):
            print(departments[i])
        
        
if __name__=="__main__":
    sparkjob = BatchProcessor()
    reviews=sparkjob.sql_read()
