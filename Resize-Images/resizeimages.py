import glob, os, sys
from PIL import Image

# ## ## # CONFIG # ## ## #
sourceFolderName = "source"
outputFolderName = "resized_imgs"

outputSize = (256, 256)
# ## # ## # ## # ## # ## #

cwd = os.getcwd()
IMG_DIR= os.path.join(cwd, sourceFolderName)

def manageDirectory():
    try:
        os.chdir(outputFolderName)
    except:
        os.mkdir(outputFolderName)
        os.chdir(outputFolderName)

def resizeImages(directory):
    pathToNewFolder = os.path.join(cwd, outputFolderName)
    counter=0
    for img in glob.glob(directory+"/*.JPG"):
        im1 = Image.open(img) 
        im1 = im1.resize(outputSize)

        counter += 1
        os.chdir(pathToNewFolder)
        im1.save('img{}.jpg'.format(counter))
        os.chdir(directory)

        showProgress(img)
    print("\nTotal Images: {}".format(counter))

def showProgress(image):
    sys.stdout.write('\r')
    sys.stdout.write("Image: {}".format(image))
    sys.stdout.flush()

if __name__ == "__main__":
    manageDirectory()
    resizeImages(IMG_DIR)
