import pickle
import tensorflow as tf
from random import shuffle
from matplotlib import pyplot as plt
import os
from tqdm import tqdm
flatten = lambda l: [item for sublist in l for item in sublist]

batch = 10
x_data = pickle.load(open("x_wins_clean.p","rb"))
y_data = pickle.load(open("y_wins_clean.p","rb"))

data = [(x,0) for x in x_data] + [(x,1) for x in y_data]
shuffle(data)

q = [x[0] for x in data]



a = [[x[1]] for x in data]


trQ = q[:int(len(q)*0.8)]
trA = a[:int(len(a)*0.8)]

trTQ = q[int(len(q)*0.8):int(len(q)*1)]
trTA = a[int(len(a)*0.8):int(len(a)*1)]

x = tf.placeholder(dtype=tf.float32, shape=[None, 65])
y = tf.placeholder(dtype=tf.float32, shape=[None, 1])


def net(data):
    hidden_l1 = {"w": tf.Variable(tf.random_normal([65, 100])), "b": tf.Variable(tf.random_normal([100]))}
    hidden_l2 = {"w": tf.Variable(tf.random_normal([100, 100])), "b": tf.Variable(tf.random_normal([100]))}
    output_l = {"w": tf.Variable(tf.random_normal([100, 1])), "b": tf.Variable(tf.random_normal([1]))}

    l1 = tf.nn.sigmoid(tf.matmul(data, hidden_l1["w"]) + hidden_l1["b"])
    l2 = tf.nn.sigmoid(tf.matmul(l1, hidden_l2["w"]) + hidden_l2["b"])
    out = tf.nn.sigmoid(tf.matmul(l2, output_l["w"]) + output_l["b"])

    return out


def train_net(x, y):
    global trA,trQ
    predict = net(x)
    cost = tf.losses.mean_squared_error(predict, y)
    optimizer = tf.train.AdamOptimizer().minimize(cost)

    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        saver = tf.train.Saver()
        testE = []
        trainE = []
        for epoch in range(50):
            c = list(zip(trQ, trA))

            shuffle(c)

            trQ, trA = zip(*c)
            for bt in range(int(len(trQ) / batch)):
                bq = trQ[bt * batch:bt * batch + batch]
                ba = trA[bt * batch:bt * batch + batch]
                _, c = sess.run([optimizer, cost], feed_dict={x: bq, y: ba})
            # print(epoch, c)
            if epoch % 1 == 0:
                loss = tf.losses.absolute_difference(predict, y)
                loss = sess.run([loss], feed_dict={x: trQ, y: trA})
                trainE.append(loss)
                loss = tf.losses.absolute_difference(predict, y)
                loss = sess.run([loss], feed_dict={x: trTQ, y: trTA})
                testE.append(loss)
                print(epoch,trainE[-1],testE[-1])

        p = sess.run([predict], feed_dict={x: trTQ, y: trTA})

        #p[0][x] = [p[0][x][0]]+[(round(p[0][x][y-1])+p[0][x][y]+round(p[0][x][y+1]))/3 for y in range(1,len(p[0][x])-1)]+[p[0][x][-1]]
        a = sum([1 for n in range(len(p[0])) if ((p[0][n]<=0.5 and trTA[n][0] == 0) or (p[0][n] > 0.5 and trTA[n][0] == 1))])
        print(a/p[0].shape[0]*100,'%')

        saver.save(sess, os.path.join(os.getcwd(),"trained_models/NN3.ckpt"))

    plt.plot(testE[1:])
    plt.plot(trainE[1:])
    plt.show()



train_net(x, y)

