# --coding:utf-8--
"""
tensor存储的数据用掉就会消失，Variable在模型训练迭代中是持久化的
"""
from tensorflow.examples.tutorials.mnist import input_data
from mnist import read_data_sets
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
cross_entropy = tf.reduce_mean(-tf.reduce_sum(y_* tf.log(y),
                                              reduction_indices=[1]))
# 学习率0.5
train_step = tf.train.GradientDescentOptimizer(0.5).minimize(cross_entropy)
tf.global_variables_initializer().run() # 全局参数初始化器
# 每次随机从训练集中抽取100条样本构成mini-batch，使用一小部分样本进行训练称随机梯度下降
for i in range(1000):
    batch_xs,batch_ys = mnist.train.next_batch(100)
    train_step.run({x:batch_xs,y_:batch_ys})

correct_prediction = tf.equal(tf.argmax(y,1),tf.argmax(y_,1))   # boolean
accuray = tf.reduce_mean(tf.cast(correct_prediction,tf.float32)) #

print(accuray.eval({x:mnist.test.images,y_:mnist.test.labels}))