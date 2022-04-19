# -*- coding: utf-8 -*-
"""
Created on Fri Jul  2 11:48:49 2021

@author: Simon Pommerencke Melgaard
"""

import plotly.io as pio
import plotly.express as px
import pandas as pd
import os
import json
import geopandas as gpd


########## Define the data paths ############################################

path_main = format(os.getcwd())                                                 # Path to the folder
path_country_codes = path_main + '\\Country_codes.txt'                          # Path to the txt file containing the ISO-3 country codes
path_geojson = path_main + '\\custom.geo.json'                                  # Path to the geojson file (specifies the location of each country)
path_data = path_main + '\\Data.xlsx'                                           # Path to the excel file containing the data





###### defines the ISO_3166-1_alpha-3 country codes ########################
country_codes = {}
country_counter = []
with open(path_country_codes) as f:
    for line in f:
        (val,key) = line.split(maxsplit=1)
        country_counter.append(val)
        if '\n' in key:                                                         # The following if sentences removes redundancies in the official naming of the countries, so it fits the naming in the excel file
            key = key[:-1]
        if key == 'Taiwan, Province of China':
            key = 'Taiwan'
        if key == 'United States of America':
            key = 'USA'
        if key == 'United Kingdom of Great Britain and Northern Ireland':
            key = 'United Kingdom of Great Britain'
        if key == 'Korea, Republic of':
            key = 'South Korea'
        if key == 'British Indian Ocean Territory':
            key = 'British Indi Ocean Territory'
        country_codes[key] = val
empty_col = [0 for x in range(len(country_counter))]
country_counter =[country_counter, empty_col]                                   # Creates the list which is used to count how many times each country is mentioned


#%% ######## Import geojson data ################################################

with open(path_geojson) as f:
  geo_data = json.load(f)

#%% ######## Import the data from the excel sheet ###############################

#file_debug = open("Debug_file.txt","w")                                        # The debug file for the data import and counter




df = pd.read_excel (r''+path_data)                                              # Imports the excel data into a dataframe


for ind in range(len(df)):
    temp_country = df['Country'][ind]
    #file_debug.write('country = '+str(temp_country)+'\n')
    if type(temp_country) == float:                                             # Does not count if there is no country in the "Country" column
        #file_debug.write('No country\n\n')
        pass
    else:
        temp_country = temp_country.upper()                                     # Upper cases the entire name, so potential capital letters do not give errors
        temp_country = temp_country.split(' / ')                                # Tries to split the text string into individual countries (a list)
        if type(temp_country) == list:                                          # If there was more than one country the current data
            for country in temp_country:
                for keys in country_codes:
                    if country in keys.upper():
                        country_counter[1][country_counter[0].index(country_codes[keys])] +=1
                        #file_debug.write(str(country_counter[0][country_counter[0].index(country_codes[keys])])+'\n')
        else:                                                                   # If there was only one country in the string
            for keys in country_codes:
                if temp_country in keys.upper():
                    country_counter[1][country_counter[0].index(country_codes[keys])] +=1
                    #file_debug.write('added '+str(country_counter[0][country_counter[0].index(country_codes[keys])])+'\n')
        #file_debug.write('\n\n')



#%% ############ create the dataframe ###############################################
df = px.pd.DataFrame()
df['adm0_a3']=(country_codes.values())
df['location_name']=(country_codes.keys())
df['times_used']=(country_counter[1])



#%% ###### World map plot with colours according to countries in the excel ###

pio.renderers.default = "browser"

geo_df = gpd.GeoDataFrame.from_features(geo_data["features"]).merge(df,on='adm0_a3').assign(lat=lambda d: d.geometry.centroid.y, lon=lambda d: d.geometry.centroid.x).set_index('adm0_a3')

geo_df.index.names = ['Country']
geo_df.rename(columns={'times_used':'Articles published'},inplace=True)


colorscale=[(0, "#E5ECF6"),(0.1, "grey"), (1, "black")]


fig = px.choropleth(geo_df,
                           locations=geo_df.index,
                           color="Articles published",
                           color_continuous_scale=colorscale)


fig.update_coloraxes(colorbar_len=0.75)
fig.update_layout(font_family="Times New Roman")





fig.write_image("World_map_FDD.svg")

fig1 = px.choropleth(geo_df,
                           locations=geo_df.index,
                           color="Articles published",
                           color_continuous_scale=colorscale)
fig1.update_coloraxes(colorbar_xanchor="right")
fig1.update_coloraxes(colorbar_xpad=30)
fig1.update_coloraxes(colorbar_yanchor="middle")
fig1.update_coloraxes(colorbar_ypad=0)

fig1.update_coloraxes(colorbar_len=1)
fig1.update_layout(font_family="Times New Roman")


fig1.show()

fig1.write_html("World_map_FDD.html")

















