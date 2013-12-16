#!/usr/bin/env python
from freenect import sync_get_depth as get_depth
import cv  
import numpy as np
from calibkinect import depth2xyzuv
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

from USBTank import USBTank

class TankController():
	def __init__(self, tank):
		self.tank = tank
		self.bounds = ((-1,1),(-1,1),(-1.5,.1))
		self.data = np.array()

	def get_data(self):
		(depth,_) = get_depth()
		(raw_data, _) = depth2xyzuv(depth)
		self.data = np.array([point for point in raw_data[::1] if inBBox(point, self.bounds)])

	def get_err(self):
		if len(self.data):
			rotErr = np.mean(self.data[:,1])	# average x data
			transErr = self.data[:,2].min()		# min z data
		else:
			rotErr, transErr = None, None

		return rotErr, transErr

	def run(self):
		while(True):
			self.get_data()
			rotErr, transErr = self.get_err()
			tank.set_vel(-transErr, -rotErr)


def inBounds(val, bounds):
	return val > bounds[0] and val < bounds[1]

def inBBox(point, box):
	res = True
	for val, bounds in box:
		res &= inBounds(val,bounds)
	return res
	



if __name__ == '__main__':
	tank = USBTank()
	controller = TankController(tank)
	controller.run()