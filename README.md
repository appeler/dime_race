## Race and Sex for DIME

Impute race and gender of people in [Database on Ideology, Money in Politics, and Elections](https://data.stanford.edu/dime). 

### Steps:

1. Subset: We first subset the database to keep: a. uniqueid (We use one that gives a unique id for each contribution.) b. columns related to name, and c. year in which the contribution was made.

2. De-duplicate: We build a primary key, where key = concatenation of name + year of contribution. We then de-duplicate based on the key. The final dataset has all the columns from step 1 (the primary key column goes away), just fewer rows. (We are eliminating multiple contributions per year from the 'same' person. Our ability to detect the 'same' person is limited by spelling errors, etc. etc.)

4. Predict: We use [https://github.com/appeler/ethnicolr](https://github.com/appeler/ethnicolr) to impute race. The package exposes multiple functions. We use the following functions with following arguments:

```
a. census_ln (takes last name) for 2010 and 2000 
b. pred_fl_reg_ln and pred_fl_reg_name
```

We then export out the file. 

### Script

* [raw_impute_DIME_database.py](raw_impute_DIME_database.py) or [raw_impute_DIME_database.ipynb](https://nbviewer.jupyter.org/github/appeler/dime_race/blob/master/raw_impute_DIME_database.ipynb)

### Data

Data will be posted at: https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/M5K7VR
