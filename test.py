import numpy as np
import sys

# Create a numpy integer
x = np.int64(1)

lst= np.fromstring(np.binary_repr(x,width=64), dtype='S1').astype(int)
lst=np.ones(lst.size)
# Get the size of the numpy integer in bytes
print(lst,lst.size)
print(1 << np.arange(lst.size,dtype=np.uint64)[::-1])
print(lst.dot(1 << np.arange(lst.size,dtype=np.uint64)[::-1]))
# print(np.zeros(10,dtype=int))