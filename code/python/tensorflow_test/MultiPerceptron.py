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

hidden1 = tf.nn.relu(tf.matmul(x,W1) + b1)
hidden1_drop = tf.nn.dropout(hidden1,keep_prob)
#第一步，定义算法公式
y = tf.nn.softmax(tf.matmul(hidden1_drop,W2) + b2)

#第二步，定义损失函数和选择优化器来优化loss,优化器选择自适应的优化器Adagrad,学习率设0.3
y_ = tf.placeholder(tf.float32,[None,10])
cross_entropy = tf.reduce_mean(-tf.reduce_sum(y_ * tf.log(y),
                               reduction_indices=[1]))
train_step = tf.train.AdagradOptimizer(0.3).minimize(cross_entropy)

#第三步，加入keep_prob作为计算图的输入，训练时设为0.75,即保留75%的节点，规模越大的神经网络，dropout效果越显著
tf.global_variables_initializer().run()
for i in range(3000):
    batch_xs,batch_ys = mnist.train.next_batch(100)
    train_step.run({x:batch_xs,y_:batch_ys,keep_prob:0.75})

#第四步，准确率评测
correct_prediction = tf.equal(tf.argmax(y,1),tf.argmax(y_,1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction,tf.float32))
print(accuracy.eval({x:mnist.test.images,y_:mnist.test.labels,keep_prob:1.0}))




