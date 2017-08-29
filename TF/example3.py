from __future__ import print_function
import tensorflow as tf
import numpy as np

cluster = tf.train.ClusterSpec({"local": ["192.168.122.171:2222", "192.168.122.40:2222"]})

x_data = np.linspace(-1, 1, 300, dtype=np.float32)[:, np.newaxis]
noise = np.random.normal(0, 0.05, x_data.shape).astype(np.float32)
y_data = np.square(x_data) - 0.5 + noise
xs = tf.placeholder(tf.float32, [None, 1])
ys = tf.placeholder(tf.float32, [None, 1])

Weights1 = tf.Variable(tf.random_normal([1,10]),name="weights1")
biases1 = tf.Variable(tf.zeros([1,10]) + 0.1,name="biases1")

Weights2 = tf.Variable(tf.random_normal([10,1]),name="weights2")
biases2 = tf.Variable(tf.zeros([1,1]) + 0.1,name="biases2")

with tf.device("/job:local/task:1"):
    Wx_plus_b1 = tf.matmul(xs, Weights1) + biases1 # hidden layer
    l1 = tf.nn.relu(Wx_plus_b1)

with tf.device("/job:local/task:0"):
    prediction = tf.matmul(l1, Weights2) + biases2 # output layer
    loss = tf.reduce_mean(tf.reduce_sum(tf.square(ys-prediction), reduction_indices=[1]))
    train_step = tf.train.GradientDescentOptimizer(0.1).minimize(loss)

init = tf.global_variables_initializer()
with tf.Session("grpc://192.168.122.40:2222") as sess:
    sess.run(init)

    for i in range(10000):
        sess.run(train_step, feed_dict={xs: x_data, ys: y_data})
        if i % 50 == 0:
            print(sess.run(loss, feed_dict={xs: x_data, ys: y_data}))
