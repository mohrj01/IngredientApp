from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt # plotting
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import streamlit as st

#import warnings
#warnings.filterwarnings('ignore')

#blob/main/
#https://github.com/mohrj01/IngredientApp/blob/069ba3b71a509b24fdbdf16ec6bec79a2da113f4/clean_recipes.csv
#'https://github.com/mohrj01/IngredientApp/clean_recipes.csv'
#https://raw.githubusercontent.com/mohrj01/IngredientApp/master/clean_recipes.csv
st.write('test')
df = pd.read_csv('https://raw.githubusercontent.com/mohrj01/IngredientApp/master/clean_recipes.csv', delimiter=';')
df.head()
#df = pd.read_csv('/kaggle/input/recipe-ingredients-and-reviews/clean_recipes.csv', delimiter=';')
#df.dataframeName = 'clean_recipes.csv'
nRow, nCol = df.shape
print(f'There are {nRow} rows and {nCol} columns')


# copy so don't overwrite both
df1 = df.copy()
df1.columns = [c.replace(' ', '_') for c in df1.columns]

# Only keeping cookies
df1 = df1[df1['Recipe_Name'].str.contains('Cookie', case = False)]
df1['Orig_Ingredients'] = df1['Ingredients']


#https://stackoverflow.com/questions/54152673/python-function-to-loop-through-columns-to-replace-strings

import re
# removing all digits
df1['Ingredients'] = df1['Ingredients'].str.replace('\d+', '')

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
    #s = s.strip()
    #print(s)
    return s
# remove trailing/leading white space

df1['Ingredients'] = df1['Ingredients'].map(myreplace)

df1['Ingredients'] = df1['Ingredients'].str.replace(', ', ',')
df1['Ingredients'] = df1['Ingredients'].str.replace(' ,', ',')
df1['Ingredients'] = df1['Ingredients'].str.replace('"', '')


#pd.set_option('display.width', None)
#pd.set_option('display.max_colwidth', -1)
#df1[df1['RecipeID'].isin([7936, 12821])]



df1.Ingredients = df1.Ingredients.apply(str).str.split(",")

#https://stackoverflow.com/questions/43945816/convert-list-of-strings-to-dummy-variables-with-pandas
#.add_prefix('ing_')
df1 = df1[["Recipe_Name", "Total_Time", "Ingredients", "RecipeID", "Orig_Ingredients"]].join(df1.Ingredients.str.join('|').str.get_dummies())


# Creating Time Variables
df = df[df['Recipe Name'].str.contains('Cookie', case = False)]

df['Total Time'] = df['Total Time'].replace("X", "Unknown")
df['Total Time'] = df['Total Time'].replace("1 d", "23 h")
df['Total Time'] = df['Total Time'].replace("Unknown", "23 h 59 m")

df["TT1"] = "0 h "+ df[df["Total Time"].str.contains('h')==False]['Total Time']
df["TT2"] = df[df["Total Time"].str.contains('m')==False]['Total Time'] + " 0 m"

df.loc[df["TT1"].isnull(), "TT1"] = df["TT2"]
df.loc[df["TT1"].isnull(), "TT1"] = df["Total Time"]

df[df["Total Time"].str.contains('h')==False]

df['Total Time'] = df['Total Time'].replace("23 h 59 m", "Unknown")

df[['hours','minutes']] = df.TT1.str.split('h', expand=True)
df['hours'] = df['hours'].str.replace('\D', '')
df['minutes'] = df['minutes'].str.replace('\D', '')

df['hours']=pd.to_numeric(df['hours'])
df['minutes']=pd.to_numeric(df['minutes'])
df['combined_time'] = df['hours']*60 + df['minutes']

# Add ratings
df_rev = pd.read_csv('https://raw.githubusercontent.com/mohrj01/IngredientApp/master/clean_reviews_reduce.csv', delimiter=',')
ratings = df_rev.groupby(['RecipeID'], as_index = False)['Rate'].mean()
df = df.merge(ratings, how = "left")

df = df.round({'Rate': 2})
df['Rate'] = df['Rate'].fillna("No Ratings")

# export
import pickle as pkl
with open("df1_ing.pkl" , "wb") as file4:
  pkl.dump(df1,file4)

with open("df_ing.pkl" , "wb") as file4:
  pkl.dump(df,file4)
