import base
import tensorflow as tf

class advisor :
    def get_all_possble(self, blc, map) :
        result = ()
        for i in range(X_MAX) :
            result.append(base.fall_block_straight())


Node = base.X_VISUAL_MAX * base.Y_VISUAL_MAX
NodeX = base.X_VISUAL_MAX
NodeY = base.Y_VISUAL_MAX

def weight_variable(shape) :
    initial = tf.truncated_normal(shape, stddev = 0.1)
    return tf.Variable(initial)

BlockShape = 5

x = tf.placeholder(tf.flaot32, shape=[Node])
y_ = tf.placeholder(tf.flaot32, shape=[NodeX])

Weight =  weight_variable([])
Bias = tf.Varialble(tf.zeros[Node,BlockShape,NodeX])

initRate = tf.matmul((x, Weight) + Bias)

Kernel = weight_variable([3,3])
ConvMap = tf.nn.conv2d(initRate, Kernel, strides=[1, 1, 1, 1], padding='SAME')

print(ConvMap)
