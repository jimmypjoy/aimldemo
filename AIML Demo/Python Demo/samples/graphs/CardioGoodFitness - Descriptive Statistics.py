import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

mydata = pd.read_csv('CardioGoodFitness.csv')
print(mydata.head(10))
print(mydata.describe(include="all"))
print(mydata.info())
print(mydata.hist(figsize=(20, 30)))

import seaborn as sns

sns.boxplot(x="Gender", y="Age", data=mydata)
plt.show()

print(pd.crosstab(mydata['Product'], mydata['Gender']))
print(pd.crosstab(mydata['Product'], mydata['MaritalStatus']))

sns.countplot(x="Product", hue="Gender", data=mydata)
plt.show()

print(pd.pivot_table(mydata, index=['Product', 'Gender'], columns=['MaritalStatus'], aggfunc=len))

print(pd.pivot_table(mydata, 'Income', index=['Product', 'Gender'], columns=['MaritalStatus']))

print(pd.pivot_table(mydata, 'Miles', index=['Product', 'Gender'], columns=['MaritalStatus']))

sns.pairplot(mydata)
plt.show()

print(mydata['Age'].std())
print(mydata['Age'].mean())

sns.distplot(mydata['Age'])
plt.show()

mydata.hist(by='Gender', column='Age')

mydata.hist(by='Gender', column='Income')

mydata.hist(by='Gender', column='Miles')
mydata.hist(by='Product', column='Miles', figsize=(20, 30))

corr = mydata.corr()
corr

sns.heatmap(corr, annot=True)
plt.show()

# Load function from sklearn
from sklearn import linear_model

# Create linear regression object
regr = linear_model.LinearRegression()

y = mydata['Miles']
x = mydata[['Usage', 'Fitness']]

# Train the model using the training sets
regr.fit(x, y)

regr.coef_
regr.intercept_
