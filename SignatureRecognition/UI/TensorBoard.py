import subprocess
import threading
import os
from pathlib import Path

class TensorBoard(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.proc = None

    def run(self):
        print('thread reached!')

        p = Path(__file__).parents[2]
        # print(p)
        path=os.path.join(p, 'Signature Resources and Data/retrain_logs')

        self.proc = subprocess.Popen(['python', '-m', 'tensorflow.tensorboard', '--logdir=' + path],
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        for line in self.proc.stdout:
            link = line.decode("utf8")
            print(link)

        #os.system('python -m tensorflow.tensorboard --logdir=' + path)

    def stop(self):
        print("Trying to stop thread ")
        if self.proc is not None:
            self.proc.terminate()
            self.proc = None

        print("thread terminated")


    def islive(self):
        if(self.proc is None):
            return True
