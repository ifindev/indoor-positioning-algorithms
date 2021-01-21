"""
Author      : Muhammad Arifin
Institution : Universitas Gadjah Mada, Yogyakarta, Indonesia
Description	: Python code for calculating the path loss exponent (PLE) of
			  			path loss measurement data with simplified log-model. 
Date				: 20th April 2020

How this code works?
1. Sympy is used to do symbolic calculations. 
2. Numpy is used to do array operations.


Licensing		: This program is licensed under MIT License. 
				  		MIT License

Copyright (c) [2020] [Muhammad Arifin]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
import numpy as np 
import sympy as sym 


# Real Path Loss Data
# Measured on 20 April 2020
# Measured on the parking lot of Pogung Baru F29


#dist     = np.array([1.0, 1.5, 2.0, 2.5, 3.0,3.5, 4.0, 4.5, 5.0, 5.5])
#measured = np.array([-49, -53, -58, -60, -68, -60, -59, -60, -64, -68])
def finding_ple(distance, measured, frequency):

	c = 3e8

	# Finding log distance and K
	log_dist = np.log10(dist)

	k = -20*np.log10(4*np.pi * frequency/c) # Path loss at 1.0 meter

	# Symbolic path loss exponent (n)
	n = sym.Symbol('n') 

	# Calculating F(n)
	fn = (measured - k + 10*n*log_dist)**2
	fn_result = 0

	for res in fn:
		fn_result += res # Summing all the component

	# Calculating PLE (n) by differentiating F(n)
	# then assign dF(n) / dn = 0 for minimum error value
	diffn  = sym.diff(fn) 
	diff_result = 0

	for num in diffn:
		diff_result += num

	str_result = str(diff_result).replace('*n','').split('-') #list values
	ple_result = round(float(str_result[1])/float(str_result[0]), 2)

	return fn_result, str_result, ple_result


def finding_std_dev(dist, measured, ple, frequency):

	# Finding log distance and K
	log_dist = np.log10(dist)

	c = 3e8

	k = -20*np.log10(4*np.pi * frequency/c) # Path loss at 1.0 meter

	# Calculating average of F(n)
	fn_total = (measured - k + 10*ple*log_dist)**2
	avg_fn_total = 0

	for num in fn_total:
		avg_fn_total += num # Summing all the component

	variance = avg_fn_total / len(dist)

	std_dev = round(np.sqrt(variance),3)

	return std_dev


# Distance and measured rssi data
#dist = np.arange(0.5,6.0,0.5)
#meas = np.array([-39,-49,-53,-58,-60,-68,-60,-59, -60, -64, -68])

dist = np.array([10, 20, 50, 100, 300])
meas = np.array([-70, -75, -90, -110, -125])
f = 2e9

path_loss = finding_ple(dist, meas, f)
stdev = finding_std_dev(dist, meas, path_loss[2], f)

fn_res   = path_loss[0]
diff_res = path_loss[1]
ple_res  = path_loss[2]

# Print the F(n), diffn, and ple_result
print("F(n) = ",fn_res,"\n")
print("dF(n)/dn = ",diff_res,"\n")
print("PLE (n) = ",ple_res,"\n")
print("Stdev = ", stdev)






