
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt # plotting
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import streamlit as st


st.title('Cookie Recipe Finder')
st.write('By Jessica Mohr')
st.write('12/8/2021')
st.write('MABA ML Final Project')
st.write("[Github](%s)" % "https://github.com/mohrj01/IngredientApp")

st.header('Introduction')

df = pd.read_csv('https://raw.githubusercontent.com/mohrj01/IngredientApp/master/clean_recipes.csv', delimiter=';')

import pickle as pkl
with open("df1_ing.pkl" , "rb") as file4:
    df1 = pkl.load(file4)




# user input
distance_columns = list(df1.columns.values)
distance_columns = distance_columns[5:]
user_input = st.multiselect(
            'What ingredients would you like to use?',
            distance_columns
        )

st.write('You selected:', user_input)


#user_input = ['strawberry', 'egg', 'pecan']
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


choice_df2 = df2[df2['Recipe_Name'] == most_similar_to_lebron]
choice = df[df['Recipe Name'] == most_similar_to_lebron]
st.write('Recipe using the most ingredients:', choice['Recipe Name'])
st.write('Author:', choice['Author'])
st.write('Directions:', choice['Directions'])


r = pd.DataFrame(choice['Recipe Photo'])
st.write(r.head())

#st.write((choice['Recipe Photo'][0]))

choice_photo = choice['Recipe Photo'].to_string()
choice_photo_2 = choice['Recipe Photo']
l=[]
for i in choice_photo_2:
    l.append(i)
    st.write(i)
    
st.write("checkpoint1")
st.write(l[0])

final_photo = l[0]
st.image(final_photo)
st.caption(final_photo)

st.write(choice['Recipe Photo'])

#choice_photo_2 = choice_photo[:5]


choice_photo = choice_photo[5:]
#choice_photo = ('"'+choice_photo+'"')
choice_photo = choice_photo.replace(" ", "")
choice_photo2 = ('"'+choice_photo+'"')

#choice_photo = ('"'+choice['Recipe Photo']+'"').to_string()
#choice_photo = (choice['Recipe Photo']).to_string()
st.write(choice_photo)
#st.image(choice_photo, width=400)
#st.image("https://images.media-allrecipes.com/images/79591.png", width=400)
st.text(choice_photo)

#st.write("check out this [link](https://share.streamlit.io/mesmith027/streamlit_webapps/main/MC_pi/streamlit_app.py)")
#st.write("check out this [link]"choice_photo)

url = choice_photo2
st.write(choice_photo2)
st.write("check out this [link](%s)" % url)
st.markdown("check out this [link](%s)" % url)



#img_bytes = Path(choice_photo).read_bytes()
#st.image(img_bytes)

#from PIL import Image
#img = Image.open(choice_photo)
#st.image(img)

#%%

# ingredients this choice has in common
choice_in = choice_df2['Ingredients']
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

st.write('Ingredients that match are:', match_in)
st.write('Ingredients you still need are:', need_in)





#%%

# for me to fix now
# display cook time in final result
# display link to recipe

#%%

# future ideas
# add in cook time (as user choice)
# add in weighted KNN > user can select the one ingredient they for sure want to use, weight it heigher


# if only select 1 ingredient, will choose the recipe with the lowest amount of ingredints bc all of the 0s match...




#sa = StreamlitApp()
#sa.construct_app()
