from __future__ import print_function
import tensorflow as tf
import numpy as np

cluster = tf.train.ClusterSpec({"local": ["192.168.122.171:2222", "192.168.122.40:2222"]})

with tf.device("/job:local/task:1"):
    x_data = np.random.rand(100).astype(np.float32)
    y_data = x_data*0.1 + 0.3
    Weights = tf.Variable(tf.random_uniform([1], -1.0, 1.0))
    biases = tf.Variable(tf.zeros([1]))
    y = Weights*x_data + biases

with tf.device("/job:local/task:0"):
    loss = tf.reduce_mean(tf.square(y-y_data))
    optimizer = tf.train.GradientDescentOptimizer(0.5)
    train = optimizer.minimize(loss)

init = tf.global_variables_initializer()
with tf.Session("grpc://192.168.122.40:2222") as sess:
    sess.run(init)
    for step in range(201):
        sess.run(train)
        if step % 20 == 0:
            print(step, sess.run(Weights), sess.run(biases))
