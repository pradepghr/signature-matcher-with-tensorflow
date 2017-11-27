import os
import glob
from PIL import Image
from random import randint
from pathlib import Path

class CreateClassDir:

    def __init__(self,Dir,className):
        self.className=className
        self.Dir=Dir
        p = Path(__file__).parents[2]
        # print(p)
        path = os.path.join(p, 'Signature Resources and Data/Data/DataSets/Training_Sets/{}/file'.format(self.className))
        self.Destination=path

        self.directory = os.path.dirname(self.Destination)
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)


    def make_class(self):

        imageList = os.listdir(self.Dir)
        if (len(imageList) == 0 ):
            print("Zero files")
            raise FileNotFoundError
        count=0
        for img in imageList:
            file = os.path.join(self.Dir,img)
            img = Image.open(file)
            #print(img.format)
            if (img.format == "JPEG" ):
                count+=1
                #print(count)
                #im = Image.open(self.Dir+'/'+img)
                #print(im)
                #Converting to grayscale
                img_grayscale = img.convert('1')
                #print(img_grayscale)
                #Resize to 299 * 299
                #img_resized=img_grayscale.resize(299 * 299)
                #print(img_resized)
                #img_grayscale.save(self.Destination+"/"+"{}-{}.jpg".format(self.className,randint(100,200)))
                img_grayscale.save("{}/{}-{}".format(self.directory,self.className,randint(100,200)), 'JPEG')

        if( count == 0 ):
            raise FileNotFoundError

        print("Class {} Created.".format(self.className))
        return