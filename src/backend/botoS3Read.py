import time
import boto3
import pandas as pd
import io

class QueryAthena:

    def __init__(self, query, database):
        self.database = database
        self.folder = 'test/'
        self.bucket = 'queryresultsedgar'

        self.s3_input = 's3://' + self.bucket + '/Unsaved/2020/01/30/'
        self.s3_output =  's3://' + self.bucket + '/' + self.folder
        self.region_name = 'us-east-1'
        self.aws_access_key_id = ACCESS_KEY
        self.aws_secret_access_key = SECRET_KEY
        self.query = query

    def load_conf(self, q):
        try:
            self.client = boto3.client('athena',
                              region_name = self.region_name,
                              aws_access_key_id = self.aws_access_key_id,
                              aws_secret_access_key= self.aws_secret_access_key)
            response = self.client.start_query_execution(
                QueryString = q,
                    QueryExecutionContext={
                    'Database': self.database
                    },
                    ResultConfiguration={
                    'OutputLocation': self.s3_output,
                    }
            )
            self.filename = response['QueryExecutionId']
            print('Execution ID: ' + response['QueryExecutionId'])

        except Exception as e:
            print(e)
        return response

    def run_query(self):
        queries = [self.query]
        for q in queries:
            res = self.load_conf(q)
        try:
            query_status = None
            while query_status == 'QUEUED' or query_status == 'RUNNING' or query_status is None:
                query_status = self.client.get_query_execution(QueryExecutionId=res["QueryExecutionId"])['QueryExecution']['Status']['State']
                print(query_status)
                if query_status == 'FAILED' or query_status == 'CANCELLED':
                    raise Exception('Athena query with the string "{}" failed or was cancelled'.format(self.query))
                time.sleep(10)
            print('Query "{}" finished.'.format(self.query))

            df = self.obtain_data()
            return df

        except Exception as e:
            print(e)

    def obtain_data(self):
        print(self.folder + self.filename)

        try:
            self.resource = boto3.resource('s3',
                                  region_name = self.region_name,
                                  aws_access_key_id = self.aws_access_key_id,
                                  aws_secret_access_key= self.aws_secret_access_key)

            response = self.resource \
            .Bucket(self.bucket) \
            .Object(key= self.folder + self.filename + '.csv') \
            .get()

            return pd.read_csv(io.BytesIO(response['Body'].read()), encoding='utf8')
        except Exception as e:
            print(e)


if __name__ == "__main__":
    d2 = 'ciklookdb'
    d1 = 's3_edgarweb_logs_db'
    t1 = 'weblogstestedgardata'
    t2 = 'cik'

    query_1 ="""SELECT web.ip,web.cik,count(web.cik) as ct,c.title
    FROM %s.%s as web
    inner JOIN %s.%s as c ON web.cik = c.cik
    where web.date between '2016-06-23'and '2017-06-29'
    group by web.cik,c.title,web.ip
    order by ct desc
    limit 10""" % (d1,t1,d2,t2)
    qa = QueryAthena(query=query_1, database='boto1_database')
    dataframe = qa.run_query()
    print(dataframe)

