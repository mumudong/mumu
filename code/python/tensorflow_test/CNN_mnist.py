import tensorflow as tf
from mnist import read_data_sets

mnist = read_data_sets("MNIST_data/",one_hot=True)
sess = tf.InteractiveSession()

def weight_variable(shape):
    # 使用截断的正态分布给权重制造一些随机噪声来打破完全对称
    initial = tf.truncated_normal(shape,stddev=0.1)
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
  padding代表边界的处理方式，same代表给边界加上padding让卷积的输出和输入保持同样的尺寸
"""
def conv2d(x,W):
    return tf.nn.conv2d(x,W,strides=[1,1,1,1],padding='SAME')
"""
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


