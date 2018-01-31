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
            self.weights['w1']),self.weights['b1']))
        self.reconstruction = tf.add(tf.matmul(self.hidden,
                                               self.weights['w2']),
                                               self.weights['b2'])
        self.cost = 0.5 * tf.reduce_sum(tf.pow(tf.subtract(
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
    """
        用一个batch数据进行训练并返回当前的损失cost
        只运行两个计算图的节点，分别是cost、optimizer
        输入的feed_dict包括输入数据x，以及噪声的系数scale
    """
    def partial_fit(self,X):
        cost,opt = self.sess.run((self.cost,self.optimizer),
                                 feed_dict={self.x:X,self.scale:self.training_scale})
        return cost
    """
    只求损失函数，测试集测试用
    """
    def calc_total_cost(self,X):
        return self.sess.run(self.cost,feed_dict={self.x:X,
                                                  self.scale:self.training_scale})
    """
    返回自编码器隐含层的输出结果
    目的是提供一个接口来获取抽象后的特征
    """
    def transform(self,X):
        return self.sess.run(self.hidden,feed_dict={self.x:X,
                                                    self.scale:self.training_scale})
    """
    将隐含层的输出结果作为输入，通过之后的重建层将提取到的高阶特征复原为原始数据。
    和前面的transform正好将自编码器拆分为两部分
    """
    def generate(self,hidden=None):
        if hidden is None:
            hidden = np.random.normal(size = self.weights['b1'])
        return self.sess.run(self.reconstruction,feed_dict={self.hidden:hidden})
    """
    整体运行一遍复原过程，包括提取高阶特征和通过高阶特征富源数据
    即包括transform和generate两块，输入数据为原数据，输出数据为复原后数据
    """
    def reconstruct(self,X):
        return self.sess.run(self.reconstruction,feed_dict={self.x:X,
                                                            self.scale:self.training_scale})
    """
    获取隐含层的权重W1
    """
    def getWeights(self):
        return self.sess.run(self.weights['w1'])
    """
    获取隐含层的偏置系数
    """
    def getBiases(self):
        return self.sess.run(self.weights['b1'])

from mnist import read_data_sets
mnist = read_data_sets("MNIST_data/",one_hot=True)
"""
标准化操作
"""
def standard_scale(X_train,X_test):
    preprocessor = prep.StandardScaler().fit(X_train)
    X_train = preprocessor.transform(X_train)
    X_test = preprocessor.transform(X_test)
    return X_train,X_test

"""
随机获取block数据，取一个从0 - batch_size之间的随机整数为起点，顺序读取size个数据
"""
def get_random_block_from_data(data,batch_size):
    start_index = np.random.randint(0,len(data)-batch_size)
    return data[start_index:(start_index + batch_size)]

X_train,X_test = standard_scale(mnist.train.images,mnist.test.images)
"""
定义常用参数：
    最大训练轮数 epoch 20
    batch_size 128
    每一轮epoch就显示一次损失cost
"""
n_samples = int(mnist.train.num_examples)
training_epochs = 20
batch_size = 128
display_step = 1
"""
模型输入节点数 n_input 784
隐含层节点数 n_hidden 200
隐含层激活函数 transfer_function softplus
噪声系数 scale 0.01
优化器optimizer为Adam，且学习率为0.001
"""
autoencoder = AdditiveGaussianNoiseAutoencoder(n_input=784,
                                               n_hidden=200,
                                               transfer_function=tf.nn.softplus,
                                               optimizer=tf.train.AdamOptimizer(learning_rate=0.001),
                                               scale=0.01)

for epoch in range(training_epochs):
    avg_cost = 0.
    total_batch = int(n_samples / batch_size)
    for i in range(total_batch):
        batch_xs = get_random_block_from_data(X_train,batch_size)
        cost = autoencoder.partial_fit(batch_xs)
        avg_cost += cost / n_samples * batch_size
    if epoch % display_step == 0 :
        print("Epoch:",'%04d'%(epoch + 1),"cost=","{:.9f}".format(avg_cost))

print("Total cost: " + str(autoencoder.calc_total_cost(X_test)))
