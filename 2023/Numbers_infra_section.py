# Used to generate all of the numbers in the infrastructure section

import pandas as pd
import numpy as np
import os

# infra data (original extract)

infra_bib = pd.read_excel(
    "Data/Infrastructure_pubs_230607.xlsx",
    sheet_name="Publications",
    engine="openpyxl",
)

# get numbers of papers for each year:

Per_year = infra_bib.groupby(["Year"]).size().reset_index().rename(columns={0: "Count"})
# print(Per_year)

# How many are in each category for last 5 years.
# need to deal with this in 2 time periods: one in 2017-2020, one in 2021-2022

Prev_three_years = infra_bib[(infra_bib["Year"] > 2016) & (infra_bib["Year"] < 2021)]

Last_two_years = infra_bib[(infra_bib["Year"] > 2020) & (infra_bib["Year"] < 2023)]

Last_two_years["Qualifiers"] = Last_two_years["Qualifiers"].fillna("|")
Prev_three_years["Qualifiers"] = Prev_three_years["Qualifiers"].fillna("|")

# now look at labels (look at service, collab, tech dev, and multiple )


def replacer(inp: str):
    if len(data := set(inp.split("|"))) == 1:
        return data.pop()
    else:
        return "Multiple"


Last_two_years["relabeled"] = Last_two_years.Qualifiers.apply(replacer)
Prev_three_years["relabeled"] = Prev_three_years.Qualifiers.apply(replacer)

# print(Last_two_years.info())
# print(Prev_three_years.info())

# Know that some of these will not be 'quite right' given how the labels happen.
# (some will be labelled multiple just because they are left blank by some units)

# Last_two_years.to_excel("Data/Last_two_years_check.xlsx")
# Prev_three_years.to_excel("Data/Prev_three_years_check.xlsx")

# Can now use manually relabelled information

two_years = pd.read_excel(
    "Data/Last_two_years_check_expanded.xlsx",
    sheet_name="Sheet1",
    engine="openpyxl",
)

prev_three = pd.read_excel(
    "Data/Prev_three_years_check_expanded.xlsx",
    sheet_name="Sheet1",
    engine="openpyxl",
)

two_year_qual = (
    two_years.groupby(["relabeled"]).size().reset_index().rename(columns={0: "Count"})
)
three_year_qual = (
    prev_three.groupby(["relabeled"]).size().reset_index().rename(columns={0: "Count"})
)

# print(two_year_qual)
# print(three_year_qual)

# Now, get overall impact metrics for the infrastructure

# need KTH data here
infra_bib = pd.read_excel(
    "Data/SciLifeLab-Infrastructure-20230615.xlsx",
    sheet_name="publ_info",
    engine="openpyxl",
)

inf_scores = infra_bib[
    (infra_bib["Publication_year"] == 2017)
    | (infra_bib["Publication_year"] == 2018)
    | (infra_bib["Publication_year"] == 2019)
    | (infra_bib["Publication_year"] == 2020)
]

inf_filtered = inf_scores[
    (inf_scores["Doc_type_code_rev"] == "RV")
    | (inf_scores["Doc_type_code_rev"] == "AR")
    | (inf_scores["Doc_type_code_rev"] == "PP")
]

inf_filtered["top10_scxwo"] = inf_filtered["top10_scxwo"].astype(float)
avinf = inf_filtered["top10_scxwo"].mean()
# print(avinf)

# Now need to match the PP(top scores to the prev_three file because need the PP(top10 for all the categories))

match_labels = pd.merge(
    prev_three,
    infra_bib,
    how="left",
    left_on="DOI",
    right_on="DOI",
)

# match_labels.to_excel("Data/test_match_categories.xlsx")

manual_match = pd.read_excel(
    "Data/test_match_categories_manual.xlsx",
    sheet_name="Sheet1",
    engine="openpyxl",
)

# checking that there have not been erraneous duplicates
# manual_match = (
#     manual_match.groupby(["relabeled"])
#     .size()
#     .reset_index()
#     .rename(columns={0: "Count"})
# )

inf_impact = manual_match[
    (manual_match["Year"] == 2017)
    | (manual_match["Year"] == 2018)
    | (manual_match["Year"] == 2019)
    | (manual_match["Year"] == 2020)
]

inf_impacts_scores = inf_impact[
    (inf_impact["Doc_type_code_rev"] == "RV")
    | (inf_impact["Doc_type_code_rev"] == "AR")
    | (inf_impact["Doc_type_code_rev"] == "PP")
]

inf_impacts_scores["top10_scxwo"] = inf_impacts_scores["top10_scxwo"].astype(float)

Collab_impact = inf_impacts_scores[(inf_impacts_scores["relabeled"] == "Collaborative")]

Service_impact = inf_impacts_scores[(inf_impacts_scores["relabeled"] == "Service")]

TD_impact = inf_impacts_scores[
    (inf_impacts_scores["relabeled"] == "Technology development")
]

Collab_impact = Collab_impact["top10_scxwo"].mean()
Service_impact = Service_impact["top10_scxwo"].mean()
TD_impact = TD_impact["top10_scxwo"].mean()
print(Collab_impact)
print(Service_impact)
print(TD_impact)
