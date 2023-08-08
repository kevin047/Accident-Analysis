from django.shortcuts import render
from django.http import HttpResponse
import matplotlib.pyplot as plt

# Create your views here.

import pandas as pd
import numpy as np
from io import StringIO
import folium
from folium.plugins import HeatMap
import seaborn as sns
sns.set_style("darkgrid")

""" Load file using pandas
    Look at some info about data and colums
    Fix any missing or incorrect values
"""
def main():
    datafile = 'usaccidents\\US_Accidents_Dec21_updated.csv'
    my_list=[]

    # Read CSV 0
    df = pd.read_csv(datafile)
    my_list.append(df)

    # Read Columns 1
    my_list.append(df.columns)

    # Read  Info 2
    # print(df.info())
    output1 = StringIO()
    df.info(buf=output1)
    my_list.append(output1.getvalue())

    #DF Describe Std  Mean  Devaiation 3
    # pd.set_option('display.max_columns',None)
    my_list.append(df.describe())
    # pd.reset_option('display.max_columns')

    # Missing values per columns
    missing_percentages = df.isna().sum().sort_values(ascending=False) / len(df)
    ax = missing_percentages[missing_percentages != 0].plot(kind='barh', figsize=(8,4.8))
    plt.subplots_adjust(left=0.2)
    plt.savefig('E:\\Win K\\4th SEM\\PSC\\direct1\\src\\static\\images\\missing.jpg')
    
    #Remove columns that you don't want to use but not good practice

    #Exploratory Analysis & Visualisation

    #Cities
    my_list.append(df.City) #[4]
    my_list.append(len(df.City.unique())) #[5]

    #Cities and their values of accidents 6
    cities_by_accidents = df.City.value_counts()
    my_list.append(cities_by_accidents)

    #Top 20 cities by accidents 7
    my_list.append(cities_by_accidents[:20])
    
    ax = cities_by_accidents[:20].plot(kind='barh', figsize=(8,4.8))
    plt.subplots_adjust(left=0.2)
    plt.savefig('E:\\Win K\\4th SEM\\PSC\\direct1\\src\\static\\images\\top20city.jpg')



    sns.histplot(cities_by_accidents, log_scale=True)
    plt.subplots_adjust(left=0.2, bottom=0.2)
    # plt.savefig('E:\\Win K\\4th SEM\\PSC\\direct1\\src\\static\\images\\cityvsacci.jpg')

    # cities with only 1 accident count 8
    my_list.append(cities_by_accidents[cities_by_accidents == 1])


    #Timing Analaysis
    my_list.append(df.Start_Time) #[9]

    df['Start_Time'] = df['Start_Time'].astype(str)
    df_filtered=df[df['Start_Time'].str.match(r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$') == True]

    # df_filtered['Start_Time'] = pd.to_datetime(df_filtered['Start_Time'],format='%Y-%m-%d %H:%M:%S')
    # sns.histplot(df_filtered['Start_Time'].dt.hour, bins=24, kde=False, stat='density')
    # plt.subplots_adjust(left=0.2, bottom=0.2)
    # plt.savefig('E:\\Win K\\4th SEM\\PSC\\direct1\\src\\static\\images\\starttime.jpg')

#Weekdays vs their density of records present
    # sns.histplot(df_filtered['Start_Time'].dt.dayofweek, bins=7, kde=False, stat='density')
    # plt.subplots_adjust(left=0.2, bottom=0.2)
    # plt.savefig('E:\\Win K\\4th SEM\\PSC\\direct1\\src\\static\\images\\weekdata.jpg')

#Sunday density of accidents on hours
    # sundays_start_time = df_filtered['Start_Time'][df_filtered['Start_Time'].dt.dayofweek == 6]
    # sns.histplot(sundays_start_time.dt.hour, bins=24, kde=False, stat='density')
    # plt.subplots_adjust(left=0.2, bottom=0.2)
    # plt.savefig('E:\\Win K\\4th SEM\\PSC\\direct1\\src\\static\\images\\sundaydata.jpg')

#Monday Density of accidents on hours
    # monday_start_time = df_filtered['Start_Time'][df_filtered['Start_Time'].dt.dayofweek == 0]
    # sns.histplot(monday_start_time.dt.hour, bins=24, kde=False, stat='density')
    # plt.subplots_adjust(left=0.2, bottom=0.2)
    # plt.savefig('E:\\Win K\\4th SEM\\PSC\\direct1\\src\\static\\images\\mondaydata.jpg')


#Visualization and Positional Analysis with density of accidents
    my_list.append(df.Start_Lat) #[10]
    my_list.append(df.Start_Lng) #[11]


#Plot in Map
    # sample_df = df.sample(int(0.1 * len(df)))
    # sns.scatterplot(x=sample_df.Start_Lng, y=sample_df.Start_Lat, size=0.001)
    # plt.subplots_adjust(left=0.2, bottom=0.2)
    # plt.savefig('E:\\Win K\\4th SEM\\PSC\\direct1\\src\\static\\images\\accipos.jpg')


#Interactive map with density of accidents in USA
    zip(list(df.Start_Lat), list(df.Start_Lng))
    sample_df = df.sample(int(0.001 * len(df)))
    lat_lon_pairs = list(zip(list(sample_df.Start_Lat), list(sample_df.Start_Lng)))
    map = folium.Map()
    HeatMap(lat_lon_pairs).add_to(map)
    map_html = map.get_root().render()


#Temperature Analysis
    my_list.append(df['Temperature(F)']) #[12]

    df['Temperature(C)']=(df['Temperature(F)']-32)*(5/9)
    df['Temperature(C)'].hist(bins=range(-20,45),density=True)
    plt.xlabel('Temperature(C)')
    plt.ylabel('Density of accidents')
    # plt.savefig('E:\\Win K\\4th SEM\\PSC\\direct1\\src\\static\\images\\accivstemp.jpg')


#Weather Conditions during accidents
    my_list.append(df['Weather_Condition'].unique()) #[13]
    weather = df['Weather_Condition'].value_counts()
    percent = weather/weather.sum()*100
    percent = percent.apply(lambda x: x if x>=0.7 else None)
    percent['Others']=percent.isnull().sum()
    percent=percent.dropna()
    weather.plot.pie(autopct='%.1f%%')
    # plt.savefig('E:\\Win K\\4th SEM\\PSC\\direct1\\src\\static\\images\\weather.jpg')



    return my_list,map_html
    # print(df)

def main_page(request, *args, **kwargs):
    df,map_html=main()
    my_context={"dict":df, "map_html":map_html}
    return render(request, "main_page.html",my_context)
