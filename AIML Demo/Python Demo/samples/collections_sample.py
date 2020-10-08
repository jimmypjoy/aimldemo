from collections import Counter

lst = [1,2,2,2,2,3,3,3,1,2,1,12,3,2,32,1,21,1,223,1]
print(Counter(lst))

print(Counter('aabsbsbsbhshhbbsbs'))

s = 'How many times does each word show up in this sentence word times each each word'
words = s.split()
print(Counter(words))

c = Counter(words)
print(c.most_common(2))