import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# reading the Data.csv, item.csv and user.csv into data frames
data = pd.read_csv('Data.csv')
#item = pd.read_csv('item.csv', index_col='movie title')
item = pd.read_csv('item.csv')
user = pd.read_csv('user.csv')

# #### 3. Apply info, shape, describe, and find the number of missing values in the data - 5 marks
#  - Note that you will need to do it for all the three datasets seperately

# In[ ]:


print('#Info of data:')
print(data.info())
print('')
print('#Shape of data:')
print(data.shape)
print('')
print('#Describe of data:')
print(data.describe())
print('')
print('#Number of misisng values of each columns of data:')
print(data.isnull().sum())

# In[ ]:


print('#Info of item:')
print(item.info())
print('')
print('#Shape of item:')
print(item.shape)
print('')
print('#Describe of item:')
print(item.describe())
print('')
print('#Number of misisng values of each columns of item:')
print(item.isnull().sum())

# In[ ]:


print('#Info of user:')
print(user.info())
print('')
print('#Shape of user:')
print(user.shape)
print('')
print('#Describe of user:')
print(user.describe())
print('')
print('#Number of misisng values of each columns of user:')
print(user.isnull().sum())

# #### 4. Find the number of movies per genre using the item data - 2.5 marks

# In[ ]:


# use sum on the default axis
# print(item.iloc[:,3: ].head())
# item.drop(['movie id','movie title','release date'], axis=1).sum(axis = 0)
print(item.iloc[:, 3:].sum(axis=0))

# #### 5. Find the movies that have more than one genre - 5 marks

# In[ ]:


# hint: use sum on the axis = 1
# item.set_index(keys='movie title')
# item.set_index('movie title')
item_temp = item.copy()
item_temp = item_temp.set_index('movie title')
item_temp=item_temp.drop(['movie id', 'release date'], axis=1).sum(axis=1)
item_temp = item_temp[item_temp[0:] > 1]



# #### 6. Drop the movie where the genre is unknown - 2.5 marks

# In[ ]:


item_unknown_genre = item[item['unknown'] == 1]
print("Movies with 'unknown' genre:")
print(item_unknown_genre)

# ### 7. Univariate plots of columns: 'rating', 'Age', 'release year', 'Gender' and 'Occupation' - 10 marks

# In[ ]:


# HINT: use distplot for age and countplot for gender,ratings,occupation, release year.
# HINT: Please refer to the below snippet to understand how to get to release year from release date. You can use str.split()
# as depicted below.


# In[ ]:


a = 'My*cat*is*brown'
print(a.split('*')[3])

# similarly, the release year needs to be taken out from release date

# also you can simply slice existing string to get the desired data, if we want to take out the colour of the cat

print(a[10:])
print(a[-5:])

# In[ ]:


# combine 3 data frames
sns.distplot(user['age']);

# In[ ]:


sns.countplot(user['gender'], hue=user['gender']);

# In[ ]:


sns.countplot(user['occupation']);

# In[ ]:


# df = item['release date'].apply(lambda x: x.split('-')[2])
#sns.countplot(item['release date'].apply(lambda x: x.split('-')[2]))
#df = item['release date'].apply(lambda x: x.split('-')[2])
item['release date'] = pd.DatetimeIndex(item['release date']).year
item.loc[(item['release date'] > 2021),'release date']=item['release date']-100
plt.figure(figsize=(30,20))
sns.countplot(item['release date']);

# ### 8. Visualize how popularity of genres has changed over the years - 10 marks
# 
# Note that you need to use the number of releases in a year as a parameter of popularity of a genre

# Hint 
#
# 1: you need to reach to a data frame where the release year is the index and the genre is the column names (one cell shows the number of release in a year in one genre) or vice versa.
# Once that is achieved, you can either use multiple bivariate plots or can use the heatmap to visualise all the changes over the years in one go. 
# 
# Hint 2: Use groupby on the relevant column and use sum() on the same to find out the nuumber of releases in a year/genre.  

# In[ ]:


item_temp = item.copy()
#item_temp['release date'] = item_temp['release date'].apply(lambda x: x.split('-')[2])
item_temp = item_temp.set_index('release date')
item_temp = item_temp.drop(['movie id'], axis=1)
item_new = item_temp.groupby('release date').sum()
item_new.head()
sns.heatmap(item_new, annot=True, cmap='plasma', vmin=-1, vmax=1)
sns.jointplot(data=item_new, x=item_new.index.values.tolist(), y='Action')
# sns.jointplot(item_new['Action']);


# ### 9. Find the top 25 movies according to average ratings such that each movie has number of ratings more than 100 - 10 marks
# 
# Hint : 
# 
# 1. First find the movies that have more than 100 ratings(use merge, groupby and count). Extract the movie id in a list.
# 2. Find the average rating of all the movies and sort them in the descending order. You will have to use the .merge() function to reach to a data set through which you can get the ids and the average rating.
# 3. Use isin(list obtained from 1) to filter out the movies which have more than 100 ratings.
# 
# Note: This question will need you to research about groupby and apply your findings. You can find more on groupby on https://realpython.com/pandas-groupby/.

# In[ ]:
item_temp = item.copy()
item_new = item_temp.set_index('movie id')
data_item = pd.merge(data, item_new, how='right', on='movie id')
movie_review_data = pd.merge(data_item, user, how='right', on='user id')
movie_review_data_new = movie_review_data[movie_review_data.groupby('movie id')['movie id'].transform('count').ge(100)]
movie_review_data_new_mean = movie_review_data_new[['movie title', 'rating']].groupby('movie title').mean()
movie_review_data_new_mean_sorted = movie_review_data_new_mean.sort_values('rating', ascending=False)
print(movie_review_data_new_mean_sorted.head(25))

# ### 10. See gender distribution across different genres check for the validity of the below statements - 10 marks
# 
# * Men watch more drama than women
# * Women watch more Sci-Fi than men
# * Men watch more Romance than women
# 

# 1. There is no need to conduct statistical tests around this. Just compare the percentages and comment on the validity of the above statements.
# 
# 2. you might want ot use the .sum(), .div() function here.
# 3. Use number of ratings to validate the numbers. For example, if out of 4000 ratings received by women, 3000 are for drama, we will assume that 75% of the women watch drama.

# #### Conclusion:
# 
# 

# In[ ]:


# Verify Men watch more drama than women
total_men = movie_review_data[movie_review_data['gender'] == 'M'].shape[0]
total_women = movie_review_data[movie_review_data['gender'] == 'F'].shape[0]
no_of_men_watching_drama = \
movie_review_data[(movie_review_data['gender'] == 'M') & (movie_review_data['Drama'] == 1)].shape[0]
no_of_women_watching_drama = \
movie_review_data[(movie_review_data['gender'] == 'F') & (movie_review_data['Drama'] == 1)].shape[0]
percent_of_men_watching_drama = no_of_men_watching_drama * 100 / total_men
percent_of_women_watching_drama = no_of_women_watching_drama * 100 / total_women
print('Men watch more drama than women: {}'.format((percent_of_men_watching_drama > percent_of_women_watching_drama)))
print('Percent of Men watching Drame: {} \nPercent of Women watching Drame: {} '.format(percent_of_men_watching_drama,
                                                                                        percent_of_women_watching_drama))

# In[ ]:


# Verify Women watch more Sci-Fi than men
no_of_men_watching_scifi = \
movie_review_data[(movie_review_data['gender'] == 'M') & (movie_review_data['Sci-Fi'] == 1)].shape[0]
no_of_women_watching_scifi = \
movie_review_data[(movie_review_data['gender'] == 'F') & (movie_review_data['Sci-Fi'] == 1)].shape[0]
percent_of_men_watching_scifi = no_of_men_watching_scifi * 100 / total_men
percent_of_women_watching_scifi = no_of_women_watching_scifi * 100 / total_women
print('Women watch more Sci-Fi than Men: {}'.format((percent_of_men_watching_scifi < percent_of_women_watching_scifi)))
print('Percent of Men watching Sci-Fi: {} \nPercent of Women watching Sci-Fi: {} '.format(percent_of_men_watching_scifi,
                                                                                          percent_of_women_watching_scifi))

# In[ ]:


# Verify Men watch more Romance than women
no_of_men_watching_romance = \
movie_review_data[(movie_review_data['gender'] == 'M') & (movie_review_data['Romance'] == 1)].shape[0]
no_of_women_watching_romance = \
movie_review_data[(movie_review_data['gender'] == 'F') & (movie_review_data['Romance'] == 1)].shape[0]
percent_of_men_watching_romance = no_of_men_watching_romance * 100 / total_men
percent_of_women_watching_romance = no_of_women_watching_romance * 100 / total_women
print('Men watch more Roamnce than women: {}'.format(
    (percent_of_men_watching_romance > percent_of_women_watching_romance)))
print('Percent of Men watching Roamnce: {} \nPercent of Women watching Roamnce: {} '.format(
    percent_of_men_watching_romance, percent_of_women_watching_romance))

# In[ ]:
