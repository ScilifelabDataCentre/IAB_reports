# script is designed to look at interactions between units in more detail than in the circos plots.
# looking at the last two years (same as circos plot) and looking at frequency of the different mumbers of units collaborating (according to certain rules e.g. don't count SCoRe)

import pandas as pd
import os
import plotly.graph_objects as go

# Look at collaborations between the units as a histogram (2021 - 2022)

# take data generated in the 'test.xlsx' file generated as part of the circos plot script - this has the names corrected and only data from the correct years
# Manually modified the file in order to show how many units collaborate (in accordance with the reporting units for 2022)
# could code in future, but it's difficult in current structure

collab_data = pd.read_excel(
    "Data/infra_collabs_freq.xlsx",
    sheet_name="Sheet1",
    header=0,
    engine="openpyxl",
    keep_default_na=False,
)

# print(collab_data.info())

collab_data["Number units"] = collab_data["Number units"].astype(str)

collab_data = collab_data[collab_data["Number units"].str.contains("1") == False]

# split the two years into different sets

year_2021 = collab_data[(collab_data["Year"] == 2021)]
year_2022 = collab_data[(collab_data["Year"] == 2022)]

year_2021 = (
    year_2021.groupby(["Number units"])
    .size()
    .reset_index()
    .rename(columns={"Number units": "Number_units", 0: "Count_2021"})
)

year_2022 = (
    year_2022.groupby(["Number units"])
    .size()
    .reset_index()
    .rename(columns={"Number units": "Number_units", 0: "Count_2022"})
)


fig = go.Figure(
    data=[
        go.Bar(
            name="2021",
            x=year_2021.Number_units,
            y=year_2021.Count_2021,
            marker=dict(color="#A7C947", line=dict(color="#000000", width=1)),
        ),
        go.Bar(
            name="2022",
            x=year_2022.Number_units,
            y=year_2022.Count_2022,
            marker=dict(color="#491F53", line=dict(color="#000000", width=1)),
        ),
    ]
)


fig.update_layout(
    barmode="group",
    plot_bgcolor="white",
    font=dict(size=39),
    margin=dict(r=150, l=10),
    autosize=False,
    width=1800,
    height=1200,
    # legend_title_text=" ",
    showlegend=False,
)

# modify x-axis
fig.update_xaxes(
    title=" ",
    tickvals=[
        "2",
        "3",
        "4",
    ],
    ticktext=[
        "Two units",
        "Three units",
        "Four units",
    ],
    showgrid=True,
    linecolor="black",
)
# modify y-axis
fig.update_yaxes(
    title=" ",
    showgrid=True,
    gridcolor="lightgrey",
    linecolor="black",
    ticktext=["0", "10", "20", "30", "40", "50", "60", "70"],
    tickvals=["0", "10", "20", "30", "40", "50", "60", "70"],
    range=[0, 71],
)

# Use the below to look at the figure (initial draft)
# fig.show()

# use the below to save a finalised figure
if not os.path.isdir("Plots/"):
    os.mkdir("Plots/")

fig.write_image("Plots/Numbers_of_collaborating_units_2122.svg")
fig.write_image("Plots/Numbers_of_collaborating_units_2122.png")
