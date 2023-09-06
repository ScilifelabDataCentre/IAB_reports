"""This script will produce pie charts showing the proportion of infra papers labelled with service/tech/collab"""

import pandas as pd
import numpy as np
import plotly.graph_objects as go
import os
from colour_science_2023 import (
    SCILIFE_COLOURS,
)

infra_bib = pd.read_excel(
    "Data/SciLifeLab-Infrastructure-20230615.xlsx",
    sheet_name="publ_info",
    engine="openpyxl",
)
affiliates_bib = pd.read_excel(
    "Data/SciLifeLab-Affiliates-20230615.xlsx",
    sheet_name="publ_info",
    engine="openpyxl",
)

# Filter to specific years
# for IAB 2023, need last 2 years of reporting (2021-2022)

inf_bib = infra_bib[
    (infra_bib["Publication_year"] > 2020) & (infra_bib["Publication_year"] < 2023)
]

affs_bib = affiliates_bib[
    (affiliates_bib["Publication_year"] > 2020)
    & (affiliates_bib["Publication_year"] < 2023)
]

# Drop uneeded rows

affs_bib = affs_bib[
    [
        "UT",
        "DOI",
        "Doc_type_code_rev",
        "Publication_year",
        "Authors",
        "Title",
        "Journal",
    ]
]

inf_bib = inf_bib[
    [
        "UT",
        "DOI",
        "Doc_type_code_rev",
        "Publication_year",
        "Authors",
        "Title",
        "Journal",
    ]
]

# # Create a dataset showing the intersection between these dataset (check against the venn diagram too)

interaction = pd.merge(
    inf_bib,
    affs_bib,
    on=[
        "UT",
    ],
    how="inner",
)

interaction.drop_duplicates(subset="UT", keep="first", inplace=True)

# print(interaction.info())

# This shows the matched set (i.e. where affiliates and infrastructure worked together)

# Now, we need to match the infrastructure labels (from the publications database)

infra_labels = pd.read_excel(
    "Data/Infrastructure_pubs_230607.xlsx",
    sheet_name="Publications",
    engine="openpyxl",
)

match_labels = pd.merge(
    interaction,
    infra_labels,
    how="left",
    left_on="DOI_x",
    right_on="DOI",
)

match_labels.drop_duplicates(subset="UT", keep="first", inplace=True)

print(match_labels.info())


def replacer(inp: str):
    if len(data := set(inp.split("|"))) == 1:
        return data.pop()
    else:
        return "Multiple"


match_labels["relabeled"] = match_labels.Qualifiers.apply(replacer)

# Use as a manual check for matches - all should match (everything in the database extract should be in the results from KTH)
# match_labels.to_excel("Data/check_inf_label_match_relabel.xlsx")
# Make some manual changes and re-read
# noticed that 'multiple' is often over-estimated, because you get the | when no label is allocated

match_labels = pd.read_excel(
    "Data/check_inf_label_match_relabel.xlsx",
    sheet_name="Sheet1",
    engine="openpyxl",
)

# Now count up the different categories

match_labels = match_labels.replace("", np.nan)
match_labels["relabeled"] = match_labels["relabeled"].fillna("No category")

match_labels = (
    match_labels.groupby(["relabeled"])
    .agg(No_papers=("relabeled", "size"))
    .reset_index()
)

# print(match_labels)

match_labels["Percentage"] = (
    (match_labels["No_papers"] / sum(match_labels["No_papers"])) * 100
).round(1)

colours = [
    SCILIFE_COLOURS[0],
    SCILIFE_COLOURS[4],
    SCILIFE_COLOURS[12],
    SCILIFE_COLOURS[8],
    SCILIFE_COLOURS[16],
]

# Edited this to fit more nicely
match_labels["relabeled"] = match_labels["relabeled"].replace(
    "Technology development",
    "Technology<br>development",
)
# print(match_labels)

fig = go.Figure(
    go.Pie(
        values=match_labels["Percentage"],
        labels=match_labels["relabeled"],
        hole=0.6,
        marker=dict(colors=colours, line=dict(color="#000000", width=1)),
        direction="clockwise",
        sort=True,
    )
)

fig.update_traces(
    textposition="outside",
    texttemplate="%{label} <br>(%{value}%)",
)
fig.update_layout(
    margin=dict(l=0, r=0, b=0, t=0),
    font=dict(size=23),
    showlegend=False,
    width=1000,
    height=1000,
    autosize=False,
)
if not os.path.isdir("Plots"):
    os.mkdir("Plots")
# fig.show()

fig.write_image("Plots/infra_affs_services_labels.svg", scale=3)
fig.write_image("Plots/infra_affs_services_labels.png", scale=3)
