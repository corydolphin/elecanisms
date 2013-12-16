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
		self.data = np.array([])
		self.goal_dist = -1

	def get_data(self):
		(depth,_) = get_depth()
		(raw_data, _) = depth2xyzuv(depth)
		print len(raw_data)
		self.data = np.array([point for point in raw_data[::4] if inBBox(point, self.bounds)])
		print len(self.data)

	def get_err(self):
		if len(self.data):
			rotErr = np.mean(self.data[:,1])	# average x data
			transErr = self.goal_dist - self.data[:,2].max()		# min z data
		else:
			rotErr, transErr = None, None

		return rotErr, transErr

	def run(self):
		try:
			while(True):
				self.get_data()
				rotErr, transErr = self.get_err()
				print rotErr, transErr
				if len(self.data) is 0:
					tank.set_vel(0,0)
					continue
				if ((abs(rotErr) > .1) or (abs(transErr) > .1)) and transErr:
					tank.set_vel(-20000*transErr, -30000*rotErr)
		except(KeyboardInterrupt):
			self.tank.set_motors(0,0)


def inBounds(val, bounds):
	return val > bounds[0] and val < bounds[1]

def inBBox(point, box):
	res = True
	for val, bounds in zip(point, box):
		res &= inBounds(val,bounds)
	return res
	



if __name__ == '__main__':
	tank = USBTank()
	controller = TankController(tank)
	controller.run()