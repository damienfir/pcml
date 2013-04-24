import numpy as np

class LeastSquares:

	def __init__(self, v, k=5):
		self.v = v
		self.k = k

	def train(self, x_lefts, x_rights, ts):
		x_lefts = np.mat(x_lefts, dtype=np.float)
		x_rights = np.mat(x_rights, dtype=np.float)
		X = np.mat(np.vstack([x_lefts, x_rights, np.ones(x_lefts.shape[1])]), dtype=np.float).T
		t = np.mat(np.vstack(map(lambda k: ts == k, range(1, self.k + 1))), dtype=np.float).T
		A = X.T * X + self.v * np.diagflat(np.ones(X.shape[1]))
		b = X.T * t

		# use numpy to solve the least squares normal equations problem
		ws, _, _, _ = np.linalg.lstsq(A, b)
		self.ws = ws

	def classify(self, x_left, x_right):
		x_left = np.mat(x_left, dtype=np.float)
		x_right = np.mat(x_right, dtype=np.float)
		X = np.mat(np.vstack([x_left, x_right, np.ones(x_left.shape[1])]), dtype=np.float)
		result = np.argmax(X.T * self.ws, 1)
		return (result + 1).T