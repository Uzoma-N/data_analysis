"""
Smartwatch Data Analysis using Python
Smartwatches are preferred by people who like to take care of their fitness.
Analyzing the data collected on your fitness is one of the use cases of Data Science in healthcare.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go

data = pd.read_csv("datasets/dailyActivity_merged.csv")
print(data.head())

# taking a look at the data
print(data.isnull().sum())

# Changing datatype of ActivityDate
data["ActivityDate"] = pd.to_datetime(data["ActivityDate"], format="%m/%d/%Y")

# combine activity minutes from different columns into one
data["TotalMinutes"] = data["VeryActiveMinutes"] + data["FairlyActiveMinutes"] + data["LightlyActiveMinutes"] \
                       + data["SedentaryMinutes"]
print(data["TotalMinutes"].sample(5))

# to get the descriptive statistics of the dataset
print(data.describe())

# to analyze the smartwatch data, let's take a lok at correlations
# firstly, calories burned vs total steps
figure = px.scatter(data_frame=data, x="Calories", y="TotalSteps", size="VeryActiveMinutes",
                    title="Relationship between Calories & Total Steps")
figure.show()

# looking at the average total number of active minutes in a day
label = ["Very Active Minutes", "Fairly Active Minutes", "Lightly Active Minutes", "Inactive Minutes"]
counts = data[["VeryActiveMinutes", "FairlyActiveMinutes", "LightlyActiveMinutes", "SedentaryMinutes"]].mean()
colors = ['gold','lightgreen', "pink", "blue"]

fig = go.Figure(data=[go.Pie(labels=label, values=counts)])
fig.update_layout(title_text='Total Active Minutes')
fig.update_traces(hoverinfo='label+percent', textinfo='value', textfont_size=30,
                  marker=dict(colors=colors, line=dict(color='black', width=3)))
fig.show()

# find the weekdays of the records and add a new column to this dataset as “Day”
data["Day"] = data["ActivityDate"].dt.day_name()
print(data["Day"].head())

# looking at the very active, fairly active, and lightly active minutes on each day of the week:
fig = go.Figure()
fig.add_trace(go.Bar(
    x=data["Day"],
    y=data["VeryActiveMinutes"],
    name='Very Active',
    marker_color='purple'
))
fig.add_trace(go.Bar(
    x=data["Day"],
    y=data["FairlyActiveMinutes"],
    name='Fairly Active',
    marker_color='green'
))
fig.add_trace(go.Bar(
    x=data["Day"],
    y=data["LightlyActiveMinutes"],
    name='Lightly Active',
    marker_color='pink'
))
fig.update_layout(barmode='group', xaxis_tickangle=-45)
fig.show()

# looking at the number of inactive minutes on each day of the week
day = data["Day"].value_counts()
label = day.index
counts = data["SedentaryMinutes"]
colors = ['gold','lightgreen', "pink", "blue", "skyblue", "cyan", "orange"]

fig = go.Figure(data=[go.Pie(labels=label, values=counts)])
fig.update_layout(title_text='Inactive Minutes Daily')
fig.update_traces(hoverinfo='label+percent', textinfo='value', textfont_size=30,
                  marker=dict(colors=colors, line=dict(color='black', width=3)))
fig.show()

# look at the number of calories burned on each day of the week
calories = data["Day"].value_counts()
label = calories.index
counts = data["Calories"]
colors = ['gold','lightgreen', "pink", "blue", "skyblue", "cyan", "orange"]

fig = go.Figure(data=[go.Pie(labels=label, values=counts)])
fig.update_layout(title_text='Calories Burned Daily')
fig.update_traces(hoverinfo='label+percent', textinfo='value', textfont_size=30,
                  marker=dict(colors=colors, line=dict(color='black', width=3)))
fig.show()


