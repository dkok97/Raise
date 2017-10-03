import time
import plotly as py
import sys # for argv
# Comma Separated Values
# a common file format to store information in plain text
import csv 
#from HTMLParser import HTMLParser


go = py.graph_objs

INPUT_CSV_FNAME     = 'rssi_agg.csv'    # file name for input data
OUTPUT_GRAPH_FNAME  = 'rssi_plot.html'  # file name for output offline data
USERNAME            = 'username'        # your plot.ly username
PASSWORD            = 'password'        # your plot.ly password
OFFLINE             = True  # to plot graph to $(PWD)
ONLINE              = False # to plot graph to plot.ly/~USERNAME
AUTOREFRESH         = True # to enable autorefreshing of html file
DURATION_REFRESH    = "1"

# REPLACE USERNAME AND PASSWORD with your own. Create one at http://plot.ly
# NOT NEEDED FOR OFFLINE PLOTTING
# Run the statement once to use the cloud service 
# and access the plots at https://plot.ly/~YOURUSERNAME/
# Free version limited to 50 API Calls/Day

def htmlAutoRefresh():
    # to add the code to refresh the page and see graph in real time. 
    # content="10" represents duration

    with open(OUTPUT_GRAPH_FNAME, 'r+') as agg:
        #'r+' opens a file for both reading and writing. 
        # The file pointer will be at the beginning of the file
        agg.write('<html><head><meta http-equiv="refresh" content="1"/></head><body><script type="text/javascript">/**')

def generatePlot(offline=True, online=False, 
        input_csv_fname=INPUT_CSV_FNAME, output_graph_fname=OUTPUT_GRAPH_FNAME):
    with open(input_csv_fname, 'rb') as rssi:  # 'rb' stands for read in binary
        x = []
        y = []
        csvreader = csv.reader(rssi)
        for i, row in enumerate(csvreader):
            #R represents the row number
            x.append("R{} {}".format(i, row[0])) 
            y.append(row[1])

        data = [go.Bar(
            x=x, y=y,
            marker=dict(
                color='rgb(158,202,225)',
                line=dict(
                    color='rgb(8,48,107)',
                    width=1),
                ),
            opacity=0.8
            )]

        layout = go.Layout(
                annotations=[
                    dict(x=xi, y=yi,
                        # text on each bar. Can be unique.
                        # Change to text = xi 
                        # for displaying the value it represents
                        text=xi.split(" ")[0] ,

                        xanchor='center',
                        yanchor='bottom',
                        showarrow=False
                        ) for xi, yi in zip(x, y)],
                    # title of the graph
                    title='RSSI Strength in dBm',
                    )

        fig = go.Figure(data=data, layout=layout)

        if offline:
            py.offline.plot(fig, filename=output_graph_fname, auto_open=False)
        if online:
            py.plotly.plot(fig, filename='rssi-agg', auto_open=False)

if __name__ == "__main__":
    if len(sys.argv) == 8:
        OFFLINE             = bool(sys.argv[1])
        ONLINE              = bool(sys.argv[2])
        AUTOREFRESH         = bool(sys.argv[3])
        INPUT_CSV_FNAME     = sys.argv[4]
        OUTPUT_GRAPH_FNAME  = sys.argv[5]
        USERNAME            = sys.argv[6]
        PASSWORD            = sys.argv[7]
        DURATION_REFRESH    = sys.argv[8]

    print "{}: {}".format("OFFLINE", OFFLINE)
    print "{}: {}".format("ONLINE", ONLINE)
    print "{}: {}".format("AUTOREFRESH", AUTOREFRESH)
    print "{}: {}".format("INPUT_CSV_FNAME", INPUT_CSV_FNAME)
    print "{}: {}".format("OUTPUT_GRAPH_FNAME", OUTPUT_GRAPH_FNAME)
    print "{}: {}".format("USERNAME", USERNAME)
    print "{}: {}".format("PASSWORD", PASSWORD)
    print "{}: {}".format("DURATION_REFRESH", DURATION_REFRESH)
    
    if ONLINE:
        py.tools.set_credentials_file(
                username=USERNAME, 
                api_key=PASSWORD
                )
    
    generatePlot(offline=OFFLINE, online=ONLINE, 
            input_csv_fname=INPUT_CSV_FNAME,
            output_graph_fname=OUTPUT_GRAPH_FNAME)

#
#    if AUTOREFRESH:
#            htmlAutoRefresh()


##STREAMING CODE
#def stream_handler(message):
#    print(message['data'])
#my_stream = db.child("Events").stream(stream_handler)


#
#config = {
#    "apiKey": "AIzaSyDnhcfRNgARiKSgh0aHo4MRNZMEWvs6NQE",
#    "authDomain": "raise-1a3b2.firebaseapp.com",
#    "databaseURL": "https://raise-1a3b2.firebaseio.com/",
#    "storageBucket": "gs://raise-1a3b2.appspot.com"
#}
#
#firebase = pyrebase.initialize_app(config)
#
#db = firebase.database()
#

#users = db.child("Active").get()
#print(users.val())
