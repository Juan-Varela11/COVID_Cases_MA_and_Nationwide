# Import needed modules, functions and objects
import pandas as pd
from pandas import read_csv, read_excel, ExcelFile
#from pandas.DataFrame import to_csv
from matplotlib import pyplot
from sodapy import Socrata
import plotly.express as px

# Web scrap CDC data on US data on COVID trends using sodapy/Socrata

# Unauthenticated client only works with public data sets. Note 'None'
# in place of application token, and no username or password:
client = Socrata("data.cdc.gov", None)

# Return client as JSON from API / converted to Python list of
# dictionaries by sodapy.
results1 = client.get("9mfq-cb36", limit=56000,offset=100) # US COVID-19 Cases and Deaths by State over time
results2 = client.get("unsk-b7fc", limit=56000,offset=100) # Overall US COVID-19 Vaccine deliveries and administration data at national and jurisdiction level
#results3 = client.get("8xkx-amqh",limit=900000,offset=200) # Overall US COVID-19 Vaccine administration and vaccine equity data at county level
results4 = client.get("pj7m-y5uh",limit = 56000,offset=100) # Provisional COVID-19 Deaths: Distribution of Deaths by Race and Hispanic Origin


# Convert to pandas DataFrame & format needed columns
cases_deaths = pd.DataFrame.from_records(results1)
cases_deaths = cases_deaths.sort_values(by='submission_date')
cases_deaths[['tot_cases','conf_cases','prob_cases','new_case','pnew_case','tot_death','conf_death',
                     'prob_death','new_death','pnew_death']] = cases_deaths[['tot_cases','conf_cases','prob_cases',
                    'new_case','pnew_case','tot_death','conf_death','prob_death','new_death','pnew_death']].apply(pd.to_numeric)
cases_deaths['submission_date'] = pd.to_datetime(cases_deaths['submission_date'])

vaccine_state = pd.DataFrame.from_records(results2)
vaccine_state = vaccine_state.sort_values(by='date')

#vaccine_county = pd.DataFrame.from_records(results3)
#vaccine_county = vaccine_county.sort_values(by='date')

race_deaths = pd.DataFrame.from_records(results4)
race_deaths[['non_hispanic_white','non_hispanic_black_african_american','non_hispanic_american_indian_alaska_native',
               'non_hispanic_asian_pacific_islander','nh_nhopi','non_hispanic_more_than_one_race','hispanic_latino_total']] = race_deaths[['non_hispanic_white',
               'non_hispanic_black_african_american','non_hispanic_american_indian_alaska_native',
               'non_hispanic_asian_pacific_islander','nh_nhopi','non_hispanic_more_than_one_race','hispanic_latino_total']].apply(pd.to_numeric)



# Select data specific for Massachusetts
cases_deaths_MA = cases_deaths.loc[cases_deaths["state"].isin(['MA'])]
cases_deaths_MA.to_csv('case_deaths_MA.csv')

vaccine_state_MA = vaccine_state.loc[vaccine_state["location"].isin(['MA'])]
vaccine_state_MA.to_csv('vaccine_state_MA.csv')

#vaccine_county_MA = vaccine_county.loc[vaccine_county["recip_state"].isin(['MA'])]
#vaccine_county_MA.to_csv('vaccine_county_MA.csv')

race_deaths_MA = race_deaths.loc[race_deaths["state"].isin(['Massachusetts'])]
race_deaths_MA = race_deaths_MA.loc[race_deaths["year"].isin(['2020-2022'])]
race_deaths_MA.to_csv('race_deaths_MA.csv')


# Visualize daily new cases for MA
fig1 = px.line(cases_deaths_MA, x="submission_date", y="new_case", 
             labels={
                     "submission_date": "Submission Date",
                     "new_case": "Number of New Cases"
                 },
             
             title='Daily New COVID-19 Cases in Massachusetts')



fig1.write_html("C:/Users/Juan Varela/Jupyter_Projects/Data Science and Machine Learning/COVID19/MA_covid_cases.html")

# Visualize daily new deaths for MA
fig2 = px.line(cases_deaths_MA, x="submission_date", y="new_death", 
             labels={
                     "submission_date": "Submission Date",
                     "new_death": "Number of New Deaths"
                 },
             
             title='Daily New COVID-19 Related Deaths in Massachusetts')

fig2.write_html("C:/Users/Juan Varela/Jupyter_Projects/Data Science and Machine Learning/COVID19/MA_covid_deaths.html")

# Visualize total number of cases for MA
fig3 = px.line(cases_deaths_MA, x="submission_date", y="tot_cases", 
             labels={
                     "submission_date": "Submission Date",
                     "tot_cases": "Total Number of Cases"
                 },
             
             title='Total Count of COVID-19 Cases in Massachusetts')

fig3.write_html("C:/Users/Juan Varela/Jupyter_Projects/Data Science and Machine Learning/COVID19/MA_tot_covid_cases.html")

# Visualize total number of deaths for MA
fig4 = px.line(cases_deaths_MA, x="submission_date", y="tot_death", 
             labels={
                     "submission_date": "Submission Date",
                     "tot_death": "Total Number of Deaths"
                 },
             
             title='Total Count of COVID-19 Related Deaths in Massachusetts')

fig4.write_html("C:/Users/Juan Varela/Jupyter_Projects/Data Science and Machine Learning/COVID19/MA_tot_covid_deaths.html")
