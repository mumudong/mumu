# --coding:utf-8--
"""
回归用sigmoid
分类用softmax
tensor存储的数据用掉就会消失，Variable在模型训练迭代中是持久化的
"""
import matplotlib.pyplot as plt
import matplotlib.pylab as pylab
from tensorflow.examples.tutorials.mnist import input_data
from mnist import read_data_sets
import numpy as np
#加载数据
mnist = read_data_sets("MNIST_data/",one_hot=True)
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
# reduction_indices删掉的维度,reduce_sum删除axis=1的维度，10 * 20的数据之后只剩下10行
cross_entropy = tf.reduce_mean(-tf.reduce_sum(y_* tf.log(y),
                                              reduction_indices=[1]),reduction_indices=None)
# 学习率0.5
train_step = tf.train.GradientDescentOptimizer(0.5).minimize(cross_entropy)
tf.global_variables_initializer().run() # 全局参数初始化器
# 每次随机从训练集中抽取100条样本构成mini-batch，使用一小部分样本进行训练称随机梯度下降
for i in range(1000):
    batch_xs,batch_ys = mnist.train.next_batch(100)
    train_step.run({x:batch_xs,y_:batch_ys})
# 比较输出的结果[长度为10的数组]，数组中最大值对应的下标。若axis=0则比较所有数组第一位最大值对应的行数...
correct_prediction = tf.equal(tf.argmax(y,1),tf.argmax(y_,1))   # boolean
accuray = tf.reduce_mean(tf.cast(correct_prediction,tf.float32)) #

for i in range(0, len(mnist.test.images)):
    result = sess.run(correct_prediction, feed_dict={x: np.array([mnist.test.images[i]]), y_: np.array([mnist.test.labels[i]])})
    if not result:
        print('预测的值是：',sess.run(y, feed_dict={x: np.array([mnist.test.images[i]]), y_: np.array([mnist.test.labels[i]])}))
        print('实际的值是：',sess.run(y_,feed_dict={x: np.array([mnist.test.images[i]]), y_: np.array([mnist.test.labels[i]])}))
        one_pic_arr = np.reshape(mnist.test.images[i], (28, 28))
        pic_matrix = np.matrix(one_pic_arr, dtype="float")
        plt.imshow(pic_matrix) # 热图，通过色差、亮度来分析数据，增加颜色标注  plt.colorbar(cax=None,ax=None,shrink=0.5)可设置Bar为一半长度。
        pylab.show()
        break

# print(accuray.eval({x:mnist.test.images,y_:mnist.test.labels}))
print("准确率---->",sess.run(accuray, feed_dict={x: mnist.test.images,
                                    y_: mnist.test.labels}))