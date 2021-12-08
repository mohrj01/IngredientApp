# imports
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt # plotting
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import streamlit as st
import re

# importing recipe data
df = pd.read_csv('https://raw.githubusercontent.com/mohrj01/IngredientApp/master/clean_recipes.csv', delimiter=';')

# copy so don't overwrite both
df1 = df.copy()
df1.columns = [c.replace(' ', '_') for c in df1.columns]

# Only keeping cookies
df1 = df1[df1['Recipe_Name'].str.contains('Cookie', case = False)]
df1['Orig_Ingredients'] = df1['Ingredients']

# ingredient list cleanup
# removing all digits
df1['Ingredients'] = df1['Ingredients'].str.replace('\d+', '')
# removing info that is not related to the ingredient
def myreplace(s):
    for ch in ['cups', 'cup', 'tablespoons', 'tablespoon', 'teaspoons', 'drops', 'drop ', 'teaspoon', 'pounds', 'pound','fluid ounce', 'ounces', 'ounce',  'fluid', 'dashes', 'dash', 'gallon', 'pinch',
               '/', 'and ', '.', '(', ')', '-',
               'crushed', 'diced', 'cleaned', 'cubed', 'divided', 'drained', 'chopped', 'mashed', 'halved', 'julienned', 'peeled', 'segmented', 'shredded', 'rinsed', 'torn', 'soaked', 'split', 'stemmed', 'thawed', 'to taste', 'washed', 'warmed',
              'cans', 'packages', 'jars', 'bottles', 'packets', 'package', 'can ', 'jar', 'bottle', 'optional', 'packet', 'recipe', 'sheets', 'sheet',
              'whole', 'large', 'small', 'finely', 'inch', 'square', 'uncooked', 'cooked', 'frozen', 'round', 'prepared', 'any color',
              'alcoholic', 'fat free', 'low fat', 'low sodium', 'fat', 'england', 'london', '(see Note)', 'fry', 'kosher for passover', 'kosher', 'lunch', 'rating', 'raw ', 'side', 'topping thawed',
              'chill', 'gram ', 'mixed with:', 'cookies', 'cookie', 'To Layer In Jar:', 'bake', 'Topping:']:
        s = s.replace(ch, '')

    # remove extra spaces
    s = re.sub(' +', ' ', s)
    return s

df1['Ingredients'] = df1['Ingredients'].map(myreplace)
# replacing symbols
df1['Ingredients'] = df1['Ingredients'].str.replace(', ', ',')
df1['Ingredients'] = df1['Ingredients'].str.replace(' ,', ',')
df1['Ingredients'] = df1['Ingredients'].str.replace('"', '')

# split along the commas
df1.Ingredients = df1.Ingredients.apply(str).str.split(",")
# get dummy variable for each ingredient
df1 = df1[["Recipe_Name", "Total_Time", "Ingredients", "RecipeID", "Orig_Ingredients"]].join(df1.Ingredients.str.join('|').str.get_dummies())


# Creating Time Variables
df = df[df['Recipe Name'].str.contains('Cookie', case = False)]

df['Total Time'] = df['Total Time'].replace("X", "Unknown")
df['Total Time'] = df['Total Time'].replace("1 d", "23 h")
df['Total Time'] = df['Total Time'].replace("Unknown", "23 h 59 m")

# if doesn't contain an hour indicator, add 0 hrs
df["TT1"] = "0 h "+ df[df["Total Time"].str.contains('h')==False]['Total Time']
# if doesn't contain a minute indicator, add 0 mins
df["TT2"] = df[df["Total Time"].str.contains('m')==False]['Total Time'] + " 0 m"

# combine all into TT1
df.loc[df["TT1"].isnull(), "TT1"] = df["TT2"]
df.loc[df["TT1"].isnull(), "TT1"] = df["Total Time"]

# put unknowns back
df['Total Time'] = df['Total Time'].replace("23 h 59 m", "Unknown")

# expand into two columns: hours and minutes. remove anything that isn't the digit
df[['hours','minutes']] = df.TT1.str.split('h', expand=True)
df['hours'] = df['hours'].str.replace('\D', '')
df['minutes'] = df['minutes'].str.replace('\D', '')

# calculate total time as hours column * 60 plus minutes column
df['hours']=pd.to_numeric(df['hours'])
df['minutes']=pd.to_numeric(df['minutes'])
df['combined_time'] = df['hours']*60 + df['minutes']


# Add ratings
df_rev = pd.read_csv('https://raw.githubusercontent.com/mohrj01/IngredientApp/master/clean_reviews_reduce.csv', delimiter=',')
ratings = df_rev.groupby(['RecipeID'], as_index = False)['Rate'].mean()
df = df.merge(ratings, how = "left")
# round and fill NAs
df = df.round({'Rate': 2})
df['Rate'] = df['Rate'].fillna("No Ratings")


# export pickle
import pickle as pkl
with open("df1_ing.pkl" , "wb") as file4:
  pkl.dump(df1,file4)

with open("df_ing.pkl" , "wb") as file4:
  pkl.dump(df,file4)
