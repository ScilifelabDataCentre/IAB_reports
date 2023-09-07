""" Plotting Altmetrics percentile scores"""
import pandas as pd
import numpy as np
import os
import plotly.express as px
from Altmetrics_data_prep import (
    Aff_data_group_melt,
    Fac_data_group_melt,
    Fell_data_group_melt,
)


def groupedbar(data, name):
    fig = px.bar(
        data,
        x="Year",
        y="Percent",
        color="Context_type",
        color_discrete_sequence=["#A7C947", "#491F53"],  # "#045C64", "#A6A6A6",
    )
    # set the order of categories
    # update figure layout to showed a grouped barchart, white background, sert font size and set overall size
    fig.update_layout(
        barmode="group",
        plot_bgcolor="white",
        font=dict(size=18),
        margin=dict(r=200, l=10),
        autosize=False,
        width=1200,
        height=600,
        legend_title_text="",
    )
    # modify x-axis
    fig.update_xaxes(
        title="",
        showgrid=True,
        linecolor="black",
        # Modify text and values as needed
        ticktext=[
            "<b>2013</b>",
            "<b>2014</b>",
            "<b>2015</b>",
            "<b>2016</b>",
            "<b>2017</b>",
            "<b>2018</b>",
            "<b>2019</b>",
            "<b>2020</b>",
            "<b>2021</b>",
            "<b>2022</b>",
        ],
        tickvals=[
            "2013",
            "2014",
            "2015",
            "2016",
            "2017",
            "2018",
            "2019",
            "2020",
            "2021",
            "2022",
        ],
    )
    # modify y-axis
    fig.update_yaxes(
        title=" ",
        showgrid=True,
        gridcolor="black",
        linecolor="black",
        ticktext=["0", "10", "20", "30", "40"],
        tickvals=["0", "10", "20", "30", "40"],
        range=[0, 45],
    )
    fig.update_traces(marker_line_width=1, marker_line_color="black")
    # #put in the line on the graph for average
    # fig.add_annotation(
    #     x=1.2,
    #     y=10,
    #     showarrow=False,
    #     text="Expected Score",
    #     textangle=0,
    #     xref="paper",
    #     yref="y",
    # )
    # fig.add_shape(
    #     type="line",
    #     x0=0,
    #     x1="1",
    #     xref="paper",
    #     y0=10,
    #     y1=10,
    #     line=dict(color="#4C979F", width=4),
    # )
    # fig.show()
    if not os.path.isdir("Plots/"):
        os.mkdir("Plots/")
    fig.write_image(
        "Plots/{}_Altmetricsscores_percent_in_context_line.png".format(name)
    )


groupedbar(Aff_data_group_melt, "affiliates")
groupedbar(Fac_data_group_melt, "infrastructure")
# groupedbar(Fell_data_group_melt, "fellows")
