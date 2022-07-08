# Import needed modules, functions and objects
import pandas as pd
from pandas import read_csv, read_excel, ExcelFile 
from matplotlib import pyplot
from sodapy import Socrata
import plotly.express as px

# Web scrap CDC data on US COVID-19 Cases and Deaths by State using sodapy/Socrata

# Unauthenticated client only works with public data sets. Note 'None'
# in place of application token, and no username or password:
client = Socrata("data.cdc.gov", None)

# Return client as JSON from API / converted to Python list of
# dictionaries by sodapy.
results = client.get("9mfq-cb36", limit=56000,offset=100)

# Convert to pandas DataFrame & format needed columns
nationwide = pd.DataFrame.from_records(results)
nationwide = nationwide.sort_values(by='submission_date') # sort instances by data submission date
nationwide[['tot_cases','conf_cases','prob_cases','new_case','pnew_case','tot_death','conf_death',
                     'prob_death','new_death','pnew_death']] = nationwide[['tot_cases','conf_cases','prob_cases',
                    'new_case','pnew_case','tot_death','conf_death','prob_death','new_death','pnew_death']].apply(pd.to_numeric)
nationwide['submission_date'] = pd.to_datetime(nationwide['submission_date'])

# Select date specific for Massachusetts
nationwide_MA = nationwide.loc[nationwide["state"].isin(['MA'])]

# Visualize daily new cases

fig = px.line(nationwide_MA, x="submission_date", y="new_case", 
             labels={
                     "submission_date": "Submission Date",
                     "new_case": "Number of Cases"
                 },
             
             title='Daily New COVID-19 Cases in Massachusetts')

fig.write_html("C:/Users/Juan Varela/Jupyter_Projects/Data Science and Machine Learning/COVID19/MA_covid_cases.html")
