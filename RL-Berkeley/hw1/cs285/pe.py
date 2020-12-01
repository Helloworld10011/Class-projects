from cs285.policies.MLP_policy import *
import os
import numpy as np
import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

import gym


sess= tf.Session()
env= gym.make('Ant-v2')

ob_dim= env.observation_space.shape[0]
ac_dim= env.action_space.shape[0]

model= MLPPolicySL(sess, ac_dim, ob_dim, 2, 64)
model.restore('data/dagger_test_dagger_ant_Ant-v2_28-04-2020_20-03-41/policy_itr_9')

ob= env.reset()

#for _ in range(1000):
env.render()

#ac= model.get_action(ob[np.newaxis, :])
#ob, reward, done, info= env.step(ac[0]) # take a random action


env.close()