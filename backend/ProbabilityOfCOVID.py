# -*- coding: utf-8 -*-
"""
Created on Wed Jan  6 19:45:27 2021

@author: kevin
"""
import numpy as np
import pandas as pd

# below is the calculation of the probability you have COVID
# this is a function of sex, age, and symptoms
# the prediction uses a logistic regressional analysis
# the paper is called "Real-time tracking of self-reported symptoms to predict COVID19

def sexFunction(sex):
    
    if sex.lower() == 'male':
        return 1.0
    elif sex.lower() == 'female':
        return 0.0
    else:
        return "Wrong Input"
    
def smellTasteFunction(smellTasteSymptom):

    if smellTasteSymptom.lower() == 'yes':
        return 1.0
    elif smellTasteSymptom.lower() == 'no':
        return 0.0
    else:
        return "Wrong Input"
    
def coughSymptom(coughSymptoms):

    if coughSymptoms.lower() == 'yes':
        return 1.0
    elif coughSymptoms.lower() == 'no':
        return 0.0
    else:
        return "Wrong Input"
    
def severeFatigue(severeFatigues):

    if severeFatigues.lower() == 'yes':
        return 1.0
    elif severeFatigues.lower() == 'no':
        return 0.0
    else:
        return "Wrong Input"
    
def skippedMeals(skippedMeal):

    if skippedMeal.lower() == 'yes':
        return 1.0
    elif skippedMeal.lower() == 'no':
        return 0.0
    else:
        return "Wrong Input"
    
# def symptomPredictionModel():
#     age = float(input("How old are you? Please enter an integer only. "))
#     print(age)
#     sex = str(input("Are you a male or female? Please answer specifically as ""male"" or ""female"". " )).lower()
#     print(sexFunction(sex))
    
#     smellTasteSymptom = str(input("Did you experience any loss of smell and taste? Please enter only yes or no as an answer. ")).lower()
#     print(smellTasteFunction(smellTasteSymptom))
    
#     coughSymptoms = str(input("Do you have severe or significant persistant coughs? Please enter only yes or no as an answer. ")).lower()
#     print(coughSymptom(coughSymptoms))
    
#     severeFatigues = str(input("Are you experiencing severe fatigue? Please enter only yes or no as an answer. ")).lower()
#     print(severeFatigue(severeFatigues))
    
#     skippedMeal = str(input("Have you skipped any meals recently? Please enter only yes or no as an answer. ")).lower()
#     print(skippedMeals(skippedMeal))
#     # this is the prediction model equation
#     prediction_model = -1.32-(0.01*age)+(0.44*sexFunction(sex))+(1.75*smellTasteFunction(smellTasteSymptom))+(0.31*coughSymptom(coughSymptoms))+(0.45*severeFatigue(severeFatigues))+(0.39*skippedMeals(skippedMeal))
    
#     # converts a probability value from a prediction model 
#     return np.exp(prediction_model)/(1+np.exp(prediction_model))

def symptomPredictionModel(age, sex, smellTasteSymptom, coughSymptoms, severeFatigues, skippedMeal):
    prediction_model = -1.32-(0.01*age)+(0.44*sexFunction(sex))+(1.75*smellTasteFunction(smellTasteSymptom))+(0.31*coughSymptom(coughSymptoms))+(0.45*severeFatigue(severeFatigues))+(0.39*skippedMeals(skippedMeal))
    
    # converts a probability value from a prediction model 
    return np.exp(prediction_model)/(1+np.exp(prediction_model))

# Community risk was a simple calculation of active cases divided by
# the county population. Note that these active cases should be adjusted with
# probable cases as updated appropriately with the DSHS
# population projection updated with texas.gov
def communityRisk():
    df = pd.read_csv('data/us-counties.csv') # data collected from NYTimes github
    hf = pd.read_csv('data/co-est2019-alldata.csv', encoding ="ISO-8859-1") # data collected from US census
    
   
    del df['date']
    del hf['SUMLEV']
    del hf['REGION']
    del hf['DIVISION']
    del hf['STATE']
    
    
    
    state_name = str(input("What state do you live in? ")) 
    county_name = str(input("What county do you live in? "))
    df = df.sort_values(by = ['county', 'state'])
    
    # narrowing the rows to just the state and county desired
    df_rowValue = df.loc[(df['state']== state_name) & (df['county'] == county_name)]
    # find the row number of a specific county and state for census dataframe
    hf_row = hf['Combined'].str.contains(state_name + county_name,na = False).idxmax()
    # reverse the dataframe 
    df_rowValue = df_rowValue[::-1]
    
    # locate the county population and county active cases
    county_population = hf.iloc[hf_row, 14]
    print("The population of", state_name + " " + county_name, "County is", county_population, "people.")
    county_totalCasesToday = df_rowValue.iloc[0,3]
    county_totalCasesTenDays = df_rowValue.iloc[10,3]
    county_activeCases = county_totalCasesToday - county_totalCasesTenDays
    print(county_name, "has", county_activeCases, "active cases.")
    # calculate the community risk
    communityRisk = int(county_activeCases)/int(county_population)
    
    return communityRisk
    
# multiply proportion of community infected with symptom prediction model
def totalSusceptibility():
    return communityRisk()*symptomPredictionModel(age, sex, smellTasteSymptom, coughSymptoms, severeFatigues, skippedMeal)
        
            
    
