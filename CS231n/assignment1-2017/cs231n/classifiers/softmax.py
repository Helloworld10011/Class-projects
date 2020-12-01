import numpy as np
from random import shuffle
from past.builtins import xrange

def softmax_loss_naive(W, X, y, reg):
	"""
	Softmax loss function, naive implementation (with loops)

	Inputs have dimension D, there are C classes, and we operate on minibatches
	of N examples.

	Inputs:
	- W: A numpy array of shape (D, C) containing weights.
	- X: A numpy array of shape (N, D) containing a minibatch of data.
	- y: A numpy array of shape (N,) containing training labels; y[i] = c means
	that X[i] has label c, where 0 <= c < C.
	- reg: (float) regularization strength

	Returns a tuple of:
	- loss as single float
	- gradient with respect to weights W; an array of same shape as W
	"""
	# Initialize the loss and gradient to zero.
	num_train= X.shape[0]
	num_classes= W.shape[1]
	loss = 0.0
	dW = np.zeros_like(W)
	scores= X.dot(W)
	
	#############################################################################
	# TODO: Compute the softmax loss and its gradient using explicit loops.     #
	# Store the loss in loss and the gradient in dW. If you are not careful     #
	# here, it is easy to run into numeric instability. Don't forget the        #
	# regularization!                                                           #
	#############################################################################
	for it in range(num_train):
		scores_norm= scores[it]- np.amax(scores[it])
		scores_exp= np.exp(scores_norm)
		scores_sum= np.sum(scores_exp)
		loss += -np.log(scores_exp[y[it]]/scores_sum)
		for j in range(num_classes):
			dW[:, j]+= (scores_exp[j]/scores_sum)*X[it, :]
		dW[:, y[it]]-=X[it, :]
	
	loss= loss/num_train+ reg*np.sum(W**2)
	dW= (dW/num_train)+2*reg*W
	#############################################################################
	#                          END OF YOUR CODE              	                   #
	#############################################################################

	return loss, dW


def softmax_loss_vectorized(W, X, y, reg):
	"""
	Softmax loss function, vectorized version.

	Inputs and outputs are the same as softmax_loss_naive.
	"""
	# Initialize the loss and gradient to zero.
	num_train= X.shape[0]
	scores= X.dot(W)
	scores_exp= np.exp(scores- np.amax(scores, axis=1)[:, np.newaxis])
	scores_exp= scores_exp/np.sum(scores_exp, axis=1)[:, np.newaxis] 
	#############################################################################
	# TODO: Compute the softmax loss and its gradient using no explicit loops.  #
	# Store the loss in loss and the gradient in dW. If you are not careful     #
	# here, it is easy to run into numeric instability. Don't forget the        #
	# regularization!                                                           #
	#############################################################################
	loss= np.sum(-np.log(scores_exp[list(range(num_train)), y]))/num_train+ reg*np.sum(W**2)
	
	scores_exp[list(range(num_train)), y]= scores_exp[list(range(num_train)), y]- np.ones(num_train)
	dW= ((X.T).dot(scores_exp))/num_train + 2*reg*W
	#############################################################################
	#                          END OF YOUR CODE                                 #
	#############################################################################

	return loss, dW

