import pandas as pd
import numpy as np

flowers = pd.Series([2, 3, 5, 4], index=['lily', 'rose', 'daisy', 'lotus'])
print(flowers['daisy'])

myList1 = [9, 8, 7.0]
myseries1 = pd.Series(data=myList1)
print(myseries1)
# custom index
myList2 = [5, 4, 6]
mylabels1 = ['First', 'Second', 'Third']
myseries2 = pd.Series(data=myList2, index=mylabels1)
print(myseries2)
print(myseries2['Third'])

df1 = pd.concat([myseries1, myseries2], axis=1, sort=False)
print(df1)

# dataframe
df3 = pd.DataFrame(np.random.randint(0, 100, [5, 5]))
print(df3)
print(df3.iloc[4])
print(df3 > 50)
print(df3[df3 > 50])
df3[5] = np.random.randint(0, 100, [5, 1])
print(df3)
print(df3.drop(0, axis=1))

# functions
print(df3.nunique())
print(df3.mean())
print(df3.min())
print('df3[1]:')
print(df3[1])
df3.set_index()


def testfun(s):
    if (s < 50):
        ret = 0
    else:
        ret = s
    return ret


print(df3[1].apply(testfun))

# writing to .csv file
df3.to_csv('DF3')