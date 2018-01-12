
# coding: utf-8

# In[1]:


from ethnicolr import census_ln, pred_fl_reg_ln, pred_fl_reg_name
import pandas as pd
import numpy as np


# In[2]:


def fetch_csv_file(selected_csv):
    """Specify the csv file being used."""
    dime_database_file = selected_csv 
    df=pd.read_csv(dime_database_file, low_memory=False)
    return df


# In[3]:


def make_contributor_subset(df):
    """Subset the database to keep: 
    a. uniqueid (there are multiple IDs. Use one that gives a unique id for each contribution.) 
    b. columns related to name, and 
    c. year in which the contribution was made."""

    selected_cols = ['cycle', 'transaction.id',
     'date', 'contributor.name',
     'contributor.lname', 'contributor.fname',
     'contributor.mname', 'contributor.suffix',
     'contributor.title', 'contributor.ffname'
    ]
    subset_df = df[selected_cols].copy()
    new_col_names = [w.replace('.', '_') for w in selected_cols]
    new_cols_dict = dict(zip(selected_cols, new_col_names))
    subset_df.rename(columns=new_cols_dict, inplace=True)
    subset_df.rename({'date':'contribution_year'}, inplace=True)
    return subset_df


# In[4]:


def deduplicate_contributors(subset_df):
    """Build a primary key, where key = concatenation of name + year of contribution. 
       De-duplicate based on the key. """
    subset_df['annual_contrib_key'] = subset_df['contributor_name'] + str(subset_df['contributor_name'])
    subset_df.drop_duplicates(subset=['annual_contrib_key'], keep=False, inplace=True)
    subset_df.drop(columns=['annual_contrib_key'], inplace=True)
    return subset_df


# In[5]:


def run_census_ln (subset_df, census_year):
    """Run the Census Ln Function."""
    has_last_name_df = subset_df[subset_df.contributor_lname.notnull()].copy()
    return census_ln(has_last_name_df, 'contributor_lname', census_year)


# In[6]:


def run_pred_fl_reg_ln(subset_df):
    """Run the pred_fl_reg_ln Function."""
    has_last_name_df = subset_df[subset_df.contributor_lname.notnull()].copy()
    return pred_fl_reg_ln(has_last_name_df , 'contributor_lname')    
    


# In[7]:


def run_pred_fl_reg_name(subset_df):
    """Run Florida Data by Name"""
    has_last_name_df = subset_df[subset_df.contributor_lname.notnull()].copy()
    also_has_first_name_df = has_last_name_df[has_last_name_df.contributor_fname.notnull()].copy()
    return pred_fl_reg_name(also_has_first_name_df, 'contributor_lname', 'contributor_fname')


# In[ ]:


def export_generated_df_csv(df, file_name):
    """Generate new csv file of the prepared dataset."""
    df.to_csv(file_name, encoding='utf-8', index=False, header=True)


# In[19]:


def main_process(selected_csv):
    """Consolidate the steps in the data collation and sanitization."""
    results = {}
    data_df = fetch_csv_file(selected_csv)
    contributors_df = make_contributor_subset(data_df)
    unique_contributors = deduplicate_contributors(contributors_df)
    census_ln_2000_results = run_census_ln(unique_contributors, 2000)
    census_ln_2010_results = run_census_ln(unique_contributors, 2010)
    pred_fl_reg_ln_results = run_pred_fl_reg_ln(unique_contributors)
    pred_fl_reg_name_results = run_pred_fl_reg_name(unique_contributors)
    results['census_ln_2000_results'] = census_ln_2000_results
    results['census_ln_2010_results'] = census_ln_2010_results
    results['pred_fl_reg_ln_results'] = pred_fl_reg_ln_results
    results['pred_fl_reg_name_results'] = pred_fl_reg_name_results
    return results


# In[20]:


"""Execute a single run of data fro dataset."""
selected_csv = 'contribDB_1980.csv' # Example DB from DIME Dataset, csv file in same folder
results = main_process(selected_csv)
for key in results.keys():
    export_generated_df_csv(results[key] , key+'.csv')
    print('{0} successfully exported'.format(key))


# In[22]:


results['census_ln_2000_results'] 


# In[23]:


results['census_ln_2010_results'] 


# In[24]:


results['pred_fl_reg_ln_results']


# In[25]:


results['pred_fl_reg_name_results']

