import numpy as np
import sys

# Create a numpy integer
x = np.int64(1)

lst= np.fromstring(np.binary_repr(x,width=64), dtype='S1').astype(int)
# Get the size of the numpy integer in bytes
print(lst)
print(lst.dot(1 << np.arange(lst.size)[::-1]))
print(np.zeros(10,dtype=int))