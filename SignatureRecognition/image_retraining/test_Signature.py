import os
from pathlib import Path
import numpy as np
import tensorflow as tf

class TestSignature:
    def __init__(self,imagePath=''):

        self.imagePath=imagePath
        p = Path(__file__).parents[2]

        self.modelFullPath = os.path.join(p, 'Signature Resources and Data/Train_resource/output_signature/output_graph.pb')

        self.labelsFullPath =os.path.join(p, 'Signature Resources and Data/Train_resource/Label_signature/labels.txt')
    def create_graph(self):
        """Creates a graph from saved GraphDef file and returns a saver."""
        # Creates graph from saved graph_def.pb.
        with tf.gfile.FastGFile(self.modelFullPath, 'rb') as f:
            graph_def = tf.GraphDef()
            graph_def.ParseFromString(f.read())
            _ = tf.import_graph_def(graph_def, name='')

    def run_inference_on_image(self):
        answer = None

        if not tf.gfile.Exists(self.imagePath):
            tf.logging.fatal('File does not exist %s', self.imagePath)
            return answer

        image_data = tf.gfile.FastGFile(self.imagePath, 'rb').read()

        # Creates graph from saved GraphDef.
        self.create_graph()

        with tf.Session() as sess:

            softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')
            predictions = sess.run(softmax_tensor,
                                   {'DecodeJpeg/contents:0': image_data})
            predictions = np.squeeze(predictions)

            top_k = predictions.argsort()[-5:][::-1]  # Getting top 5 predictions
            f = open(self.labelsFullPath, 'r')
            lines = f.readlines()
            #labels = [str(w).replace("\n", "") for w in lines]
            labels = [str(w).strip() for w in lines]

            for node_id in top_k:
                human_string = labels[node_id]
                score = predictions[node_id]
                #print('%s (score = %.5f)' % (human_string, score))

            answer = labels[top_k[0]]

            return predictions,top_k,labels


def main():
    o=TestSignature()
    o.run_inference_on_image()

if __name__ == '__main__':
    main()