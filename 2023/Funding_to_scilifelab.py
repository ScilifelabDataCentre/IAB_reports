# Note: potentially need to trim original file from OO
# Has 'spare' rows, columns and totals for checking
import pandas as pd
import plotly.graph_objects as go
import os
import numpy as np
from colour_science_2023 import (
    SCILIFE_COLOURS,
)

SciLifeLab_compare_years = pd.read_excel(
    "Data/230906 Funding pie charts 2020_2024.xlsx",
    sheet_name="data mod python",
    header=0,
    engine="openpyxl",
    keep_default_na=False,
)

# OO requested percentages rounded to nearest percent for this graph
SciLifeLab_compare_years["2020_perc"] = (
    SciLifeLab_compare_years["2020_perc"].round(0).astype(int)
)
SciLifeLab_compare_years["2024_perc"] = (
    SciLifeLab_compare_years["2024_perc"].round(0).astype(int)
)

# Want two separate pie charts (one for 2020, one for 2024)

SciLifeLab_2020 = SciLifeLab_compare_years[["Category", "2020_amount", "2020_perc"]]
SciLifeLab_2024 = SciLifeLab_compare_years[["Category", "2024_amount", "2024_perc"]]

# Drop 0 values from 2020
SciLifeLab_2020 = SciLifeLab_2020.drop(
    SciLifeLab_2020[SciLifeLab_2020["2020_perc"] == 0].index
)

colours = [
    SCILIFE_COLOURS[0],
    SCILIFE_COLOURS[4],
    SCILIFE_COLOURS[8],
]


def funding_pie(input, column_name, name):
    fig = go.Figure(
        go.Pie(
            values=input[column_name],
            labels=input["Category"],
            hole=0.6,
            marker=dict(colors=colours, line=dict(color="#000000", width=1)),
            direction="clockwise",
            sort=True,
        )
    )

    fig.update_traces(
        textposition="outside",
        texttemplate="%{label} (%{value}%)",
    )
    fig.update_layout(
        margin=dict(l=0, r=0, b=0, t=0),
        font=dict(size=34),
        # annotations=[
        #     dict(
        #         showarrow=False,
        #         text="{}".format(round(sum(Plat_tot_fund_data["Fund_MSEK"]), 1)),
        #         font=dict(size=50),  # should work for all centre bits
        #         x=0.5,
        #         y=0.5,
        #     )
        # ],
        # paper_bgcolor="rgba(0,0,0,0)",
        # plot_bgcolor="rgba(0,0,0,0)",
        showlegend=False,
        width=1000,
        height=1000,
        autosize=False,
    )
    if not os.path.isdir("Plots/"):
        os.mkdir("Plots/")
    # fig.show()
    fig.write_image("Plots/{}_SciLifeLab_funding_pie.svg".format(name), scale=3)
    fig.write_image("Plots/{}_SciLifeLab_funding_pie.png".format(name), scale=3)


funding_pie(SciLifeLab_2020, "2020_perc", 2020)
funding_pie(SciLifeLab_2024, "2024_perc", 2024)
