import numpy as np
import pandas as pd
from IPython.display import display,Image,HTML # Allows the use of display() for DataFrames
import HelperFunctions as hf
import Visualizations as viz

import plotly
import plotly.graph_objects as go
from plotly.offline import iplot
import plotly.graph_objs as go
import plotly.express as px

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

from ipywidgets import widgets

    
def multi_line(df):
    
    x = df['year']
    y1 = df['Export_Value'].astype(float)/1000
    y2 = df['Import_Value'].astype(float)/1000
    

    fig, ax = plt.subplots()
    plt.xlabel('Year')
    plt.ylabel('USD (Millions)')
    plt.title('Export vs. Import')
    
    line1, = ax.plot(x, y1, color='lightblue', marker='o', markerfacecolor='blue', markersize=12, linewidth=4)
    line2, = ax.plot(x, y2, color='lightgreen', marker='o',  markerfacecolor='olive', markersize=12, linewidth=4)
    
    ax.legend((line1, line2), ('Export Value', 'Import Value'), loc='upper right', shadow=True)

    def update(num):
        line1.set_data(x[:num+1], y1[:num+1]) 
        line2.set_data(x[:num+1], y2[:num+1])
        return line1,line2,   
    
    ani = animation.FuncAnimation(fig, update, len(x),interval=200, blit=True)
    plt.close() ## This is to prevent a static plot from appearing as output
    ani.save('Export_Import_MultiLine.gif')
    return ani

def scatter_plot(df,x_val,y_val,frame_,group_,title_):
    
    plot_ = px.scatter(df, x=x_val, y=y_val, animation_frame=frame_,
               animation_group=group_,size=x_val, color=group_, hover_name=group_,
               log_x=True, 
               size_max=70,
               range_x=[df[x_val].min(),df[x_val].max()], 
               range_y=[df[y_val].min(),df[y_val].max()],
               title=title_)
    return plot_

def bar_dropdown(df):
    #df = merge_df
    df_initial = df[(df['Commodity']=='COTTON.') & (df['country'] == "IRAQ")]
    df2 = df_initial[['year','Export_Value','Import_Value']].groupby(['year']).sum().reset_index()


    drop_down_1 = widgets.Dropdown(
        description='Commodity:   ',
        value = 'COTTON.',
        options=df['Commodity'].unique().tolist()    )

    drop_down_2 = widgets.Dropdown(
        options=list(df['country'].unique()),
        value = 'IRAQ',
        description='Country:')


    # Assign an empty figure widget with two traces
    trace1 = go.Bar(x=df2['year'],y = df2['Export_Value'], name='Export Value')
    #trace1
    trace2 = go.Bar(x=df2['year'], y = df2['Import_Value'], name='Import Value')

    g = go.FigureWidget(data=[trace1,trace2],
                        layout=go.Layout(
                            title=dict(
                                text='Export vs Import '
                            ),
                            barmode='group'
                        ))

    def response(change):
        filter_list = [i and j for i, j in
                               zip(df['Commodity'] == drop_down_1.value
                                   , df['country'] == drop_down_2.value
                                  )]
        temp_df = df[filter_list]

        y1 = temp_df['Export_Value']
        #print(x1)
        y2 = temp_df['Import_Value']
        x1 = temp_df['year']
        with g.batch_update():
            g.data[0].x = x1
            g.data[0].y = y1
            g.data[1].x = x1
            g.data[1].y = y2
            #g.layout.barmode = 'overlay'
            g.layout.xaxis.title = 'Year'
            g.layout.yaxis.title = 'value'

            #g.layout.yaxis = temp_df['year']


    drop_down_1.observe(response, names="value")
    drop_down_2.observe(response, names="value")

    container = widgets.HBox([drop_down_1, drop_down_2])
#     widgets.VBox([container,g])
    return g,container