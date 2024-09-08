
import numpy as np
import matplotlib.pyplot as plt

x = np.arange(0, 13, 0.001)
y = x*0.2 + np.sin(x*3) * (np.sin(x*60))
plt.plot(x, y)
plt.show()