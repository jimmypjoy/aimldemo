import re

text_to_search = '''
abcdefghijklmnopqurtuvwxyz
ABCDEFGHIJKLMNOPQRSTUVWXYZ
1234567890
123abc

Hello HelloHello

MetaCharacters (Need to be escaped):
. ^ $ * + ? { } [ ] \ | ( )

utexas.edu

321-555-4321
123.555.1234

daniel-mitchell@utexas.edu

Mr. Johnson
Mr Smith
Ms Davis
Mrs. Robinson
Mr. T
'''
# ## Searching literals
pattern = re.compile(r'abc')
matches = pattern.finditer(text_to_search)
for mat in matches:
    print(mat)

print(text_to_search[69:72])
print(text_to_search[1:4])

pattern = re.compile(r'cba')
matches = pattern.finditer(text_to_search)
for mat in matches:
    print(mat)

# ## Searching special characters
pattern = re.compile(r'\.')
matches = pattern.finditer(text_to_search)
for mat in matches:
    print(mat)

pattern = re.compile(r'\d')
matches = pattern.finditer(text_to_search)
for mat in matches:
    print(mat)

pattern = re.compile(r'\D')
matches = pattern.finditer(text_to_search)
for mat in matches:
    print(mat)

pattern = re.compile(r'\d\w')
matches = pattern.finditer(text_to_search)
for mat in matches:
    print(mat)

pattern = re.compile(r'\d\s')
matches = pattern.finditer(text_to_search)
for mat in matches:
    print(mat)

# ## Word boundary
# Hello HelloHello
pattern = re.compile(r'Hello')
matches = pattern.finditer(text_to_search)
for mat in matches:
    print(mat)

pattern = re.compile(r'Hello\b')
matches = pattern.finditer(text_to_search)
for mat in matches:
    print(mat)

pattern = re.compile(r'\bHello\b')
matches = pattern.finditer(text_to_search)
for mat in matches:
    print(mat)

pattern = re.compile(r'\BHello\b')
matches = pattern.finditer(text_to_search)
for mat in matches:
    print(mat)

pattern = re.compile(r'\b\d')
matches = pattern.finditer(text_to_search)
for mat in matches:
    print(mat)

pattern = re.compile(r'^\s')
matches = pattern.finditer(text_to_search)
for mat in matches:
    print(mat)

# ## Character sets
pattern = re.compile(r'[123]\w')
matches = pattern.finditer(text_to_search)
for mat in matches:
    print(mat)

pattern = re.compile(r'[a-z][a-z]')
matches = pattern.finditer(text_to_search)
for mat in matches:
    print(mat)

pattern = re.compile(r'[a-zA-Z0-9][a-zA-z-]')
matches = pattern.finditer(text_to_search)
for mat in matches:
    print(mat)

pattern = re.compile(r'[a-zA-Z][^a-zA-z]')
matches = pattern.finditer(text_to_search)
for mat in matches:
    print(mat)

# ## Character groups
pattern = re.compile(r'(abc|edu|texas)\b')
matches = pattern.finditer(text_to_search)
for mat in matches:
    print(mat)

pattern = re.compile(r'([A-Z]|llo)[a-zA-z]')
matches = pattern.finditer(text_to_search)
for mat in matches:
    print(mat)

# ## Quantifiers
pattern = re.compile(r'Mr\.?\s[A-Z]')
matches = pattern.finditer(text_to_search)
for mat in matches:
    print(mat)

pattern = re.compile(r'Mr\.?\s[A-Z][a-z]*')
matches = pattern.finditer(text_to_search)
for mat in matches:
    print(mat)

pattern = re.compile(r'M(s|rs)\.?\s[A-Z][a-z]*')
matches = pattern.finditer(text_to_search)
for mat in matches:
    print(mat)

pattern = re.compile(r'\d{3}[.-]\d{3}[.-]\d{4}')
matches = pattern.finditer(text_to_search)
for mat in matches:
    print(mat)

pattern = re.compile(r'[a-zA-Z0-9_]+\.[a-z]{3}')
matches = pattern.finditer(text_to_search)
for mat in matches:
    print(mat)

pattern = re.compile(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+')
matches = pattern.finditer(text_to_search)
for mat in matches:
    print(mat)

# ## Accessing information in the Match object
pattern = re.compile(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]{2,4}')
matches = pattern.finditer(text_to_search)
for mat in matches:
    print(mat.span(0))
    print(mat.group(0))
    print(text_to_search[mat.span(0)[0]:mat.span(0)[1]])

urls = r'''
https://www.google.com
http://yahoo.com
https://www.whitehouse.gov
https://craigslist.org
'''

pattern = re.compile(r'https?://(www\.)?\w+\.\w+')
matches = pattern.finditer(urls)
for mat in matches:
    print(mat)

pattern = re.compile(r'https?://(www\.)?(\w+)(\.\w+)')
matches = pattern.finditer(urls)
for mat in matches:
    print(mat.group(2) + mat.group(3))

pattern = re.compile(r'https?://(www\.)?(\w+)(\.\w+)')
matches = pattern.finditer(urls)
for mat in matches:
    print(mat.group(0))
    print(urls[mat.span(2)[0]:mat.span(2)[1]] + urls[mat.span(3)[0]:mat.span(3)[1]])

