# --coding:utf-8--
"""
tensor存储的数据用掉就会消失，Variable在模型训练迭代中是持久化的
"""
from tensorflow.examples.tutorials.mnist import input_data
#加载数据
# mnist = input_data.read_data_sets("MNIST_data/",one_hot=True)
# print(mnist.train.images.shape,mnist.train.labels.shape)
import tensorflow as tf
sess = tf.InteractiveSession()
x = tf.placeholder(tf.float32,[None,784])
#因为是softmax regression，此处对应十组分类，所以有十组权重
W = tf.Variable(tf.zeros([784,10]))
b = tf.Variable(tf.zeros([10]))
#softmax regression; y = softmax(wx + b)
y = tf.nn.softmax(tf.matmul(x,W) + b)
#cross-entropy交叉熵, Hy'(y) = -∑y'i * log(yi) ,y'是真实概率分布，y是预测的
y_ = tf.placeholder(tf.float32,[None,10])
cross_entropy = tf.reduce_mean(-tf.reduce_sum(y_* tf.log(y),
                                              reduction_indices=[1]))



