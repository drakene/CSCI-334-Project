import os
import time
import sys
import pandas as pd
import numpy as np
import sklearn.pipeline
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import matplotlib.pyplot as plt
import data_preliminary_analysis as dataPrelim
from IPython.display import display

def stateTotalsForDay(currDay, county_level_dataset):
    currDayCondition = county_level_dataset['date'] == currDay
    currDay_county_data = county_level_dataset[currDayCondition]
    
    #create dataset for most recent state totals
    state_col = []
    sumCases_col = []
    sumDeaths_col = []
    for state in currDay_county_data.state.unique():
        state_col.append(state)
        sumCases_col.append(currDay_county_data.groupby('state')['cases'].sum()[state])
        sumDeaths_col.append(currDay_county_data.groupby('state')['deaths'].sum()[state])

    d = {'State': state_col,'Total Cases': sumCases_col, 'Total Deaths': sumDeaths_col}
    state_totals_dataset = pd.DataFrame(d)

    return state_totals_dataset

def stateTotalCasesForDay(currDay, county_level_dataset):
    currDayCondition = county_level_dataset['date'] == currDay
    currDay_county_data = county_level_dataset[currDayCondition]
    
    #create dataset for most recent state totals
    state_col = []
    sumCases_col = []
    for state in currDay_county_data.state.unique():
        state_col.append(state)
        sumCases_col.append(currDay_county_data.groupby('state')['cases'].sum()[state])

    d = {'State': state_col,'Total Cases': sumCases_col}
    state_totals_dataset = pd.DataFrame(d)

    return state_totals_dataset

def stateTotalsFor3Days(date0, date1, currDay, county_level_dataset ):
    # column names
    cases0 = "Total Cases " + date0
    deaths0 = "Total Deaths " + date0
    cases1 = "Total Cases " + date1
    deaths1 = "Total Deaths " + date1
    cases2 = "Total Cases " + currDay
    deaths2 = "Total Deaths " + currDay
    
    day0data = stateTotalsForDay(date0, county_level_dataset)
    day0data = day0data.rename(columns = {"Total Cases": cases0, "Total Deaths": deaths0})
    day1data = stateTotalsForDay(date1, county_level_dataset)
    day1data = day1data.rename(columns = {"Total Cases": cases1, "Total Deaths": deaths1})
    day2data = stateTotalsForDay(currDay, county_level_dataset)
    day2data = day2data.rename(columns = {"Total Cases": cases2, "Total Deaths": deaths2})

    first2 = day0data.merge(day1data, on = 'State')
    allDays = first2.merge(day2data, on = 'State')

    return allDays
    
def stateTotalCasesFor3Days(date0, date1, currDay, county_level_dataset ):
    # column names
    cases0 = "Total Cases " + date0
    cases1 = "Total Cases " + date1
    cases2 = "Total Cases " + currDay
    
    day0data = stateTotalCasesForDay(date0, county_level_dataset)
    day0data = day0data.rename(columns = {"Total Cases": cases0})
    day1data = stateTotalCasesForDay(date1, county_level_dataset)
    day1data = day1data.rename(columns = {"Total Cases": cases1})
    day2data = stateTotalCasesForDay(currDay, county_level_dataset)
    day2data = day2data.rename(columns = {"Total Cases": cases2})

    first2 = day0data.merge(day1data, on = 'State')
    allDays = first2.merge(day2data, on = 'State')

    return allDays

