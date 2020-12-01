import numpy as np
import random
import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()
from load_data import DataGenerator
from tensorflow.python.platform import flags
from tensorboardX import SummaryWriter
import time

FLAGS = flags.FLAGS

flags.DEFINE_integer(
    'num_classes', 5, 'number of classes used in classification (e.g. 5-way classification).')

flags.DEFINE_integer('num_samples', 1,
                     'number of examples used for inner gradient update (K for K-shot learning).')

flags.DEFINE_integer('meta_batch_size', 16,
                     'Number of N-way classification tasks per batch')

dir= "logs/TensorBoard/"
dir+= "MANN_" + str(FLAGS.num_classes)+ ", "+ str(FLAGS.num_samples)+ "_"+ time.strftime("%d-%m-%Y_%H-%M-%S")
summary_writer = SummaryWriter(dir)

def loss_function(preds, labels):
    """
    Computes MANN loss
    Args:
        preds: [B, K+1, N, N] network output
        labels: [B, K+1, N, N] labels
    Returns:
        scalar loss
    """
    #############################
    #### YOUR CODE GOES HERE ####

    cce= tf.keras.losses.CategoricalCrossentropy(from_logits= True)
    #loss= cce(labels, preds)
    #print(labels[:, -1, :, :], preds[:, -1, :, :])
    #loss = cce(labels[:, -1, :, :], preds[:, -1, :, :])
    loss= tf.losses.softmax_cross_entropy(labels[:, -1, :, :], preds[:, -1, :, :])

    return loss
    #############################


class MANN(tf.keras.Model):

    def __init__(self, num_classes, samples_per_class):
        super(MANN, self).__init__()
        self.num_classes = num_classes
        self.samples_per_class= samples_per_class
        self.layer1 = tf.keras.layers.CuDNNLSTM(128, return_sequences=True)
        self.relu1 = tf.keras.layers.ReLU()
        self.batch1= tf.keras.layers.TimeDistributed(tf.keras.layers.BatchNormalization())
        self.layer2 = tf.keras.layers.CuDNNLSTM(64, return_sequences=True)
        self.relu2= tf.keras.layers.ReLU()
        self.dense1 = tf.keras.layers.TimeDistributed(tf.keras.layers.Dense(self.num_classes))

    def call(self, input_images, input_labels):
        """
        MANN
        Args:
            input_images: [B, K+1, N, 784] flattened images
            labels: [B, K+1, N, N] ground truth labels
        Returns:
            [B, K+1, N, N] predictions
        """
        #############################
        #### YOUR CODE GOES HERE ####

        B, K, N, _= input_images.shape
        print(K)

        K= K-1

        x_reshaped= tf.reshape(input_images, [-1, (K+1)*N, 784])
        y_zeroed= tf.concat((input_labels[:, :-1, :, :], tf.zeros_like(input_labels[:, -1, :, :][:, tf.newaxis])), axis= 1)
        y_reshaped= tf.reshape(y_zeroed, [-1, (K+1)*N, N])

        input_to = tf.concat((x_reshaped, y_reshaped), axis= 2)
        out= self.layer1(input_to)
        out= self.relu1(out)
        out = self.batch1(out)
        out= self.layer2(out)
        out= self.relu2(out)
        out= self.dense1(out)

        out= tf.reshape(out, [-1, K+1, N, N])

        #############################
        return out


ims = tf.placeholder(tf.float32, shape=(
    None, FLAGS.num_samples + 1, FLAGS.num_classes, 784))
labels = tf.placeholder(tf.float32, shape=(
    None, FLAGS.num_samples + 1, FLAGS.num_classes, FLAGS.num_classes))

data_generator = DataGenerator(
    FLAGS.num_classes, FLAGS.num_samples + 1)

o = MANN(FLAGS.num_classes, FLAGS.num_samples + 1)
out = o(ims, labels)

loss = loss_function(out, labels)
optim = tf.train.AdamOptimizer(0.001)
optimizer_step = optim.minimize(loss)

with tf.Session() as sess:
    sess.run(tf.local_variables_initializer())
    sess.run(tf.global_variables_initializer())

    for step in range(50000):
        i, l = data_generator.sample_batch('train', FLAGS.meta_batch_size)
        feed = {ims: i.astype(np.float32), labels: l.astype(np.float32)}
        _, ls = sess.run([optimizer_step, loss], feed)

        if step % 100 == 0:
            print("*" * 5 + "Iter " + str(step) + "*" * 5)
            i, l = data_generator.sample_batch('test', 100)
            feed = {ims: i.astype(np.float32),
                    labels: l.astype(np.float32)}
            pred, tls = sess.run([out, loss], feed)
            print("Train Loss:", ls, "Test Loss:", tls)

            summary_writer.add_scalar("Train loss", ls, step)
            summary_writer.add_scalar("Test loss", tls, step)

            pred = pred.reshape(
                -1, FLAGS.num_samples + 1,
                FLAGS.num_classes, FLAGS.num_classes)
            l = l[:, -1, :, :].argmax(2)
            print(pred[:, -1, :, :])
            pred = pred[:, -1, :, :].argmax(2)
            #print(pred, l)
            #print(type((1.0 * (pred == l))))

            Acc= (1.0 * (pred == l)).mean()

            print("Test Accuracy", Acc)
            summary_writer.add_scalar("Test Accuracy", Acc, step)
