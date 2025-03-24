<a className="gh-badge" href="https://datahub.io/core/cofog"><img src="https://badgen.net/badge/icon/View%20on%20datahub.io/orange?icon=https://datahub.io/datahub-cube-badge-icon.svg&label&scale=1.25" alt="badge" /></a>

Classification of the Functions of Government (COFOG) is a classification defined by the United Nations Statistics Division. Its purpose is to "classify the purpose of transactions such as outlays on final consumption expenditure, intermediate consumption, gross capital formation and capital and current transfers, by general government" (from home page).

These functions are designed to be general enough to apply to the government of different countries. The accounts of each country in the United Nations are presented under these categories. The value of this is that the accounts of different countries can be compared.

## Preparation

To prepare and process the COFOG data, follow these steps:

```bash
# Clone the repository
git clone https://github.com/datasets/cofog.git
cd cofog

# Run make to process everything
make all
```

This will:
1. Install required dependencies
2. Download and process explanatory notes
3. Extract descriptions in multiple languages
4. Merge all data into a single CSV file

The final merged dataset will be available at `data/cofog.csv`.

## Data

Data was sourced from the [UN site][un-cofog] ([raw access database from the UN][accessdb]) and extracted using the scripts found in the scripts directory of the source data package. In addition to the UN site, versions of COFOG can also be [found on Eurostat](http://ec.europa.eu/eurostat/ramon/nomenclatures/index.cfm?TargetUrl=LST_CLS_DLD&StrNom=CL_COFOG99&StrLanguageCode=EN&StrLayoutCode=HIERARCHIC) with one advantage of the Eurostat data being the availability of additional languages (e.g. German).

[un-cofog]: http://unstats.un.org/unsd/cr/registry/regcst.asp?Cl=4&Lg=1
[accessdb]: http://unstats.un.org/unsd/cr/registry/regdntransfer.asp?f=186

## License

No license specified but factual data and extraction and normalization of the csv file has been done by the Maintainer who places the material in the Public Domain under the PDDL.

