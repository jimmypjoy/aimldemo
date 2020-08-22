import numpy as np
import pandas as pd

# Read the Data
df = pd.read_csv('uberdrive.csv')

print(df.head(3))
print(df.tail(3))
print(df.shape)
print(df.size)
print(df.info())
print(df.dtypes)
print(df.describe())
print(df.describe(include='all'))
print(df.count())
# You can also find the columns with missing values through the snippet below
null_cols = df.columns[df.isnull().any()]  # get only the columns that have a null value.
null_cols = list(null_cols)
print(null_cols)
# Get the columns into a list and do use it to do some operations
# isnull() function checks the number of null values and sum() function sums up the count of these.
# Shows the column wise values of missing data
print(df.isnull().sum())

# Show the records with missing values for column= PURPOSE
print(df[df['PURPOSE*'].isnull()].head(10))
# you can as well do a head() function on this to just view the first n rows
print(df['PURPOSE*'].count())
print(df[df['END_DATE*'].isnull()])
# the above record has no entry apart from the miles and can be discarded
df.drop(1155, inplace=True)
# we set the inplace attribute to True so that the row is dropped and the dataframe is updated simultaneously.

print(df[df['END_DATE*'].isnull()], df.shape)
# note that the row is now dropped
# Note that while we dropped the row above, we will discuss in detail the techniques to handle the missing data in the upcomping weeks.

# Rename the columns to remove the * from the names
# Why ? we can use df.START_DATE same way as  df['START_DATE*']
col_names = ['START_DATE', 'END_DATE', 'CAT', 'START', 'STOP', 'MILES', 'PURPOSE']
df.columns = col_names

# Replace the * character from all the  columns .
# ( in case you have many columns and cant manually write the column names )
df.columns = df.columns.str.replace("*", "")
# You can also rename the specific column names
df.rename(columns={'CAT': 'CATEGORY'})
print(df.head())

# shows the top 5 entries where PURPOSE is null
print(df[df.PURPOSE.isnull()].head(5))

# Operation 2
# Here we have the rows that have atleast one null value. Note that since only PURPOSE column has the null value,
# We will get all the records where purpose is null
print(df[df.isnull().any(axis=1)].head(5))

# Operation 3
# inverting the selection ( not null ) ( works for booleans cases)
# using the ~, we invert the selection done in the above methods. 
# Here only the records where the purpose is not null will show up.
print(df[~df.PURPOSE.isnull()])

# you can also invert the operation 2 above
# #### Filtering out records based on conditions
# 1. Conditions within dataframe
print(df[df['MILES'] > 30].head())

# 2. SQL-like query
print(df.query('MILES > 30').head(5))

# ### Exploring Columns
print(df.MILES.max())
print(df[df.MILES == df.MILES.max()])  # Show the row that has the max miles
print(df.MILES.sort_values(ascending=False).head(10))  # Show the top 10 rides (in terms of distance driven)
print(df.sort_values(by='MILES', ascending=False).head(10))  # Shows the top 10 rows of MILES (decreasing value)

# Get the number of rows of dataframe.
print(len(df))

# #### Dropping rows  which have null values
# Get the initial data with dropping the NA values
df_dropped = df.dropna()
# Dont do the above step (df.dropna()) on the original dataframe, because you will lose good rows with values.
# To avoid losing good rows with values, make a copy and do operations on that.
print(df_dropped.shape)  # Get the shape of the dataframe after removing the null values

# The filtered dataset with no nulls ( in PURPOSE column )  contains 653 rows of non-null values

# names of unique start points
print(df['START'].unique())
print(len(df['START'].unique()))  # Count of unique start points using  len()

print(df['START'].nunique())  # or use can use the nunique function
# Get the names of stopping destinations, unique destinations
# Names of unique stopping points
print(df['STOP'].unique())
print(len(df['STOP'].unique()))  # count of unique stopping points

s_start = set(df['START'])  # names of unique start points
s_stop = set(df['STOP'])  # names of unique stop points

print(len(s_start))
print(len(s_stop))

print(s_stop & s_start)

print(df['START'].value_counts().head(10))

# Identify popular stop destinations - top 10
print(df['STOP'].value_counts().head(10))

# Are there cases where the start and the stop location are the same  ?
print(df[df['START'] == df['STOP']])

# Favorite starting point w.r.t. the total miles covered.
print(df.groupby('START')['MILES'].sum().sort_values(ascending=False).head(10))

# Find the top10 start stop pair that have the most miles covered between them ever.

# Let us drop the unknown locations
df2 = df[
    df['START'] != 'Unknown Location']  # Makes a new dataframe, which don't have "Unknown Location" as starting point
df2 = df2[df2[
              'STOP'] != 'Unknown Location']  # Further updates the df2 dataframe, by removing "Unknown Location" as stopping point

# Creating a dataframe with the top 10 most miles covered between a start stop pair

k3 = df2.groupby(['START', 'STOP'])['MILES'].sum().sort_values(ascending=False).head(10)
k3 = k3.reset_index()  # flatten the dataframe
k3['Start-Stop'] = k3['START'] + ' - ' + k3['STOP']
k3 = df2.groupby(['START', 'STOP'])['MILES'].sum().sort_values(ascending=False).head(10)
k3 = k3.reset_index()  # flatten the dataframe
k3['Start-Stop'] = k3['START'] + ' - ' + k3['STOP']
print(k3)

# just a peek into the visualisation module which you are going to learn in the upcoming weeek.
import matplotlib.pyplot as plt
import seaborn as sns

plt.figure(figsize=(16, 8))
chart1 = sns.barplot(data=k3, x='Start-Stop', y='MILES')
plt.show(chart1)

# The most popular start and stop pair - ( BY COUNT of travels! )
df2.groupby(['START', 'STOP'])['MILES'].size().sort_values(ascending=False).head(10)
# **The most popular start to destination pair is Morrisville-Cary**

print(df.head(3))

# We will be using the datetime module (  https://docs.python.org/3/library/datetime.html  )
# 
# Search for "strftime() and strptime() Format Codes" in the documentation page

# Create columns by converting the start and end date into a datatime format
# You can also over write the same column - but for the sake of understanding the difference in formats, we create new columns

from datetime import datetime  # Import datetime library

df['start_dt'] = df['START_DATE'].apply(lambda x: datetime.strptime(x, '%m/%d/%Y %H:%M'))
df['end_dt'] = df['END_DATE'].apply(lambda x: datetime.strptime(x, '%m/%d/%Y %H:%M'))

print(df.head())  # Print first 5 rows of data.

print(df.dtypes)  # See how the dtype is different

# Create more columns by using the inbuilt functionalities of datatime module

df['start_day'] = df['start_dt'].dt.day
df['start_hour'] = df['start_dt'].dt.hour
df['start_month'] = df['start_dt'].dt.month
df['d_of_wk'] = df['start_dt'].dt.dayofweek  # Days encoded as 0-6  ( monday =0, Tue =1 .... )

# You can convert the numeric encoding of weekdays into short form by manually writing the mapping
# days = {0:'Mon',1:'Tue',2:'Wed',3:'Thur',4:'Fri',5:'Sat',6:'Sun'}
# df['day_of_week'] = df['day_of_week'].apply(lambda x: days[x])

# or use the builtin functions

df['weekday'] = df['start_dt'].apply(lambda x: datetime.strftime(x, '%a'))  # ( or directly convert into the short form)

# Similarly you can use the calendar library to get the month abbreviation
# import calendar
# df['start_month_cal'] = df['start_month'].apply(lambda x: calendar.month_abbr[x])

# or 
# use the built in functions in datatime module
df['cal_month'] = df['start_dt'].apply(lambda x: datetime.strftime(x, '%b'))

print(df.head())

print(df.groupby(['start_month']).size())  # Group by the month

print(df.groupby('cal_month').sum()['MILES'].sort_values(ascending=False))

# Getting the average distance covered each month
print(df.groupby('cal_month').mean()['MILES'].sort_values(ascending=False))

# Write your inferences here based on the last 3 outputs
# Which day did he get most drives?
print(df.groupby(['weekday']).size())
# **When does he usually start the trip ?**

print(df.groupby('start_hour').size())  # The number of trips started for each hour.
# This looks like an interesting data
# 
# Does he have a prefered time of start ?

df['start_hour'] = df['start_dt'].dt.hour

df_hrs = df.groupby('start_hour').size()
df_hrs = df_hrs.reset_index()
df_hrs.columns = ['start_hour', 'count']
sns.barplot(data=df_hrs, x='start_hour', y='count')
# Looks like the driver mostly starts the trip around 9-10 and the peak hours seem to be between 12- 5 PM
# Duration of the trips

df['diff'] = (df['end_dt'] - df['start_dt'])

print(df.dtypes)
# This creates a timedelta datatype
# How long did the trips last

df['diff_hr'] = df['diff'].astype('timedelta64[h]')

print(df['diff'].describe())
# View in terms of minutes
df['diff_mins'] = df['diff'].astype('timedelta64[m]')

print(df['diff_mins'].describe())

# There seems to be somethin strange with the minumum time ( in minutes ) - it is 0
len(df[df['START_DATE'] == df['END_DATE']])

df[df['START_DATE'] == df['END_DATE']]
# There are some values where the start and end times are the same - remove them ?

print(len(df2))
# ## 3. Exploring existing features to create new ones - Speed
# - Open for all of you to explore and figure out what all can be understood and derived from this feature

# calculate trip speed for each trip
df['Duration_hours'] = df['diff_mins'] / 60
df['Speed'] = df['MILES'] / df['Duration_hours']
df['Speed'].describe()
# Remove the ones with unknown location
# Remove the ones that have the same start and end time (and redo the analysis)
df2 = df[df.start_dt != df.end_dt]

# we still see some really fast driving !!
df2.sort_values(by='diff_mins', ascending=True).head(5)
print(df['CAT'].value_counts())

# **Most trips are in the business category**
# Purpose
print(df['PURPOSE'].value_counts())
# **Most trips are for meetings**
print(df.groupby('PURPOSE').mean()['MILES'].sort_values(ascending=False))
