import os
import numpy as np
from pathlib import Path

from tensorflow.tensorboard.backend.event_processing.event_accumulator import EventAccumulator

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.figure import Figure


class Graphs:
    def __init__(self):
        p = Path(__file__).parents[2]

        path_train = os.path.join(p, 'Signature Resources and Data/retrain_logs/train')
        #path_train = "/tmp/retrain_logs/train"
        #path_train = "/home/pradeep/pythonProjects/Signature Resources and Data/retrain_logs/train"
        #path_validation = "/tmp/retrain_logs/validation"
        path_validation=os.path.join(p,'Signature Resources and Data/retrain_logs/validation')
        #path_validation = "/home/pradeep/pythonProjects/Signature Resources and Data/retrain_logs/validation"

        # Loading too much data is slow...
        tf_size_guidance = {
            'compressedHistograms': 10,
            'images': 0,
            'scalars': 100,
            'histograms': 1
        }

        self.event_t = EventAccumulator(path_train, tf_size_guidance)
        self.event_t.Reload()

        self.event_v = EventAccumulator(path_validation, tf_size_guidance)
        self.event_v.Reload()

    # For Accuracy
    def graph_of_accuracy(self):

        # Show all tags in the log file
        #print(self.event_t.Tags())
        #print(self.event_v.Tags())
        #print(self.event_v.Histograms('final_training_ops/biases/summaries/histogram'))

        training_accuracies =   self.event_t.Scalars('accuracy_1')

        validation_accuracies = self.event_v.Scalars('accuracy_1')

        steps = 100
        x = np.arange(steps)
        y = np.zeros([steps,2])

        for i in range(steps):
            y[i, 0] = training_accuracies[i][2]
            y[i, 1] = validation_accuracies[i][2]

        figure = Figure(figsize=(5, 5), dpi=100)

        a = figure.add_subplot(111)

        # plotting Accuracy graph
        a.plot(x, y[:, 0], label='Train')
        a.plot(x, y[:, 1], label='Validation')

        # a.set_xlabel("Steps")
        # a.set_ylabel("Accuracy")
        a.set_title("Accuracy")
        a.legend(loc='upper right', frameon=True)

        return figure

    # For Cross entropy
    def graph_of_cross_entropy(self):
        training_cross_entropy = self.event_t.Scalars('cross_entropy_1')
        # print(training_accuracies)
        validation_cross_entropy = self.event_v.Scalars('cross_entropy_1')

        steps = 100
        x = np.arange(steps)
        y = np.zeros([steps, 2])

        for i in range(steps):
            y[i, 0] = training_cross_entropy[i][2]  # value
            y[i, 1] = validation_cross_entropy[i][2]

        figure = Figure(figsize=(5, 5), dpi=100)

        a = figure.add_subplot(111)

        a.plot(x, y[:, 0], label='Train')
        a.plot(x, y[:, 1], label='Validation')

        a.set_title("Cross Entropy")
        a.legend(loc='upper right', frameon=True)

        return figure

    def graph_wt_mean(self):
        final_weight_summaries_mean_t = self.event_t.Scalars('final_training_ops/weights/summaries/mean')
        # print(training_accuracies)
        final_weight_summaries_mean_v = self.event_v.Scalars('final_training_ops/weights/summaries/mean')

        steps = 100
        x = np.arange(steps)
        y = np.zeros([steps, 2])

        for i in range(steps):
            y[i, 0] = final_weight_summaries_mean_t[i][2]  # value
            y[i, 1] = final_weight_summaries_mean_v[i][2]

        return x,y

    def graph_wt_max(self):
        final_weight_summaries_max_t = self.event_t.Scalars('final_training_ops/weights/summaries/max')
        # print(training_accuracies)
        final_weight_summaries_max_v = self.event_v.Scalars('final_training_ops/weights/summaries/max')

        steps = 100
        x = np.arange(steps)
        y = np.zeros([steps, 2])

        for i in range(steps):
            y[i, 0] = final_weight_summaries_max_t[i][2]  # value
            y[i, 1] = final_weight_summaries_max_v[i][2]

        return x,y

    def graph_wt_min(self):
        final_weight_summaries_min_t = self.event_t.Scalars('final_training_ops/weights/summaries/min')
        # print(training_accuracies)
        final_weight_summaries_min_v = self.event_v.Scalars('final_training_ops/weights/summaries/min')

        steps = 100
        x = np.arange(steps)
        y = np.zeros([steps, 2])

        for i in range(steps):
            y[i, 0] = final_weight_summaries_min_t[i][2]  # value
            y[i, 1] = final_weight_summaries_min_v[i][2]

        return x,y

    def graph_wt_stdev(self):
        final_weight_summaries_stdev_t = self.event_t.Scalars('final_training_ops/weights/summaries/stddev_1')
        # print(training_accuracies)
        final_weight_summaries_stdev_v = self.event_v.Scalars('final_training_ops/weights/summaries/stddev_1')

        steps = 100
        x = np.arange(steps)
        y = np.zeros([steps, 2])

        for i in range(steps):
            y[i, 0] = final_weight_summaries_stdev_t[i][2]  # value
            y[i, 1] = final_weight_summaries_stdev_v[i][2]

        return x,y

    def graph_bais_max(self):
        final_bais_summaries_max_t = self.event_t.Scalars('final_training_ops/biases/summaries/max')
        # print(training_accuracies)
        final_bais_summaries_max_v = self.event_v.Scalars('final_training_ops/biases/summaries/max')

        steps = 100
        x = np.arange(steps)
        y = np.zeros([steps, 2])

        for i in range(steps):
            y[i, 0] = final_bais_summaries_max_t[i][2]  # value
            y[i, 1] = final_bais_summaries_max_v[i][2]

        return x,y

    def graph_bais_min(self):
        final_bais_summaries_min_t = self.event_t.Scalars('final_training_ops/biases/summaries/min')
        # print(training_accuracies)
        final_bais_summaries_min_v = self.event_v.Scalars('final_training_ops/biases/summaries/min')

        steps = 100
        x = np.arange(steps)
        y = np.zeros([steps, 2])

        for i in range(steps):
            y[i, 0] = final_bais_summaries_min_t[i][2]  # value
            y[i, 1] = final_bais_summaries_min_v[i][2]

        return x,y


    def graph_bais_mean(self):
        final_bais_summaries_mean_t = self.event_t.Scalars('final_training_ops/biases/summaries/mean')
        # print(training_accuracies)
        final_bais_summaries_mean_v = self.event_v.Scalars('final_training_ops/biases/summaries/mean')

        steps = 100
        x = np.arange(steps)
        y = np.zeros([steps, 2])

        for i in range(steps):
            y[i, 0] = final_bais_summaries_mean_t[i][2]  # value
            y[i, 1] = final_bais_summaries_mean_v[i][2]

        return x,y

    def graph_bais_stdev(self):
        final_bais_summaries_stdev_t = self.event_t.Scalars('final_training_ops/biases/summaries/stddev_1')
        # print(training_accuracies)
        final_bais_summaries_stdev_v = self.event_v.Scalars('final_training_ops/biases/summaries/stddev_1')

        steps = 100
        x = np.arange(steps)
        y = np.zeros([steps, 2])

        for i in range(steps):
            y[i, 0] = final_bais_summaries_stdev_t[i][2]  # value
            y[i, 1] = final_bais_summaries_stdev_v[i][2]

        return x,y

    def graph_of_final_outputs(self):

        figure, axarr = plt.subplots(4, 2)
        #figure.suptitle('Final training outputs' )

        x, y = self.graph_bais_max()
        axarr[0, 0].plot(x, y)
        axarr[0, 0].set_title('final_training_ops/biases/summaries/max',fontsize=8)

        x, y = self.graph_bais_min()
        axarr[1, 0].plot(x, y)
        axarr[1, 0].set_title('final_training_ops/biases/summaries/min',fontsize=8)

        x, y = self.graph_bais_mean()
        axarr[ 2, 0].plot(x, y)
        axarr[ 2, 0].set_title('final_training_ops/biases/summaries/mean\n',fontsize=8)

        x, y = self.graph_bais_stdev()
        axarr[3, 0].plot(x, y)
        axarr[3, 0].set_title('final_training_ops/biases/summaries/stdev',fontsize=8)


        x, y = self.graph_wt_max()
        axarr[0, 1].plot(x, y)
        axarr[0, 1].set_title('final_training_ops/weights/summaries/max',fontsize=8)

        x, y = self.graph_wt_min()
        axarr[1, 1].plot(x, y)
        axarr[1, 1].set_title('final_training_ops/weights/summaries/min',fontsize=8)

        x, y = self.graph_wt_mean()
        axarr[2, 1].plot(x, y)
        axarr[2, 1].set_title('final_training_ops/weights/summaries/mean\n',fontsize=8)

        x, y = self.graph_wt_stdev()
        axarr[3, 1].plot(x, y)
        axarr[3, 1].set_title('final_training_ops/weights/summaries/stdev',fontsize=8)

        figure.subplots_adjust(wspace=0.6)
        figure.tight_layout()

        return figure

