# -*- coding: utf-8 -*-
"""CodeFest.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1hUru9ObNhb6-j5zrgP_LyHLIM8DF4Mck

# Imports
"""

import pandas as pd
import numpy as np
import pandas_datareader.data as web
import datetime
import matplotlib.pyplot as plt
import seaborn as sns

state_mapping = {
    'AL': 'Alabama',
    'AK': 'Alaska',
    'AZ': 'Arizona',
    'AR': 'Arkansas',
    'CA': 'California',
    'CO': 'Colorado',
    'CT': 'Connecticut',
    'DE': 'Delaware',
    'FL': 'Florida',
    'GA': 'Georgia',
    'HI': 'Hawaii',
    'ID': 'Idaho',
    'IL': 'Illinois',
    'IN': 'Indiana',
    'IA': 'Iowa',
    'KS': 'Kansas',
    'KY': 'Kentucky',
    'LA': 'Louisiana',
    'ME': 'Maine',
    'MD': 'Maryland',
    'MA': 'Massachusetts',
    'MI': 'Michigan',
    'MN': 'Minnesota',
    'MS': 'Mississippi',
    'MO': 'Missouri',
    'MT': 'Montana',
    'NE': 'Nebraska',
    'NV': 'Nevada',
    'NH': 'New Hampshire',
    'NJ': 'New Jersey',
    'NM': 'New Mexico',
    'NY': 'New York',
    'NC': 'North Carolina',
    'ND': 'North Dakota',
    'OH': 'Ohio',
    'OK': 'Oklahoma',
    'OR': 'Oregon',
    'PA': 'Pennsylvania',
    'RI': 'Rhode Island',
    'SC': 'South Carolina',
    'SD': 'South Dakota',
    'TN': 'Tennessee',
    'TX': 'Texas',
    'UT': 'Utah',
    'VT': 'Vermont',
    'VA': 'Virginia',
    'WA': 'Washington',
    'WV': 'West Virginia',
    'WI': 'Wisconsin',
    'WY': 'Wyoming'
}

city_to_county_state = {
    "New York City": "New York County, New York",
    "San Francisco": "San Francisco County, California",
    "Chicago": "Cook County, Illinois",
    "San Diego": "San Diego County, California",
    "Los Angeles": "Los Angeles County, California",
    "Washington DC": "District of Columbia, Washington DC",
    "Boston": "Suffolk County, Massachusetts",
    "Seattle": "King County, Washington",
    "San Antonio": "Bexar County, Texas",
    "Philadelphia": "Philadelphia County, Pennsylvania",
    "Houston": "Harris County, Texas",
    "Denver": "Denver County, Colorado",
    "Dallas": "Dallas County, Texas",
    "Phoenix": "Maricopa County, Arizona",
    "Austin": "Travis County, Texas",
    "Baltimore": "Baltimore City, Maryland",
    "Indianapolis": "Marion County, Indiana",
    "Charlotte": "Mecklenburg County, North Carolina",
    "Memphis": "Shelby County, Tennessee",
    "Columbus": "Franklin County, Ohio",
    "Jacksonville": "Duval County, Florida",
    "San Jose": "Santa Clara County, California",
    "Fort Worth": "Tarrant County, Texas",
    "Detroit": "Wayne County, Michigan",
    "El Paso": "El Paso County, Texas"
}

"""# X Data Sets"""

GDP_by_county = pd.read_csv('GDP_by_county.csv', header=0)
GDP_by_county = GDP_by_county.drop(columns = ['GeoFips'])
GDP_by_county = GDP_by_county.dropna()
def transform_geo_name(geo_name):
    county, postal_code = geo_name.rsplit(', ', 1)
    county_with_suffix = f"{county} County"
    state = state_mapping.get(postal_code, postal_code)
    return f"{county_with_suffix}, {state}"

GDP_by_county['Name'] = GDP_by_county['GeoName'].apply(transform_geo_name)
GDP_by_county = GDP_by_county.drop(columns = ['GeoName'])
GDP_by_county.rename(columns={'2022': 'GDP'}, inplace=True)
null_count = GDP_by_county['GDP'].isnull().sum()
GDP_by_county

temperatureByCounty = pd.read_csv('temperatureByCounty.csv', header=0, on_bad_lines='skip')
temperatureByCounty = temperatureByCounty.drop(columns = 'ID')
temperatureByCounty.rename(columns={'Value': 'Temp Val'}, inplace=True)
temperatureByCounty.rename(columns={'Anomaly (1901-2000 base period)': 'Temp Anomly'}, inplace=True)
temperatureByCounty.rename(columns={'Rank': 'Temp Rank'}, inplace=True)
temperatureByCounty.rename(columns={'1901-2000 Mean': 'Temp Mean'}, inplace=True)
temperatureByCounty['Name'] = temperatureByCounty['Name'] + ', ' + temperatureByCounty['State']
temperatureByCounty

poverty = pd.read_csv('poverty.csv', header=1)
poverty = poverty.drop(columns = ['State FIPS Code','County FIPS Code'])
poverty = poverty.drop(columns = ['Poverty Estimate, Age 0-4','90% CI Lower Bound.7','90% CI Upper Bound.7','Poverty Percent, Age 0-4','90% CI Lower Bound.8','90% CI Upper Bound.8'])

poverty['State'] = poverty['Postal Code'].replace(state_mapping)
poverty.drop(columns=['Postal Code'], inplace=True)
poverty['Name'] = poverty['Name'] + ', ' + poverty['State']
columns_to_modify = poverty.columns[poverty.columns != 'Name']
poverty[columns_to_modify] = poverty[columns_to_modify].replace(',', '', regex=True)
columns_to_convert = poverty.columns[poverty.columns != 'Name']
poverty[columns_to_convert] = poverty[columns_to_convert].apply(pd.to_numeric, errors='coerce')
poverty

precipitation = pd.read_csv('precipitation.csv', header=0, on_bad_lines='skip')
precipitation = precipitation.drop(columns = ['ID'])
precipitation.rename(columns={'Value': 'Precip Val'}, inplace=True)
precipitation.rename(columns={'Anomaly (1901-2000 base period)': 'Precip Anomly'}, inplace=True)
precipitation.rename(columns={'Rank': 'Precip Rank'}, inplace=True)
precipitation.rename(columns={'1901-2000 Mean': 'Precip Mean'}, inplace=True)
precipitation['Name'] = precipitation['Name'] + ', ' + precipitation['State']
precipitation

Hotel_GDP_by_county = pd.read_csv('HotelGDP.csv', header=0)
Hotel_GDP_by_county = Hotel_GDP_by_county.drop(columns = ['GeoFips'])
Hotel_GDP_by_county = Hotel_GDP_by_county.dropna()
Hotel_GDP_by_county['Name'] = Hotel_GDP_by_county['GeoName'].apply(transform_geo_name)
Hotel_GDP_by_county = Hotel_GDP_by_county.drop(columns = ['GeoName'])
Hotel_GDP_by_county.rename(columns={'2022': 'Hotel_GDP'}, inplace=True)
Hotel_GDP_by_county.dropna()

"""# Y Data Set"""

location_score = pd.read_csv('hotel1.csv')
location_score = location_score.dropna()
location_score['Name'] = location_score['city'].map(city_to_county_state)
location_score['Name'] = location_score['Name'].astype(str)
location_score

"""# Merge Data Sets"""

Total_df = pd.merge(temperatureByCounty, precipitation, how='left', on='Name')

Total_df = pd.merge(Total_df, poverty, how='left', on='Name')
Total_df.drop(columns=['State_y','State_x','State'], inplace=True)

Total_df = pd.merge(Total_df, GDP_by_county, how='left', on='Name')

Total_df = pd.merge(Total_df, Hotel_GDP_by_county, how='left', on='Name')

columns_to_convert = Total_df.columns[Total_df.columns != 'Name']
Total_df[columns_to_convert] = Total_df[columns_to_convert].apply(pd.to_numeric, errors='coerce')


Total_df = pd.merge(location_score, Total_df, how='left', on='Name')
Total_df = Total_df[Total_df['city'] != 'Washington DC']

Total_df

"""# Split as X and Y"""

y = Total_df['location_rating']
null_sum = y.isnull().sum()
null_sum
y

x = Total_df.drop(['location_rating','Name','city'],axis=1)
x

from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=100)
x_train = x_train.reset_index(drop=True)
x_test = x_test.reset_index(drop=True)
y_train = y_train.reset_index(drop=True)
y_test = y_test.reset_index(drop=True)

x_test

x_train
print(x_train.dtypes)

y_test

y_train

print(x_train.isnull().sum())
print(y_train.isnull().sum())

"""# XGBoost"""

import xgboost as xgb
XGB_Model = xgb.XGBRegressor(

    n_estimators=600,
    max_depth=3,
    learning_rate=0.008,
    subsample=0.5,
    colsample_bytree=0.4,
    min_child_weight=5,
    reg_lambda=2,
    reg_alpha=0.1

    )
XGB_Model.fit(x_train, y_train)
y_train_pred = XGB_Model.predict(x_train)
y_test_pred = XGB_Model.predict(x_test)
y_test_pred = np.clip(y_test_pred, 1, 5)

from sklearn.metrics import mean_squared_error

rf_train_mse = mean_squared_error(y_train,y_train_pred)

rf_test_mse = mean_squared_error(y_test,y_test_pred)

mse_residual = abs(rf_train_mse - rf_test_mse)
results = pd.DataFrame(['XGBOOST',rf_train_mse,rf_test_mse,mse_residual]).transpose()
results.columns = (['Method','Training MSE','Test MSE','Resid MSE'])
results