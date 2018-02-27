import tensorflow as tf
import numpy as np
import base as tetris

def get_all_possble(self, blc, map) :
    result = ()
    for i in range(X_MAX) :
        result.append(base.fall_block_straight())

NodeX = 10
NodeY = 23
Form = 11

X_ = tf.placeholder("float",[NodeY, NodeX])
Y_ = tf.placeholder("float",[NodeY, NodeX])

sess = tf.Session()

Map = np.array(np.zeros(shape=[3,NodeY,NodeX,1], dtype=np.float32))
MapReshaped = Map[0].reshape([NodeY, NodeX])

def rmove(mapp, plist) :
    for i in plist :
        mapp[i[0]][i[1]] = 1


class Actor :
    cost = None
    denseUnit = NodeX

    def __init__ (self):
        self.fullMap = tf.Variable(tf.ones_like(Map, dtype=tf.float32))
        self.inMap = tf.placeholder("float", [3, NodeY, NodeX,1] )
        self.mapWeight = tf.Variable(tf.random_normal([3,NodeY,NodeX,1], stddev=0.5, dtype=tf.float32))
        self.Bias = tf.Variable(tf.ones([3,NodeY,NodeX,1], dtype=tf.float32))
        self.convWeight = tf.Variable(tf.random_normal([3,3,1,1], stddev=0.5, dtype=tf.float32))
        self.convhMap = tf.Variable(tf.zeros([3,NodeY,NodeX,1], dtype=tf.float32))

        self.verticalWeight = tf.Variable(tf.random_normal([ NodeY, 1, 1, Form]))
        self.denseWeight = tf.Variable(tf.random_normal([NodeX, NodeY*NodeX], stddev=0.5, dtype=tf.float32))
        self.build_ops()

    def step(self,blc) :
        MapReshaped = Map.reshape([NodeY,NodeX])
        plist = tetris.find_all_possible_pos_by_idx(blc, MapReshaped, NodeY)

    def make_kernel(self,count) :
        return [ tf.Variable(tf.random_normal([1,NodeY, NodeX, 1], stddev=0.5, dtype=tf.float32)) for x in range(0, count) ]

    def build_ops(self) :
        init = tf.global_variables_initializer()
        sess.run(init)

        ops = tf.multiply(self.inMap, self.mapWeight) + self.Bias
        ops = tf.nn.conv2d(ops, self.convWeight, strides=[1,1,1,1], padding="SAME")
        ops = tf.tanh(ops)

        ops = tf.nn.conv2d(ops, self.verticalWeight, strides=[1,1,1,1], padding="VALID")
        cost = tf.reduce_sum(ops,3)
        optimizer = tf.train.GradientDescentOptimizer(1)
        train_op = optimizer.minimize(cost)

        sess.run(cost, feed_dict={self.inMap:Map})
        bval = tf.identity(cost)
        for i in range(0, 10000) :
            sess.run(train_op, feed_dict={self.inMap:Map})
        aval = cost

        update = aval - bval

        print(sess.run(update, feed_dict={self.inMap:Map}))

if __name__ == "__main__" :
    advInst = Actor()
