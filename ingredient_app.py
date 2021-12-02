
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt # plotting
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)


import warnings
warnings.filterwarnings(‘ignore’)

df = pd.read_csv('https://github.com/mohrj01/IngredientApp/blob/main/clean_recipes.csv')
df.head()
#df = pd.read_csv('/kaggle/input/recipe-ingredients-and-reviews/clean_recipes.csv', delimiter=';')
df.dataframeName = 'clean_recipes.csv'
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


# user input
user_input = ['strawberry', 'egg', 'pecan']
#my_in = pd.DataFrame(my_in)
my_in = pd.DataFrame(data ={'Recipe_Name': ["user input"], 'RecipeID': [0],  'Ingredients': [user_input]})


my_in = my_in[["Recipe_Name", "RecipeID", "Ingredients"]].join(my_in.Ingredients.str.join('|').str.get_dummies())

# k nearest neighbors?
# show names
# show missing ingredients from each one


# if set na to -1, then  if recepie does not require ingredient: penalize 1
#                         if recepie has ingredient: penalize 2
#                         difference: 1

# if set na to 0, then  if recepie does not require ingredient: penalize 0
#                         if recepie has ingredient: penalize 1
#                         difference 1
# if set na to .5 if recepie doesn't require, penalize .5. if recepie requires, penalize .5
# focus on finding recepies that match items you HAVE rather than match items you don't have.
# prioritizes using as many of your items as possible

# add user input to dataset, if na then 0
df2 = df1.copy()
df2 = df2.append(my_in).fillna(.5)
#df2 = df2.append(my_in).fillna(0)

distance_columns = list(df2.columns.values)
distance_columns = distance_columns[5:]

#distance_columns = ['butter', 'salt', 'pecan']
selected_player = df2[df2['Recipe_Name'] == 'user input'].iloc[0]
              

import math

def euclidean_distance(row):

    inner_value = 0
    for k in distance_columns:
        inner_value += (row[k] - selected_player[k]) ** 2
    return math.sqrt(inner_value)

lebron_distance = df2.apply(euclidean_distance, axis=1)


#https://www.dataquest.io/blog/k-nearest-neighbors-in-python/

from scipy.spatial import distance

df2_num = df2[distance_columns]
selected_player = df2_num[df2['Recipe_Name'] == 'user input']                                   
euclidean_distances = df2_num.apply(lambda row: distance.euclidean(row, selected_player), axis=1)
# Create a new dataframe with distances.
distance_frame = pd.DataFrame(data={"dist": euclidean_distances, "idx": euclidean_distances.index})
#distance_frame.sort("dist", inplace=True)
distance_frame.sort_values("dist", inplace = True)
# Find the most similar player to lebron (the lowest distance to lebron is lebron, the second smallest is the most similar non-lebron player)
second_smallest = distance_frame.iloc[1]["idx"]
most_similar_to_lebron = df2.loc[int(second_smallest)]["Recipe_Name"]


choice = df2[df2['Recipe_Name'] == most_similar_to_lebron]


#%%

# ingredients this choice has in common
choice_in = choice['Ingredients']
# choice ingredients
#choice_in = choice['Ingredients'].astype(str).values.tolist()
#choice_in = choice['Ingredients'].tolist()
#choice_in = choice_in.split(',')
#choice_in = (x[0] for x in choice_in)
#choice_in = [''.join(i) for i in choice_in]

#choice.Ingredients = choice.Ingredients.apply(str).str.split(",")
#my_choice = choice.Ingredients.str.join('|')

# create list of ingredients in selected recipe
choice_in = ','.join(str(y) for x in choice_in for y in x if len(x) > 0)
choice_in= choice_in.replace("'", '')
choice_in= choice_in.replace("[", '')
choice_in= choice_in.replace("]", '')
choice_in = choice_in.split(",")
# remove duplicates
choice_in = list(dict.fromkeys(choice_in))


def intersection(list1, list2):
    similar = [value for value in list1 if value in list2]
    return similar

match_in = (intersection(choice_in, user_input))
need_in = list(set(choice_in) - set(user_input))
# ingredients you need to buy
#list(set(choice).difference(user_input))

#print("Ingredients that match are:")
#print(match_in)
#print("Ingredients you still need are:")
#print(need_in)





#%%

# for me to fix now
# display cook time in final result
# display link to recipe

#%%

# future ideas
# add in cook time (as user choice)
# add in weighted KNN > user can select the one ingredient they for sure want to use, weight it heigher


# if only select 1 ingredient, will choose the recipe with the lowest amount of ingredints bc all of the 0s match...
