import plotly.graph_objects as go
from plotly.subplots import make_subplots
from tkinter import *

def plot(simulations, list):

    fig = make_subplots(rows=2, cols=1, subplot_titles=("Acceleration", "Velocity"))
    
    sim_names = list.get(0, END)
    sim_number = 0
    while sim_number < len(simulations):

        fig.add_trace(
            go.Scatter(x=simulations[sim_number].time, y=simulations[sim_number].acceleration, name=sim_names[sim_number]), 
            row=1, 
            col=1
        )
        fig.add_trace(
            go.Scatter(
                x=simulations[sim_number].time,
                y=simulations[sim_number].velocity, 
                name=sim_names[sim_number]
            ), 
            row=2, 
            col=1
        )
        sim_number += 1
        


    fig.update_xaxes(title_text="Time")
    fig.update_yaxes(title_text="Velocity")
    fig.update_yaxes(row=1, title_text="Acceleration")

    fig.show()