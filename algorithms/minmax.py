"""
Author		: Muhammad Arifin
Institution	: Department of Nuclear Engineering and Engineering Physics, Universitas Gadjah Mada
Initial Release	: 29th April, 2020
License		: MIT License
Description	: This program is a direct implementation of mathematical equations used to calculate 
		  min-max algorithm for indoor positioning using Received Signal Strength Indicator (RSSI)
		  data from four Wi-Fi routers. The mathematics are derived in my thesis and in other
		  journal papers on internet.
				  

Licensing	: This program is licensed under MIT License. 

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
import matplotlib.pyplot as plt
import pandas as pd 
import os



def main():
	# path = 'D:/Skripsweetku/Raw Data/Pengukuran Variasi Jarak Ulangan/'
	path = 'D:/Skripsweetku/Raw Data/Pengukuran Variasi Jarak dan Manusia/'
	cases = os.listdir(path)
	# case = '4D4.csv' # for testing purpose
	for case in cases:
		# read data
		df = pd.read_csv(path+case)

		# drop time column
		df = df.drop(columns=["Time"])

		# drop NaN values
		df = df.dropna()

		# take only data from column 1-2
		df = df.iloc[:,0:3]

		# Rename columns to AP1, AP2, and AP3
		df.columns = ["AP1", "AP2", "AP3"]

		#~~~~~~~~~~~~~~~~ Distance calculation from rssi using ple data ~~~~~~~~~~~~~~~#

		# Add path loss exponent and rssi at d0 parameters
		# Create a lambda function to convert RSSI data into distance
		dist = lambda k, n, rssi: 10**((k - rssi) / (10*n))

		# path loss parameters
		rssi_d0 = -49
		ple = 2.255

		# Add distance columns in df 
		for i in range(1,4):
			df["dist%d"%i] = dist(rssi_d0, ple, df["AP%d"%i])


		# Determining AP coordinate from case 
		# 1Dx means d = 1, 2Dx means d = 2, cont..

		if case[0] == "1":
			d = 1
		elif case[0] == "2":
			d = 2
		elif case[0] == "3":
			d = 3
		else:
			d = 4

		# Setting APs coordinates
		# AP1
		x1 = 0
		y1 = 0

		# AP2
		x2 = 0
		y2 = 1 * d

		# AP3
		x3 = 1 * d
		y3 = 1 * d

		xcoords = [x1, x2, x3]
		ycoords = [y1, y2, y3]

		# Target coordinates
		case = case.upper()
		if case[1:3] == "D1":
			xreal = (1/2) * d
			yreal = 1*d
		elif case[1:3] == "D2":
			xreal = (1/4) * d
			yreal = (3/4) * d
		elif case[1:3] == "D3":
			xreal = (1/2) * d
			yreal = (1/2) * d
		elif case[1:3] == "D4":
			xreal = (1/2) * d
			yreal = 0 * d

		#~~~~~~~~~~~~~~~~~~~~~ Min and Max coordinates calculations ~~~~~~~~~~~~~~~~~~~~#
		# Add xmax, xmin, ymin, and ymax of all APs into df
		for i in range(1,4):
			df["x%d_max"%i] = xcoords[i-1] + df["dist%d"%i]
			df["x%d_min"%i] = xcoords[i-1] - df["dist%d"%i]
			df["y%d_max"%i] = ycoords[i-1] + df["dist%d"%i]
			df["y%d_min"%i] = ycoords[i-1] - df["dist%d"%i]

		#print(df.head())

		#~~~~~~~~~~~~~~~~~~~~~ Min and Max coordinates calculations ~~~~~~~~~~~~~~~~~~~~#

		# Concantenate all the max and min coordinates
		xmax = np.array(pd.concat([df["x1_max"], df["x2_max"], df["x3_max"]]).sort_values(ascending=True))
		xmin = np.array(pd.concat([df["x1_min"], df["x2_min"], df["x3_min"]]).sort_values(ascending=False))
		ymax = np.array(pd.concat([df["y1_max"], df["y2_max"], df["y3_max"]]).sort_values(ascending=True))
		ymin = np.array(pd.concat([df["y1_min"], df["y2_min"], df["y3_min"]]).sort_values(ascending=False))

		# assign 100 values for each minmax and maxmin values
		# minmax = minimum value from a set of maximum values
		# maxmin = maximum value from a set of minimum values 

		xminmax = xmax[:100]
		xmaxmin = xmin[:100]
		yminmax = ymax[:100]
		ymaxmin = ymin[:100]

		#~~~~~~~~~~~~~~~~~~~~~~~~~  Min-Max Target calculations ~~~~~~~~~~~~~~~~~~~~~~~#
		x_pred = (xminmax + xmaxmin)/2
		y_pred = (yminmax + ymaxmin)/2

		#~~~~~~~~~~~~~~~~~~~~~~~~~  Sqrt Error and Mean Sqrt Error ~~~~~~~~~~~~~~~~~~~~#
		SQEmm = np.sqrt((x_pred - xreal)**2 + (y_pred - yreal)**2)
		MSEmm = np.mean(SQEmm)

		print("Localization using ESP32 %s" %case[0:3])
		print("MSE Min-Max %s:" %case[0:3],round(MSEmm,2),"\n")
		#~~~~~~~~~~~~~~~~~~~~~~~~~~~  Plot Graphical Results ~~~~~~~~~~~~~~~~~~~~~~~~~~#

		if case[0] == "1":
			limits = [-0.5, 1.5]
			ticks  = np.arange(-0.5, 1.51, 0.5)
		elif case[0] == "2":
			limits = [-1, 3.0]
			ticks  = np.arange(-1, 3.1, 0.5)
		elif case[0] == "3":
			limits = [-1, 4]
			ticks  = np.arange(-1, 4.1, 0.5)
		else:
			limits = [-1, 5]
			ticks  = np.arange(-1, 5.1, 0.5)

		plt.figure("%s"%case[0:3],figsize = [8,6])
		# plt.title("Min-Max Kasus %s\n Variasi Jarak + Manusia" %case[0:3], fontsize = 15, fontweight = "bold")
		plt.title("Min-Max Kasus %s\n Variasi Jarak" %case[0:3], fontsize = 15, fontweight = "bold")
		plt.plot(x1, y1, "X", label = "AP1", markersize = 12, c = "red")
		plt.plot(x2, y2, "X", label = "AP2", markersize = 12, c = "navy")
		plt.plot(x3, y3, "X", label = "AP3", markersize = 12, c = "darkgreen")
		plt.scatter(x_pred, y_pred, label = "minmax", c = "blue")
		plt.plot(xreal, yreal, "D", label = "real", markersize = 9, c = "brown")
		plt.plot(np.mean(x_pred), np.mean(y_pred), "*", label = "$avg_{minmax}$", markersize = 12, c = "black")
		plt.ylim(limits)
		plt.xlim(limits)
		plt.xticks(ticks, fontsize = 12)
		plt.yticks(ticks, fontsize = 12)
		plt.xlabel("\nx (m)", fontsize = 12)
		plt.ylabel("y (m)", fontsize = 12)
		plt.legend(loc = "lower right", fontsize = 12)
		plt.grid()
		# plt.savefig(fname="D:/Skripsweetku/Raw Data/Grafik PNG/minmax/Variasi Jarak/%s"%case[0:3], dpi=100)
		# plt.savefig(fname="D:/Skripsweetku/Raw Data/Grafik PNG/minmax/Variasi Jarak dan Manusia/%s"%case[0:3], dpi=100)
		plt.show()
		plt.close()

#~~~~~~~~~~~~~~~~~~~~~ Run Program ~~~~~~~~~~~~~~~~~~~~#
if __name__ == '__main__':
	main()
