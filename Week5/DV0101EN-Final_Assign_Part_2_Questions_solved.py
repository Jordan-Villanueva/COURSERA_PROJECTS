#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px


# Load the data using pandas
data = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/historical_automobile_sales.csv')

# Initialize the Dash app
app = dash.Dash(__name__)

dropdown_options = [
    {'label': 'Recession Period Statistics', 'value': 'Yearly Statistics'}]

# List of years 
year_list = [i for i in range(1980, 2024, 1)]

app.layout = html.Div([
    #TASK 2.1 Add title to the dashboard
    html.H1("Automobile Sales Statistics Dashboard", style={'textAlign': 'center', 'color': '#503D6', 'font-size': 24}),
    html.Div([#TASK 2.2: Add two dropdown menus
        # html.Label("Select Statistics:"),
          dcc.Dropdown(value = 'Select Statistics',id='dropdown-statistics', 
                   options=[
                           {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
                           {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'}
                           ],
                  placeholder='Select a report type',
                  style={'width':'80%','padding':'3px','font-size':'20px', 'text-align-last':'center'}),
          dcc.Dropdown(value = 'Select Year',id='select-year', 
                   options=[{'label':i,'value':i} for i in range(1980,2024)],
                  placeholder='Select a year',
                  style={'width':'80%','padding':'3px','font-size':'20px', 'text-align-last':'center'})
    ]),
    html.Div([#TASK 2.3: Add a division for output display
    html.Div(id='output-container', className='chart-grid')], style={'display':'flex'})
])

@app.callback(
    Output(component_id='select-year', component_property='disabled'),
    Input(component_id='dropdown-statistics',component_property='value'))

def update_input_container(value):
    if value =='Yearly Statistics': 
        return False
    else: 
        return True

@app.callback(
    Output(component_id='output-container', component_property='children'),
    [Input(component_id='select-year', component_property='value'), Input(component_id='dropdown-statistics', component_property='value')])


def update_output_container(selected_year, selected_statistics):
    global data 
    print(type(selected_year))
    if selected_statistics  == 'Recession Period Statistics':
        # Filter the data for recession periods
        recession_data = data[data['Recession'] == 1]
        #Plot 1 Automobile sales fluctuate over Recession Period (year wise) using line chart
        # grouping data for plotting
        yearly_rec=recession_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        # Plotting the line graph
        R_chart1 = dcc.Graph(
        figure=px.line(yearly_rec, x='Year', y='Automobile_Sales',
                title="Automobile sales over Recession Periods (year wise)"))

        # Plot 2: Calculate the average number of vehicles sold by vehicle type and represent as a Bar chart
        yearly_rec2 = recession_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        R_chart2 = dcc.Graph(
        figure=px.bar(
        yearly_rec2,
        x='Vehicle_Type',
        y='Automobile_Sales',
        title="Average number of vehicles sold by vehicle type over Recession Periods (year wise)",
        opacity=0.8  # Adjust opacity if needed
        ).update_layout(
        xaxis_title='Vehicle_Type',  # Add x-axis title
        yaxis_title='Average Sales'  # Add y-axis title
        )
        )
        # Plot 3 : Pie chart for total expenditure share by vehicle type during recessions
        exp_rec= recession_data.groupby(['Vehicle_Type'])['Advertising_Expenditure'].sum().reset_index()
        R_chart3 = dcc.Graph(
                    figure=px.pie(exp_rec,
                    values='Advertising_Expenditure',
                 names='Vehicle_Type',
                 title="Total expenditure share by vehicle type during recessions"
                )
        )
        # Plot 4: Bar chart for the effect of unemployment rate on vehicle type counts
        # Count occurrences of each vehicle type for each unemployment rate
        counts = recession_data.groupby(['unemployment_rate', 'Vehicle_Type']).size().reset_index(name='Count')
        bar_fig = px.bar(counts, x='unemployment_rate', y='Count', color='Vehicle_Type',
                 title='Count of Vehicle Types by Unemployment Rate During Recession Period',
                 labels={'unemployment_rate': 'Unemployment Rate', 'Count': 'Count'},
                 barmode='group')
        bar_fig.update_layout(xaxis_title='Unemployment Rate', yaxis_title='Count')  # Add axis titles
        R_chart4 = dcc.Graph(figure=bar_fig)


        return [
            html.Div(
                className='chart-item',
                children=[
                    html.Div(children=R_chart1),
                    html.Div(children=R_chart2)
                ],
                style={'display': 'flex'}
            ),
            html.Div(
                className='chart-item',
                children=[
                    html.Div(children=R_chart3),
                    html.Div(children=R_chart4)
                ],
                style={'display': 'flex'}
            )
        ]

    # Yearly Statistic Report Plots                             
    elif (selected_year and selected_statistics=='Yearly Statistics'):
        yearly_data = data[data['Year'] == selected_year]
        print(yearly_data)  # Debug statement to check the filtered data
                              
    # Plot 1 :Yearly Automobile sales using line chart for the whole period.
        yas= data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        Y_chart1 = dcc.Graph(
            figure=px.line(yas, x='Year', y='Automobile_Sales',
                title="Automobile Sales over Time")
        )
    # Plot 2 :Total Monthly Automobile sales using line chart.
        mas= yearly_data.groupby('Month')['Automobile_Sales'].sum().reset_index()
        Y_chart2 = dcc.Graph(
            figure=px.line(yearly_data, x='Month', y='Automobile_Sales',
                title='Total Monthly Automobile Sales over the year{}'.format(selected_year))
        )
    # Plot bar chart for average number of vehicles sold during the given year
        avr_vdata=yearly_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        Y_chart3 = dcc.Graph(figure=px.bar(avr_vdata,
        x='Vehicle_Type',
        y='Automobile_Sales',
        title='Average Vehicles Sold by Vehicle Type in the year {}'.format(selected_year)))
    
    
    # Plot 4 Total Advertisement Expenditure for each vehicle using pie chart
        expy= yearly_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        Y_chart4 = dcc.Graph(
                    figure=px.pie(expy,
                    values='Advertising_Expenditure',
                 names='Vehicle_Type',
                 title='Total advertising expenditure by vehicle type during year {}'.format(selected_year)
                )
        )


        return [
            html.Div(
                className='chart-item',
                children=[
                    html.Div(children=Y_chart1),
                    html.Div(children=Y_chart2)
                ],
                style={'display': 'flex'}
            ),
            html.Div(
                className='chart-item',
                children=[
                    html.Div(children=Y_chart3),
                    html.Div(children=Y_chart4)
                ],
                style={'display': 'flex'}
            )
        ]

    # Return an empty Div if no data is selected
    return html.Div()


if __name__ == '__main__':
    app.run_server()
    
