import numpy as np 
import matplotlib.pyplot as plt

d = np.linspace(1,10,100)
pt = 1
Gl = 1
c = 3*(10**8)

f1 = 300 #MHz
f2 = 600*(10**6) #MHz
f3 = 900*(10**6) #GHz

lm1 = c/f1
lm2 = c/f2
lm3 = c/f3

pr1 = pt * ((np.sqrt(Gl)*lm1) / (4*np.pi*d))**2
pr2 = pt * ((np.sqrt(Gl)*lm2) / (4*np.pi*d))**2
pr3 = pt * ((np.sqrt(Gl)*lm3) / (4*np.pi*d))**2

#pr1 = np.log10(pt) + 10*np.log10(Gl) + 20*np.log10(lm1) - 20*np.log10(4*np.pi) - 20*np.log10(d)
#pr2 = np.log10(pt) + 10*np.log10(Gl) + 20*np.log10(lm2) - 20*np.log10(4*np.pi) - 20*np.log10(d)

plt.title("Received Power vs Frequency")
plt.plot(d, pr1*(10**3),linestyle='-.', color='black',label="$f$ = 300 MHz")
plt.plot(d, pr2*(10**3),linestyle='-', color='black',label="$f$ = 600 MHz")
plt.plot(d, pr3*(10**3),linestyle='--', color='black',label="$f$ = 900 MHz")
plt.xlim([1,10])
plt.ylim([0,6])
plt.xlabel("d [m]")
plt.ylabel("$P_{r}$ [mW]")
plt.legend()
plt.grid()
plt.show()
