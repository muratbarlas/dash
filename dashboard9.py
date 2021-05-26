# Python version 3.8.3
# plotly 4.14.3
# dash 1.19.0
# dash-core-components 1.15.0
# dash-html-components 1.1.2
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash.dependencies import Input, Output
from plotly.subplots import make_subplots
from csv import reader
from numpy import interp

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__,
                external_stylesheets=external_stylesheets)  # external sheets are used to make the main dash background black

########### first dropdown ##########

# setting up the dropdown list for the top graph
dropdownData = pd.read_csv("output2.csv")  # creating a df from pedstats
dropdownData = dropdownData[
    ["Location", "Date", "APD", "Adherence12", "Adherence6", "Adherence3"]]  # only getting these columns

option_list = [{'label': x, 'value': x} for x in dropdownData['Location'].unique()]  # this is a list of dictionaries

# print(dropdownData)
option_list.insert(0, {'label': 'All locations', 'value': 'All locations'})
######################################


##### map graph start ###########
column_names = ["description", "x", "y"]
df = pd.read_csv("Cameras.csv", names=column_names)
x_cor = df.x.to_list()  # x coordinates of camera locations
y_cor = df.y.to_list()  # y coordinates of camera locations
loc = df.description.to_list()  # location names #lochere

location_apd_average = {}  # contains average apd number for each location, this is used to create the size of the marks on the camera map
dff_average = pd.read_csv("output2.csv")  # creating a df to find average apd for all locations
# before the february update PedStats.csv file was used

for index, row in dff_average.iterrows():
    if row['Location'] not in location_apd_average:
        location_apd_average[row['Location']] = [row['APD'], 1]

    else:
        location_apd_average[row['Location']][0] += row['APD']
        location_apd_average[row['Location']][1] += 1

for key, value in location_apd_average.items():
    location_apd_average[key] = value[0] / value[1]
# the two for loops above calculate the average apd for each location for the given dates in the csv, this information is needed for the
# bubble sizes on the map

list_size = []
for i in range(len(loc)):
    if loc[i] in location_apd_average:
        list_size.append(int(location_apd_average[loc[i]]) * 10)
        loc[i] = str(loc[i]) + ", APD at this locations is " + str(round(location_apd_average[loc[i]], 2))

    else:
        loc[i] = str(loc[i]) + ", no APD data."
        list_size.append(9)  # if there is no data size is 9

mapbox_access_token = open("mapbox_token.txt").read()  # token for the map API
fig_map = go.Figure(go.Scattermapbox(
    lat=y_cor,
    lon=x_cor,
    mode='markers',
    marker=go.scattermapbox.Marker(
        color="#6D92E2",
        # size=9
        size=list_size  # takes size, lat, and long from the lists described earlier
    ),
    hoverinfo="text",  # if this is missing coordinates are displayed
    hovertext=loc

))
fig_map.update_layout(
    autosize=True,
    mapbox=dict(
        accesstoken=mapbox_access_token,
        bearing=0,
        center=dict(
            lat=40.72,
            lon=-74
        ),
        pitch=0,
        zoom=10
    ),
)

margin = dict(l=10, r=10, t=40, b=0)

fig_map.update_layout(template="plotly_dark", title="Camera Locations", margin=dict(l=40, r=40, b=20, t=60))
##### map graph end ###########


df_pie = pd.read_csv("apr-mayComplaints.csv")
fig_pie = px.pie(df_pie, values='Reports', names='ComplaintType', color_discrete_sequence=px.colors.sequential.Blues_r)
fig_pie.update_layout(template="plotly_dark")
fig_pie.update_layout(title="Top 311 Complaints After the Pandemic")
fig_pie.update_layout(legend=dict(
    orientation="h",
    yanchor="bottom",
    y=-0.7,
    xanchor="right",
    x=1

))

apd_dict_new = {}  # includes apd for each date for all locations (it's from the summary table provided by Fan)
with open('PedStats3.csv', 'r') as read_obj:  # pedstats3 includes summary data provided by Fan
    csv_reader = reader(read_obj)
    for row in csv_reader:
        if row[0] != "Date":
            apd_dict_new[row[0]] = float(row[4])

# print(apd_dict_new)
# ---------------------------------------------------------------
# layout of everything
app.layout = html.Div([

    html.Div(children=[
        html.H1(children='C2SMART COVID-19 Data Dashboard - Sociability',
                style={"color": 'white', 'backgroundColor': '#111111', 'margin': 0, "text-align": "center",
                       'fontSize': 30, "margin-top": 20, "font-weight": "bold"}),
        html.P(["(Last Updated: February 2021)"],
               style={"color": 'white', 'fontSize': 15, "text-align": "center", "margin-bottom": 10}),

    ]),

    html.Div(style={"display": "flex", "justify-content": "center"}, children=[
        html.Div(style={'backgroundColor': "#2c2b2b", 'width': '40vh', 'display': 'inline-block', "class": "center",
                        'margin-right': 10},
                 children=[
                     html.H1(["Avg Safety Rate"],
                             style={"color": 'white', 'fontSize': 13, "text-align": "center", "margin-top": 10}),
                     html.H1(["95.0%"],
                             style={"color": 'white', 'fontSize': 40, "text-align": "center", "font-weight": "bold"}),
                     html.H1(["0.23% lower than the previous month"],
                             style={"color": 'white', 'fontSize': 13, "text-align": "center"})
                 ]
                 ),

        html.Div(style={'backgroundColor': "#2c2b2b", 'width': '40vh', 'display': 'inline-block', 'margin-right': 10},
                 children=[
                     html.H1(["Avg Pedestrian density (peds/frame)"],
                             style={"color": 'white', 'fontSize': 13, "text-align": "center", "margin-top": 10}),
                     html.H1(["1.23"],
                             style={"color": 'white', 'fontSize': 40, "text-align": "center", "font-weight": "bold"}),

                     html.H1(["0.14 higher than the previous month"],
                             style={"color": 'white', 'fontSize': 13, "text-align": "center"})
                 ]
                 ),

        html.Div(style={'backgroundColor': "#2c2b2b", 'width': '40vh', 'display': 'inline-block', 'margin-right': 10},
                 children=[
                     html.H1(["Camera Locations Screened"],
                             style={"color": 'white', 'fontSize': 13, "text-align": "center", "margin-top": 10}),
                     html.H1(["68"],
                             style={"color": 'white', 'fontSize': 40, "text-align": "center", "font-weight": "bold"}),
                     html.H1(["With 5 boroughs of NYC"],
                             style={"color": 'white', 'fontSize': 13, "text-align": "center"})
                 ]
                 )

    ]

             ),

    html.Div([
        dcc.Dropdown(
            id='my_dropdown',
            options=option_list,
            value="All locations",
            style={'width': '80vh', "margin-top": 30}

        ),

    ]),
    html.Div([

        dcc.Graph(id='the_graph', style={"margin-top": 30}),
        dcc.Graph(id='cases_graph'),
        html.P(["Slider"],
               style={"color": 'white', "margin-bottom": 10, "margin-left": 40, "fontSize": 15}),
        html.Div(style={"margin-left": 20}, children=[
            dcc.RangeSlider(
                id='my-range-slider',  # any name you'd like to give it
                marks={
                    0: 'April',  # key=position, value=what you see
                    1: 'May',
                    2: 'June',
                    3: 'July',
                    4: 'August',
                    5: 'September',
                    6: 'October',
                },

                max=6,
                value=[2, 6],
                dots=False,
                allowCross=False,
                step=0.5,
                updatemode='drag',

            )

        ]),

        html.P([
            "The formula for calculating the average pedestrian density is to sum all the pedestrian count for the specific location in one day (count every 30 seconds, 4 hours in total) divided by the number of counting. This means it is the average number of pedestrian for camera capture area during the specific time period (4 hours, sampling every 30 seconds)."],
            style={"color": 'white', "margin-left": 40}  # ,'margin-bottom':40, 'margin-left':80}
        )
    ]),

    html.Div([
        dcc.Graph(id='nyc-map', figure=fig_map),  # style={'display': 'inline-block', "margin-left":40}),
        html.P(["The closed-circuit television (CCTV) system is a valuable source of traffic condition information for",
                "many transportation systems. This work collected traffic video data from NYC Department of Transportation (NYCDOT) traffic cameras. The bubble sizes on the map are proportional to the overall APD for that location."],
               style={"color": 'white', "margin-left": 40}),  # 'display': 'inline-block', "margin-left":40}),

    ]),

    html.Div(
        children=[
            dcc.Graph(id='pie', figure=fig_pie),  # style={"margin-top": "40px"}),
            html.P(["Top 10 311 Complaint Types"],
                   style={"color": 'white', "margin-bottom": 10, 'fontSize': 20, "margin-top": 20}),
            dcc.Dropdown(
                id='my_dropdown2',
                options=[
                    {'label': "21 February - 21 March", 'value': 1},
                    {'label': "22 March - 22 April", 'value': 2},
                    {'label': "23 April - 11 May", 'value': 3}
                ],
                value=1,
                style={'width': '80vh', "margin-bottom": 30}

            ),
            dcc.Graph(id="the_table")
        ]
    ),

])

location = None


# ---------------------------------------------------------------
# @app.callback(  # callback for the first graphs location dropdown
#     Output(component_id='cases_graph', component_property='figure'),
#     [Input('my-range-slider', 'value')],
#
#
# )
#
# def update_cases_graph(my_range):
#     global date_list3
#     with open('dailyCovidCasesFormatted.csv', 'r') as read_obj:
#         # pass the file object to reader() to get the reader object
#         csv_reader = reader(read_obj)
#         # Iterate over each row in the csv using reader object
#         case_count =[]
#         for row in csv_reader:
#             if row[0] != "date_of_interest":
#                 if row[0] in date_list3:
#                     case_count.append(row[1])
#                 elif row[0] not in date_list3:
#                     case_count.append(0)
#
#     fig = px.scatter(x=date_list3, y=case_count)
#     print(date_list2)
#     print(case_count)
#     return fig
#
#



@app.callback(  # callback for the first graphs location dropdown
    Output(component_id='the_graph', component_property='figure'),
    Output(component_id='cases_graph', component_property='figure'),
    [Input(component_id='my_dropdown', component_property='value'), Input('my-range-slider', 'value')],

)
def update_graph(my_dropdown, dates_chosen):
    global location
    location = my_dropdown  # selected locations
    date_list = []  # available dates to be shown for that locations
    apd_list = []  # apd for those dates
    Adherence12 = []
    Adherence6 = []
    Adherence3 = []  # adherences for those dates
    apd_list2 = []  # average apd for those dates
    date_list2 = []

    counter = 0
    if my_dropdown == "All locations":
        with open('PedStats3.csv', 'r') as read_obj:
            # pass the file object to reader() to get the reader object
            csv_reader = reader(read_obj)
            # Iterate over each row in the csv using reader object
            for row in csv_reader:
                counter += 1
                if row[0] != "Date":
                    date_list.append(row[0])
                    date_list2.append(row[0])
                    Adherence3.append(float(row[1]))
                    Adherence6.append(float(row[2]))
                    Adherence12.append(float(row[3]))
                    apd_list2.append(float(row[4]))

    if my_dropdown != "All locations":
        for index, row in dropdownData.iterrows():
            if row["Location"] == my_dropdown:
                date_list.append(row["Date"])
                date_list2.append(row["Date"])
                if row["Date"] in apd_dict_new:
                    apd_list2.append(apd_dict_new[row["Date"]])
                apd_list.append(row["APD"])
                Adherence12.append(row["Adherence12"])
                Adherence6.append(row["Adherence6"])
                Adherence3.append(row["Adherence3"])

    start = int(interp(dates_chosen[0], [0, 6], [0, len(date_list)]))  # because there are 7 months now
    end = int(interp(dates_chosen[1], [0, 6], [0, len(date_list)]))

    date_list = date_list[start:end]
    apd_list = apd_list[start:end]
    Adherence12 = Adherence12[start:end]
    Adherence6 = Adherence6[start:end]
    Adherence3 = Adherence3[start:end]
    apd_list2 = apd_list2[start:end]
    date_list2 = date_list2[start:end]
    date_list3 = date_list2

    date_list_nyc_cases = []
    hospital_count = []

    fig_scatter = make_subplots(specs=[[{"secondary_y": True}]])

    fig_scatter.update_layout(template="plotly_dark",
                              title="Average Pedestrian Density (APD) and Safety Rate Across Locations",
                              margin=dict(t=60, b=30))

    # fig_scatter.update_layout(title="Average Pedestrian Density (APD) and Safety Rate Across Locations",margin=dict(t=60))

    fig_scatter.add_bar(x=date_list, y=Adherence3, name="Distance > 3ft", marker={"color": "#c4d3f3"})
    fig_scatter.add_bar(x=date_list, y=Adherence6, name="Distance > 6ft", marker={"color": "#6D92E2"})
    fig_scatter.add_bar(x=date_list, y=Adherence12, name="Distance > 12ft", marker={"color": "#2b3a5a"})

    if my_dropdown != "All locations":
        fig_scatter.add_trace(
            go.Scatter(x=date_list, y=apd_list, mode='lines+markers', name="APD for the selected location",
                       marker=dict(color="green")), secondary_y=True)
    elif my_dropdown == "All locations":
        fig_scatter.add_trace(
            go.Scatter(x=date_list, y=apd_list2, mode='lines+markers', name="APD for the selected location",
                       marker=dict(color="green")), secondary_y=True)
    fig_scatter.add_trace(
        go.Scatter(x=date_list2, y=apd_list2, mode='lines+markers', name="APD for all locations",
                   marker=dict(color="orange")), secondary_y=True)

    fig_scatter.update_yaxes(title_text="Safety rate", secondary_y=False)
    fig_scatter.update_yaxes(title_text="APD", secondary_y=True)

    fig_scatter.update_yaxes(range=[0.5, 1], secondary_y=False)
    fig_scatter.update_yaxes(tickformat=',.0%', secondary_y=False)

    fig_scatter.update_yaxes(range=[0, 10], secondary_y=True)

    fig_scatter.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.5,
        xanchor="right",
        x=1,

    ))

    with open('dailyCovidCasesFormatted.csv', 'r') as read_obj:
        # pass the file object to reader() to get the reader object
        csv_reader = reader(read_obj)
        # Iterate over each row in the csv using reader object
        case_count =[]
        row_count = 0
        marker = False
        for row in csv_reader:
            if row[0] != "date_of_interest":
                row_count+=1
                if row[0] == date_list2[0]:
                    marker =True
                if marker == True:
                    date_list_nyc_cases.append(row[0])
                    case_count.append(int(row[1]))
                    hospital_count.append(int(row[3]))
                if row[0] == date_list2[len(date_list)-1]:
                    break

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=date_list_nyc_cases, y=case_count,
                             mode='lines+markers', name="Daily cases",  marker = dict(color = 'rgba(109, 146, 226, 0.8)', size=4) , line=dict( width=1)
                             ))



    #fig.add_trace(go.Scatter(x=date_list_nyc_cases, y=hospital_count,
                             #mode='lines+markers', name="Daily Hospitilizations",marker=dict(color='rgba(255, 165, 0, 0.8)', size=4), line=dict( width=1)
                             #))

    fig.add_bar(x=date_list_nyc_cases, y=hospital_count, name="Daily Hospitilizations", marker=dict(color='rgba(255, 165, 0, 0.8)'))


    fig.update_layout(template="plotly_dark", title="Daily Covid Cases in NYC", height=350)

    fig.update_xaxes(title_text="Dates")
    fig.update_yaxes(title_text="Case count")

    fig.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-1,
        xanchor="right",
        x=1,

    ))

    return fig_scatter, fig


@app.callback(
    # callback for the second dropdown (dropdown for the 311 table at the bottom)
    Output(component_id='the_table', component_property='figure'),
    [Input(component_id='my_dropdown2', component_property='value')]
)
def update_table(my_drowdown2):
    if my_drowdown2 == 1:  # values are defined in layout
        table1_data = pd.read_csv("311_1.csv")
        fig_table1 = go.Figure(data=[go.Table(
            header=dict(values=list(table1_data.columns), ),
            cells=dict(values=[table1_data.MonthRank, table1_data.ComplaintType, table1_data.Reports]))
        ])
        fig_table1.update_layout(template="plotly_dark", title="21 February - 21 March",
                                 margin=dict(l=10, r=10, t=40, b=0))
        return fig_table1
    elif my_drowdown2 == 2:
        table2_data = pd.read_csv("311_2.csv")
        fig_table2 = go.Figure(data=[go.Table(
            header=dict(values=list(table2_data.columns), ),
            cells=dict(values=[table2_data.MonthRank, table2_data.ComplaintType, table2_data.Reports], ))
        ])
        fig_table2.update_layout(template="plotly_dark", title="22 March - 22 April",
                                 margin=dict(l=10, r=10, t=40, b=0))
        return fig_table2

    elif my_drowdown2 == 3:
        table3_data = pd.read_csv("311_3.csv")
        fig_table3 = go.Figure(data=[go.Table(
            header=dict(values=list(table3_data.columns), ),
            cells=dict(values=[table3_data.MonthRank, table3_data.ComplaintType, table3_data.Reports], ))
        ])
        fig_table3.update_layout(template="plotly_dark", title="23 April - 11 May", margin=dict(l=10, r=10, t=40, b=0))
        return fig_table3


if __name__ == '__main__':
    app.run_server(debug=True)