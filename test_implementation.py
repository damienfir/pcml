import sys
import scipy.io
import numpy as np
from utils import *
import stream_utils as streams
import mlp, lstsq, logistic

block_size = 10
mlp_classifier = mlp.MLP(0.01, 0.1, 10, 10)
lstsq_classifier = lstsq.LeastSquares(0.1)
log_classifier = logistic.LogisticLoss(0.01, 0.1)

def classify(classifier, validations):
	errors = 0.0
	for _ in xrange(0, validations.size):
		x_left, x_right, t = validations.next()
		error, classerror = classifier.error(x_left, x_right, t)
		errors += error
	avg_error = errors / float(validations.size)
	print "Average error =", avg_error

def classify_binary(classifier):
	return classify(classifier, streams.validation_binary())

def classify_5class(classifier):
	return classify(classifier, streams.validation_5class())

def test_mlp_binary():
	stream = streams.training_binary(count=block_size)
	for _ in xrange(0, 100):
		x_left, x_right, t = stream.next()
		mlp_classifier.train(x_left, x_right, t)
	classify_binary(mlp_classifier)

def test_least_squares():
	stream = streams.training_5class()
	x_left, x_right, t = stream.all()
	lstsq_classifier.train(x_left, x_right, t)
	classify_5class(lstsq_classifier)

def test_logistic():
	stream = streams.training_5class(count=block_size)
	for _ in xrange(0, 100):
		x_left, x_right, t = stream.next()
		log_classifier.train(x_left, x_right, t)
	classify_5class(log_classifier)

test_least_squares()

