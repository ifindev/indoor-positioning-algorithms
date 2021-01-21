"""
Author	: Muhammad Arifin
Date	: 7th May, 2020
Subject	: Implementation of trilateration calculation

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

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

######## Function to calculate trilateration parameters ########

def trilat_params(xi,yi,xj,yj,ri,rj):
	a = -2*xi + 2*xj
	b = -2*yi + 2*yj
	c = ri**2 - rj**2 - xi**2 + xj**2 - yi**2 + yj**2

	return a,b,c


######## Implementation of trilateration calculation process ########
# Function of Trilateration Calculation Process
# Data to be processed is stored as csv file. 
# Data is processed entirely using pandas dataframe

def trilateration_process(path, case, ple, rssi_d0):
	# Read csv file as panda data frame
	df = pd.read_csv(path+case)

	# Drop 'Time' column
	df = df.drop(columns=["Time"])

	# Drop NaN values
	df = df.dropna()

	# Take only column 0-3 which is AP1, AP2, and AP3
	# This step is important as sometimes the csv data
	# has other column aside Time, and RSSI values of 
	# AP1, AP2, and AP3

	df = df.iloc[:,0:3]

	# Rename columns to AP1, AP2, and AP3
	df.columns = ["AP1", "AP2", "AP3"]


	# Add path loss exponent and rssi at d0 parameters
	# Create a lambda function to convert RSSI data into distance
	dist = lambda k, n, rssi: 10**((k - rssi) / (10*n))

	# Add distance columns in df 
	for i in range(1,4):
		df["dist%d"%i] = dist(rssi_d0, ple, df["AP%d"%i])


	# Determining what is the distance case 
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

	ap_coordinates = [[x1,y1], [x2, y2], [x3, y3]]

	# Calculation target Coordinates 
	# check which STA position case is being analysed
	# Also check whether the entered case is in capital or not

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

	# Trilateration parameters calculation
	# Calculate A, B, C, D, E, and F 
	A, B, C = trilat_params(x1, y1, x2, y2, df["dist1"], df["dist2"])
	D, E, F = trilat_params(x2, y2, x3, y3, df["dist2"], df["dist3"])

	# Calculate x and y using trilateration
	# x = CE - BF / AE - BD; y = CD - AF / BD - AE
	xtr = (C*E - B*F) / (A*E - B*D)
	ytr = (C*D - A*F) / (B*D - A*E)

	# Determine the Squared Root Error and the Mean Squared Error 
	SQEtr = np.sqrt((xtr - xreal)**2 + (ytr - yreal)**2)
	MSEtr = np.mean(SQEtr)

	# Add target coordinates,
	# predicted coordinates by trilateration
	# also the SQRT error in df

	df["xreal"]   = xreal  		
	df["xtrilat"] = xtr	

	df["yreal"]   = yreal
	df["ytrilat"] = ytr

	df["SQEtr"]	  = SQEtr

	# Return the trilateration df and MSE
	return (df, MSEtr, ap_coordinates)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~ Main Program ~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
def main():

	""" Run the program """
	# Data Paths
	# path = 'D:/Skripsweetku/Raw Data/Pengukuran Variasi Jarak Ulangan/'
	path = 'D:/Skripsweetku/Raw Data/Pengukuran Variasi Jarak dan Manusia/'
	cases = os.listdir(path)
	#cases = ['3D1.csv']

	# RSSI @d0 and path loss exponent (gamma)
	gamma = 2.255
	K = -49

	# Run all cases in the directory
	print(path)
	for x in cases:
		df, mse, ap_coords = trilateration_process(path, x, gamma, K)

		# Assign APs coordinates
		ap1_xcoord = ap_coords[0][0]
		ap1_ycoord = ap_coords[0][1]

		ap2_xcoord = ap_coords[1][0]
		ap2_ycoord = ap_coords[1][1]

		ap3_xcoord = ap_coords[2][0]
		ap3_yxoord = ap_coords[2][1]

		#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
		""" Print All the Results """
		print("\n")
		print("Localization using ESP32 %s \n" %x)
		# print(df)
		# print(ap_coords)
		# x_real = np.mean(df["xreal"])
		# y_real = np.mean(df["yreal"])
		# x_trilat = round(np.mean(df["xtrilat"]),2)
		# y_trilat = round(np.mean(df["ytrilat"]),2)
		# print("Real x coordinate    : ",x_real)
		# print("Mean x Trilateration : ",x_trilat)
		# print("Real y coordinate    : ",y_real)
		# print("Mean y Trilateration : ",y_trilat)
		print("MSE Trilaterasi      : ",round(mse,2))
		# print("Standar Deviasi x-tri: ",round(np.std(df["xtrilat"]),2))
		# print("Standar Deviasi y-tri: ",round(np.std(df["ytrilat"]),2))

		# Graph limits and ticks based on case
		if x[0] == "1":
			limits = [-0.5, 4]
			ticks  = np.arange(-0.5, 4.1, 0.5)
		elif x[0] == "2":
			limits = [-1, 3.0]
			ticks  = np.arange(-1, 3.1, 0.5)
		elif x[0] == "3":
			limits = [-1, 4]
			ticks  = np.arange(-1, 4.1, 0.5)
		else:
			limits = [-1, 5]
			ticks  = np.arange(-1, 5.1, 0.5)

		# Graphing the Results
		# Plot the results
		plt.figure("%s" %x[0:3], figsize = [8,6])
		# plt.title("Trilaterasi Kasus %s\n Variasi Jarak" %x[0:3], fontsize = 15, fontweight = "bold")
		plt.title("Trilaterasi Kasus %s\n Variasi Jarak + Manusia" %x[0:3], fontsize = 15, fontweight = "bold")
		plt.plot(ap1_xcoord, ap1_ycoord, "X", label = "AP1", markersize = 12, c = "red")
		plt.plot(ap2_xcoord, ap2_ycoord, "X", label = "AP2", markersize = 12, c = "navy")
		plt.plot(ap3_xcoord, ap3_yxoord, "X", label = "AP3", markersize = 12, c = "darkgreen")
		plt.scatter(df["xtrilat"], df["ytrilat"], label = "tri", c = "blue")
		plt.plot(df["xreal"], df["yreal"], "D", label = "real", markersize = 9, c = "brown")
		plt.plot(np.mean(df["xtrilat"]), np.mean(df["ytrilat"]), "*", label = "$avg_{tri}$", markersize = 12, c = "black")

		# Setting the limits of graph
		# also the ticks
		# Save the image in image directory
		plt.ylim(limits)
		plt.xlim(limits)
		plt.xticks(ticks, fontsize = 12)
		plt.yticks(ticks, fontsize = 12)
		plt.xlabel("\nx (m)", fontsize = 12)
		plt.ylabel("y (m)", fontsize = 12)
		plt.legend(loc = "lower right", fontsize = 12)
		plt.grid()
		# plt.savefig(fname="D:/Skripsweetku/Raw Data/Grafik PNG/trilaterasi/Variasi Jarak/%s"%x[0:3], dpi=100)
		# plt.savefig(fname="D:/Skripsweetku/Raw Data/Grafik PNG/trilaterasi/Variasi Jarak dan Manusia/%s"%x[0:3], dpi=100)
		plt.show()
		plt.close()

if __name__ == '__main__':
	main()
