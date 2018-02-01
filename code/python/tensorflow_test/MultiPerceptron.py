import tensorflow as tf
from mnist import read_data_sets

mnist = read_data_sets("MNIST_data/",one_hot=True)
sess = tf.InteractiveSession()

in_units = 784 # 输入节点数
h1_units = 300 # 隐含层节点数

#偏置初始为0，权重初始化为截断的正态分布，标准差为0.1
# W1对应784个特征，300个输出
W1 = tf.Variable(tf.truncated_normal([in_units,h1_units],stddev=0.1))
b1 = tf.Variable(tf.zeros([h1_units]))  # 300个输出
W2 = tf.Variable(tf.zeros([h1_units,10]))
b2 = tf.Variable(tf.zeros([10]))

x = tf.placeholder(tf.float32,[None,in_units])
# dropout的比率是不一样的，通常训练时小于1，预测时等于1
keep_prob = tf.placeholder(tf.float32)

hidden1 = tf.nn.relu(tf.matmul(x.W1) + b1)
hidden1_drop = tf.nn.dropout(hidden1,keep_prob)

y = tf.nn.softmax(tf.matmul(hidden1_drop,W2) + b2)
