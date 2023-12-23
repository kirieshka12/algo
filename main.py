from PIL import Image
from PIL import ImageFilter
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import os

app = QApplication([])
win = QWidget()
win.resize(1000,1000)


v1 = QVBoxLayout()
button_open = QPushButton('Папка')
v1.addWidget(button_open)
image_list = QListWidget()
v1.addWidget(image_list)


hor_dop = QHBoxLayout()
v2 = QVBoxLayout()
img = QLabel('Картинка')
v2.addWidget(img)
but_mir = QPushButton('Зеркало')
but_rez = QPushButton('Резкость')
but_left =  QPushButton('Лево')
but_right = QPushButton('Право')
but_bw = QPushButton('Чёрно-Белый')
hor_dop.addWidget(but_mir)
hor_dop.addWidget(but_rez)
hor_dop.addWidget(but_left)
hor_dop.addWidget(but_right)
hor_dop.addWidget(but_bw)

v2.addLayout(hor_dop)

hor_main = QHBoxLayout()
hor_main.addLayout(v1)
hor_main.addLayout(v2)
win.setLayout(hor_main)

def filter(fileList, formatList):
    result = []
    for file in fileList:
        for format in formatList:
            if file.endswith(format):
                result.append(file)
    return result

workdir = ''
def open_folder():
    global workdir
    workdir = QFileDialog.getExistingDirectory()


def show_folder():
    formatList = ['.jpg','.png','.jpeg','.gif','.bmp']
    open_folder()
    fileList = filter(os.listdir(workdir), formatList)
    image_list.clear()
    for file in fileList:
        image_list.addItem(file)



class ImageProc():
    def __init__(self):
        self.now_image = None
        self.name_file = None
        self.change_dir = '/changed'
    def loadImage(self, filename):
        self.name_file = filename
        image_path = os.path.join(workdir, filename)
        self.now_image = Image.open(image_path)

    def showImage(self,path):
        img.hide()
        pixmap = QPixmap(path)
        w, h =  img.width(), img.height()
        pixmap = pixmap.scaled(w, h, Qt.KeepAspectRatio)
        img.setPixmap(pixmap)
        img.show()

    def do_bw(self):
        bw_image = self.now_image.convert('L')
        bw_image.save('bw.jpg') #save
        image_path = os.path.join(workdir, 'bw.jpg')
        self.showImage(image_path)

workimage = ImageProc()

def showChosenImage():
    if image_list.currentRow() >=0:
        filename = image_list.currentItem().text()
        workimage.loadImage(filename)
        image_path = os.path.join(workdir, workimage.name_file)
        workimage.showImage(image_path)


image_list.currentRowChanged.connect(showChosenImage)
button_open.clicked.connect(show_folder)
but_bw.clicked.connect(workimage.do_bw)
win.show()
app.exec_()