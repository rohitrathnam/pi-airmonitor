import pickle
import numpy as np
#import pandas as pd
#import matplotlib.pyplot as plt
from statistics import mean
import time

rf = pickle.load(open('xg.pkl','rb'))

a = np.zeros((1,2))
a[0][0]=71
a[0][1]=23
t=time.time()
rf.predict(a)
print(time.time()-t)

'''xg
data = pd.read_csv("data.csv")
labels = ['rh', 'temp']

o = rf.predict(data[labels])

plt.plot(o)
plt.plot(data['co2'])
plt.show()

smoothed = np.zeros((14000,))
buf = [0]*5

k=0
buf = o[0:5]
for i in range(5,14000):
	buf[k] = o[i]
	smoothed[i] = mean(buf)
	if k==4:
		k=0
	else:
		k=k+1

plt.plot(smoothed)
plt.plot(data['co2'])
plt.show()
'''
