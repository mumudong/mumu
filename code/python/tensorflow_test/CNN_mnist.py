import tensorflow as tf
from mnist import read_data_sets

mnist = read_data_sets("MNIST_data/",one_hot=True)
sess = tf.InteractiveSession()

def weight_variable(shape):
    # 使用截断的正态分布给权重制造一些随机噪声来打破完全对称,截断分布是指，限制变量x 取值范围
    initial = tf.truncated_normal(shape,stddev=0.1) # 产生正态分布的值与均值的差若大于两倍的标准差就重新生成
    return tf.Variable(initial)

def bias_variable(shape):
    # 因采用ReLU，给偏置加一些较小的正值0.1，来避免死亡节点。
    initial = tf.constant(0.1,shape=shape)
    return initial
"""
  x是输入，W是卷积的参数,如[5,5,1,32],前两个参数是卷积核的尺寸
      第三个代表有多少个channel，因为只有灰度单色，所以是1，若是RGB,则应为3
      第四个参数代表卷积核的数量，即卷积层会提取多少类特征
  strides代表卷积模板移动的步长，都是1代表不遗漏的划过图片每个点
  padding代表边界的处理方式，same代表给边界加上padding让卷积的中心扫过所有点，输出和输入保持同样的尺寸
                             valid则让边重合边
"""
def conv2d(x,W):
    return tf.nn.conv2d(x,W,strides=[1,1,1,1],padding='SAME')
"""
value [batch, height, width, channels]
ksize表示池化的大小，即[batch,in_height,in_wide, in_channels]，目前一般batch和channels不做池化，对应为1
strides表示在特征图上移动,[batch,in_height,in_wide, in_channels]
"""
def max_pool_2x2(x):
    return tf.nn.max_pool(x,ksize=[1,2,2,1],strides=[1,2,2,1],
                          padding='SAME')
"""
x是特征，y_是真实label,卷积网络会用到空间结构，需将1D输入向量转为2D图片结构
[-1,28,28,1]第一个-1代表样本数量不固定，最后的1代表颜色通道数量
"""
x = tf.placeholder(tf.float32,[None,784])
y_ = tf.placeholder(tf.float32,[None,10])
x_image = tf.reshape(x,[-1,28,28,1])

# 第一个卷积层
W_conv1 = weight_variable([5,5,1,32]) # 卷积核尺寸5X5,1个颜色通道，32个不同的卷积核
b_conv1 = bias_variable([32]) # 32中卷积核，同样数量的偏置
h_conv1 = tf.nn.relu(conv2d(x_image,W_conv1) + b_conv1) # 激活
h_pool1 = max_pool_2x2(h_conv1)

# 第二个卷积层
W_conv2 = weight_variable([5,5,32,64]) # 提取64种特征
b_conv2 = bias_variable([64])
h_conv2 = tf.nn.relu(conv2d(h_pool1,W_conv2) + b_conv2)
h_pool2 = max_pool_2x2(h_conv2)

# 经过前两次步长2x2的最大池化，边长只有1/4了，图片尺寸由28*28变为7*7
# 第二个卷积核数量为64，输出tensor尺寸为 7*7*64.
# 将其输出转为1D向量，然后链接一个全连接层，隐含节点为1024
W_fc1 = weight_variable([7 * 7 * 64,1024])
b_fc1 = bias_variable([1024])
h_pool2_flat = tf.reshape(h_pool2,[-1,7*7*64])
h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat,W_fc1) + b_fc1)


#Dropout减轻过拟合
keep_prob = tf.placeholder(tf.float32)
h_fc1_drop = tf.nn.dropout(h_fc1,keep_prob)

#将Dropout层的输出连接softmax层，得到最后的概率输出
W_fc2 = weight_variable([1024,10])
b_fc2 = bias_variable([10])
y_conv = tf.nn.softmax(tf.matmul(h_fc1_drop,W_fc2) + b_fc2)

#损失函数cross_entropy,优化器Adam
cross_entropy = tf.reduce_mean(-tf.reduce_sum(y_ * tf.log(y_conv),
                                              reduction_indices=[1]))
train_step = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy)
correct_prediction = tf.equal(tf.argmax(y_conv,1),tf.argmax(y_,1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction,tf.float32))

tf.global_variables_initializer().run()
for i in range(20000):  #20000次迭代训练
    batch = mnist.train.next_batch(50) #大小为50的batch
    if i%100 == 0:
        train_accuracy = accuracy.eval(feed_dict={x:batch[0],y_:batch[1],
                                                  keep_prob:1.0})
        print("step %d,training accuracy %g"%(i,train_accuracy))
    train_step.run(feed_dict={x:batch[0],y_:batch[1],keep_prob:0.5})

print("test accuracy %g"%accuracy.eval(feed_dict={x:mnist.test.images,
                                                   y_:mnist.test.labels,
                                                   keep_prob:1.0}))


