import numpy
from scipy import stats

speed = [8,6,12,8,9]

print('std dev is {}'.format(numpy.std(speed)))
print('var is {}'.format(numpy.var(speed)))
print('mean is {}'.format(numpy.mean(speed)))
print('median is {}'.format(numpy.median(speed)))
print('mode is {}'.format(stats.mode(speed)))

print('percentile for 8 is {}'.format(numpy.percentile(speed,50)))
