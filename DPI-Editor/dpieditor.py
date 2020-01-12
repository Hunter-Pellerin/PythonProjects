from PIL import Image
import glob, os, sys

sourceFolderName = "source"
outputFolderName = "resized_imgs"

sizeMultiplier = 1 # change output resolution
outputDPI = 72

cwd = os.getcwd()
IMG_DIR= os.path.join(cwd, sourceFolderName)

def manageDirectory():
    try:
        os.chdir(outputFolderName)
    except:
        os.mkdir(outputFolderName)
        os.chdir(outputFolderName)

def changeDPI(directory):
    counter=0
    pathToNewFolder = os.path.join(cwd, outputFolderName)
    for img in glob.glob(directory+"/*.JPG"):
        workingImg = Image.open(img)
        x, y = workingImg.size
        im2 = workingImg.resize((int(x*sizeMultiplier), int(y*sizeMultiplier)), Image.BICUBIC)

        counter += 1
        os.chdir(pathToNewFolder)
        im2.save("resized_img{}.jpg".format(counter), dpi=(outputDPI,outputDPI))
        os.chdir(directory)

        showProgress(img)
    print("\nTotal Images: {}".format(counter))

def showProgress(image):
    sys.stdout.write('\r')
    sys.stdout.write("Image: {}".format(image))
    sys.stdout.flush()

if __name__ == "__main__":
    manageDirectory()
    changeDPI(IMG_DIR)