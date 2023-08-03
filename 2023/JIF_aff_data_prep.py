# Data prep for affiliates JIF plot

import pandas as pd
import numpy as np

# Import data

Pubs_JIF_raw = pd.read_excel(
    "Data/SciLifeLab-Affiliates-20230615.xlsx",
    sheet_name="publ_info",
    header=0,
    engine="openpyxl",
    keep_default_na=False,
)

JIF_scores_raw = pd.read_excel(
    "Data/JCR_JournalResults_12_2022_byISSN_221208_affadded_1.xlsx",
    sheet_name="JCR",
    header=0,
    engine="openpyxl",
    keep_default_na=False,
)

# Need to filter raw pubs (2013-22 for IAB 2023)

Pubs_JIF_raw = Pubs_JIF_raw[
    (Pubs_JIF_raw["Publication_year"] > 2012)
    & (Pubs_JIF_raw["Publication_year"] < 2023)
]

# Need to join the two above files and align JIF with ISSN/ISSN-L
# simpler to work with only columns of interest

Pubs_JIF_sub = Pubs_JIF_raw[
    [
        "UT",
        "Title",
        "Publication_year",
        "Journal",
    ]
]

JIF_scores_sub = JIF_scores_raw[
    [
        "Journal name",
        "JCR Abbreviation",
        "JIF Without Self Cites",
    ]
]

# Must maximise matching of JIF. I recommend checking over
# May be necessary to do some manual work

Pubs_JIF_sublow = Pubs_JIF_sub.apply(lambda x: x.astype(str).str.lower())
JIF_scores_sublow = JIF_scores_sub.apply(lambda x: x.astype(str).str.lower())
# Pubs_JIF_sublow["Journal"] = Pubs_JIF_sublow["Journal"].str.replace(".", "", regex=True)
# JIF_scores_sublow["JCR Abbreviation"] = JIF_scores_sublow[
#     "JCR Abbreviation"
# ].str.replace("-basel", "", regex=True)

JIF_merge_abbnames = pd.merge(
    Pubs_JIF_sublow,
    JIF_scores_sublow,
    how="left",
    left_on="Journal",
    right_on="JCR Abbreviation",
)

JIF_merge_abbnames.drop_duplicates(subset="UT", keep="first", inplace=True)

# JIF_merge_abbnames.to_excel("firstcheck_aff.xlsx")

JIF_merge_abbnames = JIF_merge_abbnames.drop(
    [
        "Journal name",
        "JCR Abbreviation",
    ],
    axis=1,
)

JIF_merge_fullnames = pd.merge(
    JIF_merge_abbnames,
    JIF_scores_sublow,
    how="left",
    left_on="Journal",
    right_on="Journal name",
)

JIF_merge_fullnames.drop_duplicates(subset="UT", keep="first", inplace=True)

JIF_merge_fullnames.rename(
    columns={
        "JIF Without Self Cites_y": "JIF",
        "Publication_year": "Year",
    },
    inplace=True,
)

JIF_merge_fullnames = JIF_merge_fullnames.replace("n/a", np.nan)

JIF_merge_fullnames["JIF"] = JIF_merge_fullnames["JIF"].fillna(-1)

JIF_merge_fullnames["JIF"] = pd.to_numeric(JIF_merge_fullnames["JIF"])

JIF_merge_fullnames.to_excel("firstcheck_aff_Aug.xlsx")

JIF_merge_fullnames["JIF"] = JIF_merge_fullnames["JIF"].fillna(-1)
JIF_merge_fullnames["JIF"] = pd.to_numeric(JIF_merge_fullnames["JIF"])
JIF_merge_fullnames["JIFcat"] = pd.cut(
    JIF_merge_fullnames["JIF"],
    bins=[-1, 0, 6, 9, 25, 1000],
    include_lowest=True,
    labels=["JIF unknown", "JIF <6", "JIF 6-9", "JIF 9-25", "JIF >25"],
)

JIF_aff_data = JIF_merge_fullnames.groupby(["Year", "JIFcat"]).size().reset_index()
JIF_aff_data.columns = ["Year", "JIFcat", "Count"]

JIF_aff_data.to_excel("categorise_affiliates_JIF_Aug23.xlsx")
