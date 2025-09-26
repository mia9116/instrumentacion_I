A = 0b1000

print(A/0b10000)

B = A | 0b0100

print("{0:>04b}".format(B))

B = A & 0b0000

print("{0:>04b}".format(B))


import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

T = 1000
x = np.arange(0,T)
y=  np.sin(4*np.pi*x/T)+np.cos(8*np.pi*x/T)+2

df = pd.DataFrame({'x':x, 'y':y})
df.plot('x', 'y')
plt.show()

df.to_csv("data1.csv")


# plt.plot(x,y)
# plt.show()