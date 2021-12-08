# imports
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt # plotting
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import streamlit as st
import math
from scipy.spatial import distance

# Title
st.title('Cookie Recipe Finder')
st.image('https://leclerc-business-site-production.s3.amazonaws.com/uploads/2018/05/08/13/33/11/09be0c78-9eba-4786-910c-4030e6333bff/header-image.png')
st.write("Jessica Mohr  |  12/08/2021  |  MABA ML Final Project  |  [Github](%s)" % "https://github.com/mohrj01/IngredientApp")

# INTRODUCTION
st.header('Introduction')
st.write('This app will take two user inputs: the ingredients they wish to use in their cookies and the maximum amount of time they have to make their cookies. '
         "The model will then filter down to recipes within the user's time limit and apply K Nearest Neighbors to their ingredient selection in order to find "
         "the recipe that uses the largest amount of their ingredients. The model prioritiezes using as many of the user inputed ingredients as possible and "
         "does not punish recipes in which the user is missing many ingredients. The output is a single recipe, with author, time to cook, average rating, "
         "directions, and photo. A list is also included of the ingredients the user has that match the requirements of the recipe and a list of the ingredients "
         "that the user still needs to acquire. A download button above the later list provides an excel file of the ingredients the user needs to purchase (their shopping list).")

# load pre-processed data
import pickle as pkl
with open("df1_ing.pkl" , "rb") as file4:
    df1 = pkl.load(file4)
    
import pickle as pkl
with open("df_ing.pkl" , "rb") as file4:
    df = pkl.load(file4)


# INGREDIENT SELECTION
st.header('Ingredient Selection')

# allow user to select between all of the possible ingredients in the cookie recipes
# ignore the first 5 columns because not ingredient dummy variables
distance_columns = list(df1.columns.values)
distance_columns = distance_columns[5:]
user_input = st.multiselect(
            'What ingredients would you like to use?',
            distance_columns)

# TIME LIMIT SELECTION
# allow user to use slider to select maximum time
# if user_time specify infinity, then set user_time = 200 in order to capture all non specified recipes
st.header("Time Limit Selection")
user_time = st.select_slider('What is the maximum time you want to spend (in hours)?', [1,2,3,4,5,6,7,8,"∞"], help="Select infinity to show recipes with no time indicated")
if user_time == "∞":
    user_time = 200
user_time = int(user_time)

# MODELING
# add the users selections as a row to the dataframe
my_in = pd.DataFrame(data ={'Recipe_Name': ["user input"], 'RecipeID': [0],  'Ingredients': [user_input]})
my_in = my_in[["Recipe_Name", "RecipeID", "Ingredients"]].join(my_in.Ingredients.str.join('|').str.get_dummies())

# if set na to .5 if recepie doesn't require, penalize .5. if recepie requires, penalize .5
# focus on finding recepies that match items you HAVE rather than match items you don't have.
# prioritizes using as many of your items as possible

# copy dataset
df2 = df1.copy()
# filter to be below user time requirements
user_time = user_time*60
df_IDS = df[df['combined_time']<user_time]
df2 = df1[df1.RecipeID.isin(df_IDS.RecipeID)]
# add user input to copied dataset, if na then .5 because of the reason above
df2 = df2.append(my_in).fillna(.5)

# select the newly added row (user input)
selected_row = df2[df2['Recipe_Name'] == 'user input'].iloc[0]

# euclidean distance function for KNN
def euclidean_distance(row):
    inner_value = 0
    for k in distance_columns:
        inner_value += (row[k] - selected_row[k]) ** 2
    return math.sqrt(inner_value)

selected_distance = df2.apply(euclidean_distance, axis=1)

# Reference: https://www.dataquest.io/blog/k-nearest-neighbors-in-python/
df2_num = df2[distance_columns]
selected_row = df2_num[df2['Recipe_Name'] == 'user input']
euclidean_distances = df2_num.apply(lambda row: distance.euclidean(row, selected_row), axis=1)
# Create a new dataframe with distances.
distance_frame = pd.DataFrame(data={"dist": euclidean_distances, "idx": euclidean_distances.index})
distance_frame.sort_values("dist", inplace = True)
# Find the most similar player to user's choice (the lowest distance to their choice is their choice, the second smallest is the most similar non-user choice)
second_smallest = distance_frame.iloc[1]["idx"]
most_similar_to_selected = df2.loc[int(second_smallest)]["Recipe_Name"]

# User's choice
choice = df[df['Recipe Name'] == most_similar_to_selected]


# COOKIE RECIPE RESULT
st.header("Cookie Recipe Result")
# Print Recipe Info
col1, col2 = st.columns(2)
col1.write("Recipe using the most ingredients:")
col1.write("Author:")
col1.write("Time to Make:")
col1.write("Average Rating:")
for i in choice['Recipe Name']:
    col2.write(i)
# Print Recipe Author
for i in choice['Author']:
    col2.write(i)
# Print total time
for i in choice['Total Time']:
    col2.write(i)
# Print Rating
for i in choice['Rate']:
    col2.write(i)
# Print Recipe Directions
for i in choice['Directions']:
    st.write(i)

# Print Photo
choice_photo = choice['Recipe Photo']
l=[]
for i in choice_photo:
    l.append(i)
    
final_photo = l[0]
st.image(final_photo)


# INGREDIENT INVENTORY
# ingredients this choice has in common
choice_df2 = df2[df2['Recipe_Name'] == most_similar_to_selected]
choice_in = choice_df2['Ingredients']

# create list of ingredients in selected recipe, clean up
choice_in = ','.join(str(y) for x in choice_in for y in x if len(x) > 0)
choice_in= choice_in.replace("'", '')
choice_in= choice_in.replace("[", '')
choice_in= choice_in.replace("]", '')
choice_in = choice_in.split(",")
# remove duplicates
choice_in = list(dict.fromkeys(choice_in))

# find where ingredients are the same
def intersection(list1, list2):
    similar = [value for value in list1 if value in list2]
    return similar

# ingredients that match
match_in = (intersection(choice_in, user_input))
# ingredients that are still needed
need_in = list(set(choice_in) - set(user_input))
st.header("Ingredient Inventory")
col1, col2 = st.columns(2)
col1.metric(label="Ingredients You Have", value=len(match_in))
col2.metric(label="Ingredients You Need", value=len(need_in))

# Create download CSV
dict = {"Ingredients Needed": need_in}
df_download = pd.DataFrame(dict)
choice_in = choice['Ingredients']

name = []
for i in choice['Recipe Name']:
    name.append(i)

name = str(name)
name = name.replace('[', '')
name = name.replace(']', '')
name = name.replace("'", '')

my_download = ("Ingredients Needed for "+ str(name) + ".csv")

@st.cache
def convert_df(df):
    return df.to_csv(index=False).encode('utf-8')

csv = convert_df(df_download)
col2.download_button("Download Shopping List", csv, file_name = my_download)

st.markdown("---")
col1, col2 = st.columns(2)
for i in match_in:
    col1.write(i)

for i in need_in:
    col2.write(i)

    
# footer image
st.image('https://sweetgirlcookies.com/wp-content/uploads/2021/08/cookie-header-1.png')

