import pandas as pd
import numpy as np


### FAC MAP
# to their labels in the publication database
fac_map_input = pd.read_excel(
    "Data/Reporting Units 2022.xlsx",  ## file from Lars OO
    sheet_name="Reporting units",
    header=0,
    engine="openpyxl",
    keep_default_na=False,
)
fac_map_input["PDB label"] = fac_map_input["PDB label"].str.replace(
    r"\(.*\)", "", regex=True
)
fac_map_input = fac_map_input[["Unit", "PDB label"]]
fac_map_input = fac_map_input.replace("", np.nan)
fac_map_input["PDB label"] = fac_map_input["PDB label"].fillna(fac_map_input["Unit"])
fac_map_input.rename(columns={"PDB label": "Label"}, inplace=True)
# fac_map_input = fac_map_input.replace(
#     "Drug Discovery and Development ", "Drug Discovery and Development"
# )
# fac_map_input = fac_map_input.replace(
#     "Eukaryotic Single Cell Genomics ", "Eukaryotic Single Cell Genomics"
# )
# fac_map_input = fac_map_input.replace(
#     "Swedish Metabolomics Centre ", "Swedish Metabolomics Centre"
# )
# fac_map_input = fac_map_input.replace("In Situ Sequencing ", "In Situ Sequencing")
# fac_map_input = fac_map_input.replace(
#     "Spatial Mass Spectrometry + Advanced FISH Technologies",
#     "Spatial Mass Spectrometry",
# )
# fac_map_input = fac_map_input.replace("Swedish NMR Centre ", "Swedish NMR Centre")
# fac_map_input = fac_map_input.replace(
#     "Chemical Biology Consortium Sweden ", "Chemical Biology Consortium Sweden"
# )

fac_map = dict(zip(fac_map_input.Label, fac_map_input.Unit))
# print(fac_map)
df = pd.read_excel(
    "Data/Infrastructure_pubs_230607.xlsx",
    sheet_name="Publications",
    engine="openpyxl",
)
df = df[(df["Year"] > 2020) & (df["Year"] < 2023)]
# extract unit labels from the excel
df = df.replace(
    "Swedish Metabolomics Centre (SMC)|Swedish NMR Centre (SNC)",
    "Swedish Metabolomics Centre|Swedish NMR Centre",
)
df = df.replace(
    "Affinity Proteomics Uppsala|Bioinformatics Compute and Storage|NGI Short read|NGI Stockholm (Genomics Production)|National Genomics Infrastructure|Swedish Metabolomics Centre (SMC)",
    "Affinity Proteomics Uppsala|Bioinformatics Compute and Storage|NGI Short read|NGI Stockholm|National Genomics Infrastructure|Swedish Metabolomics Centre",
)
df = df.replace(
    "Chemical Biology Consortium Sweden (CBCS)|Swedish Metabolomics Centre (SMC)",
    "Chemical Biology Consortium Sweden|Swedish Metabolomics Centre",
)
df = df.replace(
    "Bioinformatics Compute and Storage|Chemical Biology Consortium Sweden (CBCS)|Drug Discovery and Development (DDD)",
    "Bioinformatics Compute and Storage|Chemical Biology Consortium Sweden|Drug Discovery and Development",
)
df = df.replace(
    "Chemical Biology Consortium Sweden (CBCS)|Drug Discovery and Development (DDD)",
    "Chemical Biology Consortium Sweden|Drug Discovery and Development",
)
df = df.replace(
    "CRISPR Functional Genomics|Chemical Biology Consortium Sweden (CBCS)|Global Proteomics and Proteogenomics|NGI Stockholm (Genomics Applications)|NGI Stockholm (Genomics Production)|National Genomics Infrastructure",
    "CRISPR Functional Genomics|Chemical Biology Consortium Sweden|Global Proteomics and Proteogenomics|National Genomics Infrastructure",
)
df = df.replace(
    "Bioinformatics Compute and Storage|Eukaryotic Single Cell Genomics (ESCG)|Microbial Single Cell Genomics|NGI Stockholm (Genomics Applications)|NGI Stockholm (Genomics Production)|National Genomics Infrastructure",
    "Bioinformatics Compute and Storage|Eukaryotic Single Cell Genomics|Microbial Single Cell Genomics|NGI Stockholm|National Genomics Infrastructure",
)
df = df.replace(
    "Chemical Biology Consortium Sweden (CBCS)|Swedish NMR Centre (SNC)",
    "Chemical Biology Consortium Sweden|Swedish NMR Centre",
)
df = df.replace(
    "Chemical Biology Consortium Sweden (CBCS)|Swedish NMR Centre (SNC)",
    "Chemical Biology Consortium Sweden|Swedish NMR Centre",
)
df = df.replace(
    "NGI Short read|NGI Uppsala (SNP&SEQ Technology Platform)|National Genomics Infrastructure|Swedish NMR Centre (SNC)",
    "NGI Short read|NGI Uppsala|National Genomics Infrastructure|Swedish NMR Centre",
)
df["Labels"] = df["Labels"].str.replace(r"\(.*\)", "", regex=True)
df = df.replace(fac_map, regex=True)
# need to do some manual changes given that labels are combined
# This is because some labels were deleted when the publication label ends in ()
# and the puctuation is replaced with str.replace(r"\(.*\)", "", regex=True)
df.to_excel("test.xlsx")
