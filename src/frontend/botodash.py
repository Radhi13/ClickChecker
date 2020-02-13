import dash
import dash_core_components as dcc
import dash_html_components as html
from datetime import datetime as dt
import s3fs
from s3fs.core import S3FileSystem
import io
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import psycopg2

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

def connect():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = config()
 
        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
      
        # create a cursor
        cur = conn.cursor()
        
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')
 
s3_f = s3fs.S3FileSystem(anon=False)
with s3_f.open('radhika-queryresultsedgar/boto3Output/e25d04e4-c891-4ff4-824a-28cbaddb55a2.csv', 'rb') as f:
    df = pd.read_csv(f)
    df.columns = ['IP ADDR', 'COMPANYKEY','COUNT','COMPANY']

def generate_table_cik():
    sql = "select web.cik,count(web.cik) as ct ,c.company from aprEdgar as web inner join ciklookup as \
    c on CAST(web.cik as float) = cast(c.cik as int) where web.date = '2016-04-13' and web.code = 200 AND web.idx = 0 \
    AND web.crawler = 0 group by web.cik,c.company order by ct desc limit 10;"

    dx = pd.read_sql(sql,conn)
    print(dx.columns)
    dx.columns = ['CIK', 'COUNT','COMPANY']
    print(dx.columns)

    return html.Table(className="table",
          children=[
              html.Thead(
                  html.Tr(
                      children=[
                          html.Th(col.title()) for col in dx.columns.values]
                      )
                  ),
              html.Tbody(
                  [
                  html.Tr(
                      children=[
                          html.Td(data) for data in d]
                      )
                   for d in dx.values.tolist()])
              ]
    )
def get_ip_graph():
    # sql = "select web.ip,count(web.code) as ct from aprEdgar as web where web.date = '2016-04-13' \
    # and web.code  = 320 AND web.idx = 0 AND web.crawler = 0 group by web.ip order by ct desc limit 10;"
    #
    # dx = pd.read_sql(sql,conn)
    # print(dx.columns)
    #dx.columns = ['CIK', 'COUNT','COMPANY']
    #print(dx.columns)

    gf = pd.read_parquet(path= 's3://radhika-parquet2016edgarlog/2016/parquet/dt=20160413/part-00001-194d8004-379e-4016-9f4e-c7abbcd94d56-c000.snappy.parquet')
    grouped = gf.groupby(['ip','code']).agg({'code':['count']})
    grouped.columns = ['count']
    print(grouped.columns)
    grouped = grouped.reset_index()
    grouped = grouped.loc[grouped['code'] == 200]
    grouped = grouped.sort_values('count', ascending=False).head(15)

    #fig = px.line(grouped, x='time', y='count')
    fig = go.Figure([go.Scatter(x=grouped['ip'], y=grouped['count'])])
    #fig = go.Figure([go.Scatter(x=dx['ip'], y=dx['ct'])])
    return dcc.Graph(
        id='example-graph-4',
        figure=fig,
        )
def get_date_graph():
    rf = pd.read_parquet(path= 's3://radhika-parquet2016edgarlog/2016/parquet/dt=20160413/part-00001-194d8004-379e-4016-9f4e-c7abbcd94d56-c000.snappy.parquet')
    grouped = rf.groupby(['time','code']).agg({'code':['count']})
    grouped.columns = ['count']
    grouped = grouped.reset_index()
    #grouped = grouped.sort_values('time', ascending=False)
    x = grouped.loc[grouped['code'] == 200]
    y = grouped.loc[grouped['code'] > 200]
    #fig = px.line(grouped, x='time', y='count')
    #fig = go.Figure([go.Scatter(x=grouped['time'], y=grouped['count'])])
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x.time, y=x['count'], name="Right Clicks",
                             line_color='deepskyblue'))

    fig.add_trace(go.Scatter(x=y.time, y=y['count'], name="Wrong Clicks",
                             line_color='dimgray'))

    fig.update_layout(title_text='Time Series with Rangeslider',
                      xaxis_rangeslider_visible=True)
    return dcc.Graph(
        id='example-graph-2',
        figure=fig,
        )

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.config.suppress_callback_exceptions = True

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

index_page = html.Div([

    html.H1('Every CLick Matters!!!!',style={'color': 'blue','font-weight': 'bold','text-align': 'center'}),
    html.H2('Top 10 Companies visited - April 13 2016'),
    html.H5(generate_table_cik(),style={'width':'50%', 'height':'100%','float':'left'}),
    html.H2('Top 10 IP Address accessed EDGAR - April 13 2016'),
    html.H5(get_ip_graph(),style={'width':'50%', 'height':'100%','float':'right'}),
    dcc.Link('Go to Page 1', href='/page-1'),
    html.Br(),
])


render_graph = html.Div([
    html.H5(get_date_graph()),
    html.Br(),
])

page_1_layout = html.Div([
    html.H4('Select Date : Get detials of clicks in the time range'),

    dcc.DatePickerSingle(
        id='date-picker',
        min_date_allowed=dt(1995, 8, 5),
        max_date_allowed=dt(2017, 9, 19),
        initial_visible_month=dt(2017, 8, 5),
        date=str(dt(2016,4,13))
    ),

    html.Button('Submit', id='button'),
    html.Div(id='page-1-content'),
    html.Br(),
    dcc.Link('Go back to home', href='/'),
])

@app.callback(
    dash.dependencies.Output('page-1-content', 'children'),
    [dash.dependencies.Input('button', 'n_clicks'),dash.dependencies.Input('date-picker', 'date')])
#get datestring
def update_output(n_clicks,date):
    string_prefix = 'You have selected: '
    if date is not None:
        print('date',date)
        date = dt.strptime(date.split(' ')[0], '%Y-%m-%d')
        date_string = date.strftime('%B %d, %Y')
        if (n_clicks is not None):
            get_date_graph()
            return render_graph , string_prefix + date_string
        else:
            return string_prefix + date_string + " But need to hit submit button to see the graph"

    if len(string_prefix) == len('You have selected: '):
        return 'Select a date to see it displayed here'
    else:
        return string_prefix ,render_graph

# Update the index
@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/page-1':
        return page_1_layout
    elif pathname == '/page-2':
        return page_2_layout
    else:
        return index_page

if __name__ == '__main__':
    connect();	
    app.run_server(host='ec2-3-91-180-95.compute-1.amazonaws.com',port=8080)

cur.close()
conn.close()
