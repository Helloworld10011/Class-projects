#import tensorflow as tf
import numpy as np

#x= tf.one_hot([1, 2, 4, -1, -1, -1, -1, 1], 10)
#print(x.numpy())

x= np.array([1, 3, 3, 3])

print(np.argmax(x))