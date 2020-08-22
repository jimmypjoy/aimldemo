import numpy as np
from numpy import matrix

nparray = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
print(nparray)
print(np.min(nparray))
print(np.max(nparray))

print(np.arange(1, 10, 3))

print(np.pi)
print(np.sqrt(36))
print(np.log(np.exp(5)))

# equi space points
vec1 = np.linspace(0, 5, 10)
print(vec1)
vec1_reshaped = vec1.reshape(5, 2)
print(vec1_reshaped)

# Matrix of 0s
print(np.zeros([5, 3]))
print(np.zeros([5]))
print(np.ones([5, 3]))

# print identical matrix. only diagonal elments 1 and others 0
print(np.eye(5))

# adding array elements together
array1 = np.arange(1, 6)
array2 = np.arange(6, 11)
print(array1 + array2)
print(array1 * array2)
print(1 / array1)
print(np.square(array1))

# unique elements of an array
array3 = np.array(['blue', 'red', 'orange', 'blue', 'red'])
print(np.unique(array3))

# random numbers
print(np.random.rand(5, 5))
print(np.random.randn(5, 5))

# Accessing numpy vectors
random_vec = np.arange(0, 19)
print(random_vec)
print(random_vec[4:7])
print(random_vec[np.arange(0, 15, 10)])
random_vec[3:5] = -1
print(random_vec[3])

# matrix
matrix = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
print(matrix[1:, 1:])
print(matrix[1][1])
print(matrix > 3)
print(matrix[matrix > 3])
matrix[matrix < 3] = 0
print(matrix)

# Save an array to file
np.save('np_array_file1', matrix)
print(np.load('np_array_file1.npy'))
#save array as text file
np.savetxt('np_array_filetxt1.txt', matrix,delimiter=',')
print(np.loadtxt('np_array_filetxt1.txt',delimiter=','))
