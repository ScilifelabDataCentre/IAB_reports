# Used to generate all of the numbers research impact section (chapter 9)
import pandas as pd
import numpy as np
import os
from matplotlib_venn import venn2, venn2_unweighted, venn2_circles
import matplotlib.pyplot as plt

# many of the numbers can be obtained from other graphs etc.
# Only those not calculated elsewhere will be created here.

# # Affiliates data

# affiliates_bib = pd.read_excel(
#     "Data/SciLifeLab-Affiliates-20230615.xlsx",
#     sheet_name="publ_info",
#     engine="openpyxl",
# )

# # PPtop10 calculation

# aff_impact = affiliates_bib[
#     (affiliates_bib["Publication_year"] == 2017)
#     | (affiliates_bib["Publication_year"] == 2018)
#     | (affiliates_bib["Publication_year"] == 2019)
#     | (affiliates_bib["Publication_year"] == 2020)
# ]

# aff_impacts_scores = aff_impact[
#     (aff_impact["Doc_type_code_rev"] == "RV")
#     | (aff_impact["Doc_type_code_rev"] == "AR")
#     | (aff_impact["Doc_type_code_rev"] == "PP")
# ]

# aff_impacts_scores["top10_scxwo"] = aff_impacts_scores["top10_scxwo"].astype(float)
# aff_impacts_scores = aff_impacts_scores["top10_scxwo"].mean()

# # print(aff_impacts_scores)


# # Fellows data

# Fell_bib = pd.read_excel(
#     "Data/SciLifeLab-Fellows-20230615.xlsx",
#     sheet_name="publ_info",
#     engine="openpyxl",
# )

# # PPtop10 calculation

# Fell_impact = Fell_bib[
#     (Fell_bib["Publication_year"] == 2017)
#     | (Fell_bib["Publication_year"] == 2018)
#     | (Fell_bib["Publication_year"] == 2019)
#     | (Fell_bib["Publication_year"] == 2020)
# ]

# Fell_impacts_scores = Fell_impact[
#     (Fell_impact["Doc_type_code_rev"] == "RV")
#     | (Fell_impact["Doc_type_code_rev"] == "AR")
#     | (Fell_impact["Doc_type_code_rev"] == "PP")
# ]

# Fell_impacts_scores["top10_scxwo"] = Fell_impacts_scores["top10_scxwo"].astype(float)
# Fell_impacts_scores = Fell_impacts_scores["top10_scxwo"].mean()

# # print(Fell_impacts_scores)

# Now work on Venn diagram figures...
# Need PP(top10) for earlier numbers though..

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

# Need 2017-2020

inf_bib = infra_bib[
    (infra_bib["Publication_year"] > 2016) & (infra_bib["Publication_year"] < 2021)
]

affs_bib = affiliates_bib[
    (affiliates_bib["Publication_year"] > 2016)
    & (affiliates_bib["Publication_year"] < 2021)
]

# Now need to get the sets for just infra, just aff, intersection
# DO a venn for each set as a check

# inf_set_DOI = set(inf_bib["UT"])
# aff_set_DOI = set(affs_bib["UT"])

# # Make a weighted Venn with initial values

# total = len(inf_set_DOI.union(aff_set_DOI))
# v = venn2(
#     subsets=[inf_set_DOI, aff_set_DOI],
#     # next line would set labels outside the circles
#     set_labels=(
#         "Användare av SciLifeLab:s\nforskningsinfrastruktur   ",
#         "SciLifeLab:s forskare",
#     ),
#     set_colors=("#A7C947", "#4C979F"),
#     subset_label_formatter=lambda x: f"{x}\n({(x/total):1.0%})",
#     alpha=1.0,
#     ax=plt.gca(),
# )
# # set outer labels
# for text in v.set_labels:
#     text.set_fontsize(12)
# # below recolours overlapping sections to be consistent with scilifelab visual ID
# v.get_patch_by_id("11").set_color("#a48fa9")
# plt.show()

# Now have to make the sets for this

# make intersection first

interaction = pd.merge(
    inf_bib,
    affs_bib,
    on=[
        "UT",
    ],
    how="inner",
)

# print(interaction.info())

# Now the ones only in affiliates or infra NOT intersection

aff_only = affs_bib[~affs_bib["UT"].isin(interaction["UT"])]
inf_only = inf_bib[~inf_bib["UT"].isin(interaction["UT"])]

# PPtop10 calculation
# (already filtered for years)

int_impacts_scores = interaction[
    (interaction["Doc_type_code_rev_x"] == "RV")
    | (interaction["Doc_type_code_rev_x"] == "AR")
    | (interaction["Doc_type_code_rev_x"] == "PP")
]

aff_impacts_scores = aff_only[
    (aff_only["Doc_type_code_rev"] == "RV")
    | (aff_only["Doc_type_code_rev"] == "AR")
    | (aff_only["Doc_type_code_rev"] == "PP")
]

inf_impacts_scores = inf_only[
    (inf_only["Doc_type_code_rev"] == "RV")
    | (inf_only["Doc_type_code_rev"] == "AR")
    | (inf_only["Doc_type_code_rev"] == "PP")
]

int_impacts_scores["top10_scxwo_y"] = int_impacts_scores["top10_scxwo_y"].astype(float)
aff_impacts_scores["top10_scxwo"] = aff_impacts_scores["top10_scxwo"].astype(float)
inf_impacts_scores["top10_scxwo"] = inf_impacts_scores["top10_scxwo"].astype(float)
int_impacts_scores = int_impacts_scores["top10_scxwo_y"].mean()
aff_impacts_scores = aff_impacts_scores["top10_scxwo"].mean()
inf_impacts_scores = inf_impacts_scores["top10_scxwo"].mean()
