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
		self.bounds = ((-1,1),(-1,1),(-2,.1))
		self.data = np.array([])
		self.goal_dist = -1

	def get_data(self):
		(depth,_) = get_depth()
		(raw_data, _) = depth2xyzuv(depth)
		self.data = np.array([point for point in raw_data[::4] if inBBox(point, self.bounds)])

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
				if len(self.data) is 0:
					tank.set_vel(0,0)
					continue
				if transErr: # if there are points detected
					linVel, angVel = self.get_speed(transErr, rotErr)
					tank.set_vel(linVel, angVel)
		except(KeyboardInterrupt):
			self.tank.set_motors(0,0)

	def get_speed(self, transErr, rotErr):
		# proportional control
		linVel = -100000*transErr
		angVel = -100000*rotErr

		# saturate
		linVel = max(min(linVel, 32767), -32767)
		angVel = max(min(angVel, 32767), -32767)

		# dead zone
		if abs(transErr) < .1:
			linVel = 0
		if abs(rotErr) < .1:
			angVel = 0

		return linVel, angVel



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