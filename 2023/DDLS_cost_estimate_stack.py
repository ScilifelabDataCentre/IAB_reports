""" The script contains the information to produce a stacked plot for DDLS estimated costs"""
import pandas as pd
import os
import plotly.graph_objects as go

# import plotly.express as px
# import numpy as np
from colour_science_2023 import (
    SCILIFE_COLOURS,
)

Raw_data = pd.read_excel(
    "Data/Cost_estimate.xlsx",
    sheet_name="Sheet 1",
    header=0,
    engine="openpyxl",
    keep_default_na=False,
)

# print(Raw_data)

DDLS_melt = pd.melt(
    Raw_data,
    id_vars="Type",
    value_vars=list(Raw_data.columns[1:]),
    var_name="Year",
    value_name="Cost",
)

DDLS_melt.rename(
    columns={"Type": "Type_costs"},
    inplace=True,
)
DDLS_melt = DDLS_melt.replace("2021 actual", "2021")
DDLS_melt = DDLS_melt.replace("2022 actual", "2022")

##print(DDLS_melt)

# Below can be used
DDLS_melt["Cost"] = DDLS_melt["Cost"] * 1000

##print(DDLS_melt)


def DDLS_graph_func(input):
    costestimate = input
    # split down dataframes to enable stacking
    DDLS_fell = costestimate[(costestimate["Type_costs"] == "DDLS fellow-packages")]
    phd_proj = costestimate[(costestimate["Type_costs"] == "PhD projects")]
    ind_phd = costestimate[(costestimate["Type_costs"] == "Industrial PhD projects")]
    postdoc_proj = costestimate[(costestimate["Type_costs"] == "Postdoc projects")]
    ind_postdoc = costestimate[
        (costestimate["Type_costs"] == "Industrial postdoc projects")
    ]
    WABI = costestimate[(costestimate["Type_costs"] == "WABI")]
    WASP = costestimate[(costestimate["Type_costs"] == "WASP")]
    WASP_HS = costestimate[(costestimate["Type_costs"] == "WASP-HS")]
    data_supp = costestimate[
        (costestimate["Type_costs"] == "Data support and databases")
    ]
    other = costestimate[(costestimate["Type_costs"] == "Other activities")]
    # Make stacked bar chart
    fig = go.Figure(
        data=[
            go.Bar(
                name="DDLS fellows",
                x=DDLS_fell.Year,
                y=DDLS_fell.Cost,
                marker=dict(
                    color=SCILIFE_COLOURS[0], line=dict(color="#000000", width=2)
                ),
            ),
            go.Bar(
                name="PhD",
                x=phd_proj.Year,
                y=phd_proj.Cost,
                marker=dict(
                    color=SCILIFE_COLOURS[12], line=dict(color="#000000", width=2)
                ),
            ),
            go.Bar(
                name="Industrial PhD",
                x=ind_phd.Year,
                y=ind_phd.Cost,
                marker=dict(
                    color=SCILIFE_COLOURS[4], line=dict(color="#000000", width=2)
                ),
            ),
            go.Bar(
                name="Postdoctorate",
                x=postdoc_proj.Year,
                y=postdoc_proj.Cost,
                marker=dict(
                    color=SCILIFE_COLOURS[14], line=dict(color="#000000", width=2)
                ),
            ),
            go.Bar(
                name="Industrial postdoctorate",
                x=ind_postdoc.Year,
                y=ind_postdoc.Cost,
                marker=dict(color="#000000", line=dict(color="#000000", width=2)),
            ),
            go.Bar(
                name="WABI",
                x=WABI.Year,
                y=WABI.Cost,
                marker=dict(
                    color=SCILIFE_COLOURS[8], line=dict(color="#000000", width=2)
                ),
            ),
            go.Bar(
                name="WASP",
                x=WASP.Year,
                y=WASP.Cost,
                marker=dict(color="#696969", line=dict(color="#000000", width=2)),
            ),
            go.Bar(
                name="WASP-HS",
                x=WASP_HS.Year,
                y=WASP_HS.Cost,
                marker=dict(
                    color=SCILIFE_COLOURS[10], line=dict(color="#000000", width=2)
                ),
            ),
            go.Bar(
                name="Data support and databases",
                x=data_supp.Year,
                y=data_supp.Cost,
                marker=dict(
                    color=SCILIFE_COLOURS[2], line=dict(color="#000000", width=2)
                ),
            ),
            go.Bar(
                name="Other activities",
                x=other.Year,
                y=other.Cost,
                marker=dict(color="#FFFFFF", line=dict(color="#000000", width=2)),
            ),
        ]
    )

    fig.update_layout(
        barmode="stack",
        plot_bgcolor="white",
        autosize=False,
        font=dict(size=26),
        margin=dict(r=270, t=0, b=0, l=0),
        width=2000,
        height=1000,
        showlegend=True,
        legend={"traceorder": "normal"},
    )
    # edit legend
    # fig.update_layout(legend_tracegroupgap=30)
    # List years to use in x-axis
    Years = costestimate["Year"].unique().astype(str)
    Years_int = costestimate["Year"].unique()
    # modify x-axis
    fig.update_xaxes(
        title=" ",
        showgrid=True,
        linecolor="black",
        # add more years as needed
        ticktext=[
            "<b> 2021*</b>",
            "<b> 2022*</b>",
            "<b>" + Years[2] + "</b>",
            "<b>" + Years[3] + "</b>",
            "<b>" + Years[4] + "</b>",
            "<b>" + Years[5] + "</b>",
            "<b>" + Years[6] + "</b>",
            "<b>" + Years[7] + "</b>",
            "<b>" + Years[8] + "</b>",
            "<b>" + Years[9] + "</b>",
            "<b>" + Years[10] + "</b>",
            "<b>" + Years[11] + "</b>",
            "<b>" + Years[12] + "</b>",
        ],
        tickvals=[
            Years[0],
            Years[1],
            Years[2],
            Years[3],
            Years[4],
            Years[5],
            Years[6],
            Years[7],
            Years[8],
            Years[9],
            Years[10],
            Years[11],
            Years[12],
        ],
    )

    Year_one = costestimate[(costestimate["Year"] == Years_int[0])]
    Year_two = costestimate[(costestimate["Year"] == Years_int[1])]
    Year_three = costestimate[(costestimate["Year"] == Years_int[2])]
    Year_four = costestimate[(costestimate["Year"] == Years_int[3])]
    Year_five = costestimate[(costestimate["Year"] == Years_int[4])]
    Year_six = costestimate[(costestimate["Year"] == Years_int[5])]
    Year_seven = costestimate[(costestimate["Year"] == Years_int[6])]
    Year_eight = costestimate[(costestimate["Year"] == Years_int[7])]
    Year_nine = costestimate[(costestimate["Year"] == Years_int[8])]
    Year_ten = costestimate[(costestimate["Year"] == Years_int[9])]
    Year_eleven = costestimate[(costestimate["Year"] == Years_int[10])]
    Year_twelve = costestimate[(costestimate["Year"] == Years_int[11])]
    Year_thirteen = costestimate[(costestimate["Year"] == Years_int[12])]

    highest_y_value = max(
        Year_one["Cost"].sum(),
        Year_two["Cost"].sum(),
        Year_three["Cost"].sum(),
        Year_four["Cost"].sum(),
        Year_five["Cost"].sum(),
        Year_six["Cost"].sum(),
        Year_seven["Cost"].sum(),
        Year_eight["Cost"].sum(),
        Year_nine["Cost"].sum(),
        Year_ten["Cost"].sum(),
        Year_eleven["Cost"].sum(),
        Year_twelve["Cost"].sum(),
        Year_thirteen["Cost"].sum(),
    )

    if highest_y_value < 500000000:
        yaxis_tick = 100000000
    if highest_y_value > 500000000:
        yaxis_tick = 150000000

    # modify y-axis
    fig.update_yaxes(
        title="Estimated Cost per Operative Area (SEK)<br>",
        showgrid=True,
        gridcolor="lightgrey",
        linecolor="black",
        dtick=yaxis_tick,
        # ticksuffix=" SEK",
        range=[0, 500000000],
    )
    # fig.update_layout(legend={"itemsizing": "constant"})
    if not os.path.isdir("Plots/"):
        os.mkdir("Plots/")
    fig.show()

    fig.write_image("Plots/DDLS_cost_estimate.png")
    fig.write_image("Plots/DDLS_cost_estimate.svg")


DDLS_graph_func(DDLS_melt)
