"""
Author			: Muhammad Arifin
Institution		: Department of Nuclear Engineering and Engineering Physics, Universitas Gadjah Mada
Initial Release	: 29th April, 2020
License			: MIT License

Description		: This program is a direct implementation of mathematical equations
				  used to calculate path loss exponent information from path loss 
				  measurement data. The implementation is based on theoritical 
				  explanation on Andreas Goldsmith's Wireless Communications book
				  chapter 2 on Path Loss and Shadowing. 

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
import matplotlib.pyplot as plt 


class Pathloss:
	def __init__(self, distance, measured, frequency):
		"""
		Class for creating a path loss object.

		Distance is an array of distances from Tx to Rx.
		Measured is the measured rssi values 
		corresponding to the given distance.
		"""

		# distance and rssi values
		self.dist = distance
		self.meas = measured

		# Finding total Number of data
		self.num_data = len(self.dist)

		# Finding measured rssi at d0
		self.freq = frequency
		self.light_speed = 3e8
		self.wavelength  = self.light_speed / self.freq
		self.d0 = 1.0
		#self.k = -20*np.log10(4 * np.pi * self.d0 / self.wavelength)
		self.k = self.meas[1]

		# Finding log distance
		self.log_dist = np.log10(self.dist)

		# symbolic path loss exponent
		self.n = sym.Symbol('n')


	def finding_ple(self):
		"""
		Pathloss class method to calculate path loss exponent
		given distances and measured rssi data.

		Calculation is based on Andreas Goldsmith Wireless
		Communications book p.40 of examples 2.3

		"""
		# Calculating F(n)
		self.fn = (self.meas - self.k + 10*self.n*self.log_dist)**2
		self.fn_result = 0

		for res in self.fn:
			self.fn_result += res # Summing all the component

		# Calculating PLE (n) by differentiating F(n)
		# then assign dF(n) / dn = 0 for minimum error value
		self.diffn  = sym.diff(self.fn) 
		self.diff_result = 0

		for num in self.diffn:
			self.diff_result += num

		self.str_result = str(self.diff_result).replace('*n','').split('-') #list values
		self.ple_result = round(float(self.str_result[1])/float(self.str_result[0]), 2)	

		return self.ple_result

	def finding_stdev(self):
		"""
		Pathloss class method to calculate standar deviation
		from given distances and rssi data. 

		Calculation is based on Andreas Goldsmith Wireless
		Communications book p.46 of examples 2.4
		"""
		# finding variance
		self.fn_total = (self.meas - self.k + 10*self.ple_result*self.log_dist)**2
		self.variance = 0

		for var in self.fn_total:
			self.variance += var # summing all the components

		self.std_dev = round(np.sqrt(self.variance / self.num_data) ,2)

		return self.std_dev

	def path_loss_model_simplified(self):
		"""
		Pathloss class method to calculate the simplified path loss model.
		"""

		self.path_loss_simplified = self.k - 10*self.ple_result*np.log10(self.dist)
		#self.path_loss_simplified = self.k - 10*3.71*np.log10(self.dist)
		return self.path_loss_simplified


	def path_loss_model_shadowing(self):
		"""
		Pathloss class method to calculate the path loss model with shadowing.
		Shadowing is modeled using gaussian random noise
		"""

		#Gaussian random noise with mean = 0 and sigma = std_dev
		self.mean = 0
		self.gaussian_noise = np.random.normal(self.mean, self.std_dev, self.num_data)
		#self.gaussian_noise = np.random.normal(self.mean, 3.65, self.num_data)

		# Path loss model with shadowing modeled as gaussian random noise
		self.path_loss_shadowing = self.path_loss_simplified + self.gaussian_noise

		return self.path_loss_shadowing


def plotGraph(fx, x, legend):
	#plt.figure("Path Loss Graph")
	plt.plot(x, fx, "o-", label = str(legend))
	plt.title("Path Loss")
	plt.xlabel("d (m)")
	plt.ylabel("RSSI (dBm)")
	plt.ylim([-75, -35])
	plt.xlim([0, max(x)])
	plt.xticks(np.arange(0.0,5.0,0.5))
	plt.yticks(np.arange(-75,-30,5))
	plt.legend()
	plt.grid(color='lightgray', zorder = 10)
	plt.show()

def main():
	# Distance and measured rssi data
	#dist = np.arange(0.5,4.5,0.5)
	#meas = np.array([-41,-54,-55,-58,-61,-59,-62,-67])

	#dist = np.array([0.5, 0.7, 0.9, 1.0, 1.2, 1.5, 2.0, 2.5, 3.0, 3.2, 3.5, 3.7, 4.0, 4.2, 4.5, 4.7, 5.0, 5.5])
	#meas = np.array([-39, -42, -51, -49, -50, -53, -58, -60, -68, -60, -60, -56, -59, -62, -60, -62, -64, -68])
	f 	 = 2.4e9

	pathloss = Pathloss(dist, meas, f)
	plexp = pathloss.finding_ple()
	stdev = pathloss.finding_stdev()
	plmodel_simplified = pathloss.path_loss_model_simplified()
	plmodel_shadowing  = pathloss.path_loss_model_shadowing()

	print("Path Loss Exponent: ", plexp)
	print("Standard Deviation: ", stdev)
	print("Simplified Path Loss Model: ", plmodel_simplified)
	print("Path Loss Model with Shadowing: ", plmodel_shadowing)

	plotGraph(meas, dist, "Measured")
	plotGraph(plmodel_simplified, dist, "Simplified")
	plotGraph(plmodel_shadowing, dist, "Shadowing")

if __name__ == '__main__':
	try:
		main()
	except ValueError:
		print("ValueError: Number of distance and measured elements must be the same!")
