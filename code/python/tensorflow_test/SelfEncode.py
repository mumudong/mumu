#--encoding:utf-8--
import numpy as np
import sklearn.preprocessing as prep
import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data
import mnist
# xaiver初始化器,可让初始化权重刚好合适，让权重满足0均值，方差为 2/(innum + outnum)
def xavier_init(fan_in,fan_out,constant = 1):
    low = -constant * np.sqrt(6.0 / (fan_in + fan_out))
    high = constant * np.sqrt(6.0 / (fan_in + fan_out))
    return tf.random_uniform((fan_in,fan_out),
                             minval = low,maxval = high,
                             dtype = tf.float32)

# 去噪自编码class
class AdditiveGaussianNoiseAutoencoder(object):
    def __init__(self,n_input,n_hidden,transfer_function=tf.nn.softplus,
                       optimizer=tf.train.AdamOptimizer(),scale=0.1):
        self.n_input = n_input
        self.n_hidden = n_hidden
        self.transfer = transfer_function
        self.scale = tf.placeholder(tf.float32)
        self.training_scale =scale
        network_weights = self._initialize_weights()
        self.weights =network_weights
        #定义网络数据
        self.x = tf.placeholder(tf.float32,[None,self.n_input])
        self.hidden = self.transfer(tf.add(tf.matmul(
            self.x + scale * tf.random_normal((n_input,)),
            self.wights['w1']),self.weights['b1']))
        self.reconstruction = tf.add(tf.matmul(self.hidden,
                                               self.weights['w2']),
                                               self.weights['b2'])
        self.cost = 0.5 * tf.reduct_sum(tf.pow(tf.subtract(
            self.reconstruction,self.x),2.0))
        self.optimizer = optimizer.minimize(self.cost)

        init = tf.global_variables_initializer()
        self.sess = tf.Session()
        self.sess.run(init)

    def _initialize_weights(self):
        all_weights = dict()
        all_weights['w1'] = tf.Variable(xavier_init(self.n_input,
                                                    self.n_hidden))
        all_weights['b1'] = tf.Variable(tf.zeros([self.n_hidden],
                                                 dtype=tf.float32))
        all_weights['w2'] = tf.Variable(tf.zeros([self.n_hidden,
                                                  self.n_input],
                                                 dtype=tf.float32))
        all_weights['b2'] = tf.Variable(tf.zeros([self.n_input],
                                                 dtype=tf.float32))
        return all_weights



