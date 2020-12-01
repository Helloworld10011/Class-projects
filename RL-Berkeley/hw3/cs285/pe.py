import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()
import numpy as np

#x= tf.one_hot([1, 2, 4, -1, -1, -1, -1, 1], 10)
#print(x.numpy())

def lander_model(obs, num_actions, scope= "lander_model", reuse= True):
    with tf.variable_scope(scope, reuse= reuse):
        with tf.variable_scope("action_value"):
            out = tf.layers.dense(obs, units=64, activation='relu')
            out = tf.layers.dense(out, units=64, activation='relu')
            out = tf.layers.dense(out, units= num_actions)
        return out


ac_dim =4
ob_dim = 50

input_shape = (ob_dim,)

obs_t_ph = tf.random.normal([5, ob_dim])
act_t_ph = tf.random.uniform([5, ], minval=0, maxval= ac_dim, dtype= tf.int32)

q_t_values1 = lander_model(obs_t_ph, ac_dim, scope='q_func', reuse= False)
q_t_values2 = lander_model(obs_t_ph, ac_dim, scope='q_func_2', reuse= False)
q_t_values3 = lander_model(obs_t_ph, ac_dim, scope='q_func', reuse= False)

q_t_values4= lander_model(obs_t_ph, ac_dim, scope= 'q_2', reuse= False)

loss= tf.reduce_sum(q_t_values1)

opt= tf.train.AdamOptimizer()
opt.gra

with tf.Session() as sess:
    tf.global_variables_initializer().run()
    q1, q2, q3, q4 = sess.run([q_t_values1, q_t_values2, q_t_values3, q_t_values4])

    print(q1, q2, q3, q4)

#q_t = tf.reduce_sum(q_t_values * tf.one_hot(act_t_ph, ac_dim), axis=1)
#print(q_t)


