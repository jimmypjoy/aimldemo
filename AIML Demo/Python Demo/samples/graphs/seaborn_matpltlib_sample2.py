import warnings
warnings.filterwarnings('ignore')   # to avoid warnings

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(style="darkgrid")

tips = sns.load_dataset("tips")

# Importing dataset from seaborn library, seaborn library consist of some inbuilts datasets.
print(tips.head())
print(tips.shape)
print(tips.info())
print(tips.describe().transpose())
print(tips['sex'].nunique())
print(tips['sex'].unique())
print(tips[['sex', 'tip']].groupby('sex').mean())
#who paid max tip
print(tips[tips['tip'] == tips['tip'].max()])

#plot all attributes
sns.pairplot(tips[['total_bill', 'tip', 'sex', 'smoker', 'day', 'time','size']])

sns.distplot(tips['total_bill'],color='hotpink')
plt.show()

sns.distplot(tips['tip'],color='lime')
plt.show()

sns.jointplot(tips['total_bill'], tips['tip'],color='green')
plt.show()

sns.jointplot(tips['total_bill'], tips['tip'], kind = "hex",color='red')
plt.show()

sns.pairplot(tips[['total_bill','tip']])
plt.show()

sns.lmplot(x = "total_bill",y = "tip", data = tips)
plt.show()

sns.stripplot(tips['sex'], tips['tip'])
plt.show()


sns.lmplot(x='total_bill',y='tip',data=tips,fit_reg=False,hue='sex')
plt.show()

sns.countplot(tips['day'], hue = tips['sex'])
plt.show()


sns.countplot(tips['smoker'])
plt.show()
sns.lmplot(x='total_bill',y='tip',data=tips,fit_reg=False,hue='sex',col='smoker',palette='rocket')
plt.show()
