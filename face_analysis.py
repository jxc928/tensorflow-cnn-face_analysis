import imageread as image

import tensorflow as tf
import numpy as np
import os

def init_weights(shape):
    return tf.Variable(tf.random_normal(shape, stddev=0.01))


def model(X, w, w2, w3, w4, w_o, p_keep_conv, p_keep_hidden):
    l1a = tf.nn.relu(tf.nn.conv2d(X, w,                       # l1a shape=(?, 28, 28, 32)
                        strides=[1, 1, 1, 1], padding='SAME'))
    l1 = tf.nn.max_pool(l1a, ksize=[1, 2, 2, 1],              # l1 shape=(?, 14, 14, 32)
                        strides=[1, 2, 2, 1], padding='SAME')

    l1 = tf.nn.dropout(l1, p_keep_conv)
    l2a = tf.nn.relu(tf.nn.conv2d(l1, w2,                     # l2a shape=(?, 14, 14, 64)
                        strides=[1, 1, 1, 1], padding='SAME'))
    l2 = tf.nn.max_pool(l2a, ksize=[1, 2, 2, 1],              # l2 shape=(?, 7, 7, 64)
                        strides=[1, 2, 2, 1], padding='SAME')
    l2 = tf.nn.dropout(l2, p_keep_conv)

    l3a = tf.nn.relu(tf.nn.conv2d(l2, w3,                     # l3a shape=(?, 7, 7, 128)
                        strides=[1, 1, 1, 1], padding='SAME'))
    l3 = tf.nn.max_pool(l3a, ksize=[1, 2, 2, 1],              # l3 shape=(?, 4, 4, 128)
                        strides=[1, 2, 2, 1], padding='SAME')
    l3 = tf.reshape(l3, [-1, w4.get_shape().as_list()[0]])    # reshape to (?, 2048)
    l3 = tf.nn.dropout(l3, p_keep_conv)

    l4 = tf.nn.relu(tf.matmul(l3, w4))
    l4 = tf.nn.dropout(l4, p_keep_hidden)

    pyx = tf.matmul(l4, w_o)
    return pyx

y_data = [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]

X = tf.placeholder("float", [None, 28, 28, 3])
Y = tf.placeholder("float", [None, 4])

w = init_weights([3, 3, 3, 32])       # 3x3x3 conv, 32 outputs
w2 = init_weights([3, 3, 32, 64])     # 3x3x32 conv, 64 outputs
w3 = init_weights([3, 3, 64, 128])    # 3x3x64 conv, 128 outputs
w4 = init_weights([128 * 4 * 4, 625]) # FC 128 * 4 * 4 inputs, 625 outputs
w_o = init_weights([625, 4])         # FC 625 inputs, 10 outputs (labels)

p_keep_conv = tf.placeholder("float")
p_keep_hidden = tf.placeholder("float")
py_x = model(X, w, w2, w3, w4, w_o, p_keep_conv, p_keep_hidden)

cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(py_x, Y))
train_op = tf.train.RMSPropOptimizer(0.001, 0.9).minimize(cost)
predict_op = tf.argmax(py_x, 1)

x = image.readimage('img/')
# Launch the graph in a session
with tf.Session() as sess:
    # you need to initialize all variables
    tf.initialize_all_variables().run()

    for i in range(1000):
        sess.run(train_op, feed_dict={X: x, Y: y_data, p_keep_conv: 0.8, p_keep_hidden: 0.5})
        print sess.run(cost, feed_dict={X: x, Y: y_data, p_keep_conv: 0.8, p_keep_hidden: 0.5})

    data =[image.doflat('img/2/1.jpg')]

    if(sess.run(predict_op, feed_dict={X: data, p_keep_conv: 1, p_keep_hidden: 1})[0]) == 0:
        print "dohoon1"

    elif(sess.run(predict_op, feed_dict={X: data, p_keep_conv: 1, p_keep_hidden: 1})[0]) == 1:
        print "minsuk2"

    elif (sess.run(predict_op, feed_dict={X: data, p_keep_conv: 1, p_keep_hidden: 1})[0]) == 2:
        print "sukjoon3"

    elif (sess.run(predict_op, feed_dict={X: data, p_keep_conv: 1, p_keep_hidden: 1})[0]) == 3:
        print "seunghyun4"


