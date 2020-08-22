import pandas as pd

email_data = pd.read_csv('Random Email Dataset.csv')


# #### Display the Email ids
email_data['Email Address']


# #### FInd the number of gamail email Ids (ending with @gamail.com)

import re
x = email_data['Email Address']
print('||'.join(x))

#here the column Email Address has been converted to a string where each email id is searated by a pipe

#now let us use the join to find out the number of email ids with gamail
pattern1 = re.compile(r'[a-zA-Z0-9_]@gamail\.com\b') #using a space after each address in the pattern
matches = pattern1.finditer(' '.join(x)) #using a space after each address as in the pattern which matches with our string
counter = 0
for mat in matches:
    counter = counter+1
print('Number of gamail email ids:', counter)


# #### Find the number of yahooo email Ids (ending with @yahooo.com)
# We will follow the same approach.
pattern2 = re.compile(r'[a-zA-Z0-9_]@yahooo\.com\b') #using a space after each address in the pattern
matches = pattern2.finditer(' '.join(x)) #using a space after each address as in the pattern which matches with our string
counter = 0
for mat in matches:
    counter = counter+1
print('Number of yahooo email ids:', counter)


# #### Find the number of entries that are not email ids (consider the entries that do not have a @ and a .com/.in/.org in them)
pattern3 = re.compile(r'[a-zA-Z0-9_]+@[a-zA-Z0-9_]+\.com\b')
matches = pattern3.finditer(' '.join(x)) #using a space after each address as in the pattern which matches with our string
counter = 0
for mat in matches:
    counter = counter + 1
    #print(mat)
email_ids = counter

print('Number of email ids:', email_ids)

# let us find the total number of non-email data entries
total_entries = len(email_data['Email Address'])
print('Total Number of non email entries:',total_entries-email_ids)


# #### find the total entries that have the pattern 'asd' in them
pattern4 = re.compile(r'asd')
matches = pattern4.finditer(' '.join(x))
counter = 0
for mat in matches:
    counter = counter + 1
    #print(mat)

print('Number of such patterns:', counter)


# #### find the number of email Ids that start with k
pattern5 = re.compile(r'\b[k][a-zA-Z0-9_]*@[a-zA-Z0-9_]*\.[a-z]{2,4}\b')
matches = pattern5.finditer(' '.join(x))
counter = 0
for mat in matches:
    counter = counter + 1
    #print(mat)

print('Number of such email Ids:', counter)
