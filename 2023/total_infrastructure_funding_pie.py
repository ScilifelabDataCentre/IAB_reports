# Note: potentially need to trim original file from OO
# Has 'spare' rows, columns and totals for checking
import pandas as pd
import plotly.graph_objects as go
import os
import numpy as np
from colour_science_2023 import (
    PLATFORM_FUNDING_COLOURS,
)

Plat_tot_fund_data = pd.read_excel(
    "Data/Total Infrastructure Funding 2022.xlsx",
    sheet_name="Sheet 1",
    header=0,
    engine="openpyxl",
    keep_default_na=False,
)


# OO requested percentages rounded to nearest percent for this graph
Plat_tot_fund_data["Fund_MSEK"] = Plat_tot_fund_data["Funding 2022 (MSEK)"]
# print(Acaduser_data)
colours = np.array([""] * len(Plat_tot_fund_data["Category"]), dtype=object)
for i in Plat_tot_fund_data["Category"]:
    colours[np.where(Plat_tot_fund_data["Category"] == i)] = PLATFORM_FUNDING_COLOURS[
        str(i)
    ]

Plat_tot_fund_data["Category"] = Plat_tot_fund_data["Category"].replace(
    "User Fees",
    "User<br>Fees<br>",
)

Plat_tot_fund_data["Category"] = Plat_tot_fund_data["Category"].replace(
    "SciLifeLab Base",
    "SciLifeLab<br>Base<br>",
)
Plat_tot_fund_data["Category"] = Plat_tot_fund_data["Category"].replace(
    "SciLifeLab Instrument",
    "SciLifeLab Instrument<br>",
)
Plat_tot_fund_data["Category"] = Plat_tot_fund_data["Category"].replace(
    "University",
    "University<br>",
)
Plat_tot_fund_data["Category"] = Plat_tot_fund_data["Category"].replace(
    "VR",
    "VR<br>",
)


fig = go.Figure(
    go.Pie(
        values=Plat_tot_fund_data["Fund_MSEK"],
        labels=Plat_tot_fund_data["Category"],
        hole=0.6,
        marker=dict(colors=colours, line=dict(color="#000000", width=1)),
        direction="clockwise",
        sort=True,
    )
)

fig.update_traces(
    textposition="outside",
    texttemplate="%{label} (%{value:.1f})",
)
fig.update_layout(
    margin=dict(l=0, r=0, b=0, t=0),
    font=dict(size=34),
    annotations=[
        dict(
            showarrow=False,
            text="{}".format(round(sum(Plat_tot_fund_data["Fund_MSEK"]), 1)),
            font=dict(size=50),  # should work for all centre bits
            x=0.5,
            y=0.5,
        )
    ],
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
fig.write_image("Plots/total infrastructure funding.svg", scale=3)
fig.write_image("Plots/total infrastructure funding.png", scale=3)
