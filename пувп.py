import sys
from PIL import Image
from PIL.ImageQt import ImageQt
from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import datetime
import csv

SIZE = 0
h = 100
w = 100
type_file = ''
file_name = ''
flag_for_square = False
flag_for_triangle = False
flag_for_round = False
EVENTLOG = []
penwidth = 10
textfortcrop = (0, 0, h, w)
f = False
rasmer = 50
trues = False


class miniPhotoshop(QMainWindow):
    def __init__(self):
        super(miniPhotoshop, self).__init__()
        self.dialog = None
        self.dwnld = None
        self.instruction = None
        uic.loadUi('Draw_and_change_window.ui', self)
        self.setWindowTitle('Draw_and_change_v01')
        self.createbtn_2.clicked.connect(self.create_)
        self.dwnld.clicked.connect(self.dwnld_)
        self.instruct_but.clicked.connect(self.instruct)
        self.logbtn.clicked.connect(self.log)

    def create_(self):
        global trues
        self.dialog = ClssCreater()
        self.dialog.show()
        if trues:
            self.current_log()
            self.update()
            trues = False

    def dwnld_(self):
        self.dwnld = ClssDwnld()
        self.dwnld.show()

    def instruct(self):
        self.instruction = ClssInstruct()
        self.instruction.show()

    def log(self):
        self.log = LogCreater()
        self.log.show()

    def current_log(self):
        self.listWidget.addItem("".join(list(map(lambda x: '\n' + str(x), EVENTLOG))))
        self.update()


class ClssCreater(QDialog):
    def __init__(self):
        super(ClssCreater, self).__init__()
        self.Drawer = None
        uic.loadUi('creater.ui', self)
        self.setWindowTitle('Create_the_picture')
        self.btncreation.clicked.connect(self.getthis)

    def getthis(self):
        global h
        global w
        global file_name
        global type
        global EVENTLOG
        h = int(self.height_b.text())
        w = int(self.width_b.text())
        file_name = self.lineEdit.text()
        type = self.comboBox.currentText()
        EVENTLOG += [[f'{datetime.datetime.now()}', f'|был успешно создан файл {file_name}.{type}|', ]]
        self.Drawer = Drawerd()
        self.Drawer.show()


class Drawerd(QDialog):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.pen_width_getter = None
        self.curr_image = None
        self.directionclss = None
        self.setAttribute(Qt.WA_StaticContents)
        self.h = h
        self.w = w
        self.myPenColor = Qt.black
        self.myPenWidth = 10
        uic.loadUi('Picture.ui', self)
        self.setWindowTitle('Draw_your_picture')
        self.button_for_pen_color.clicked.connect(self.set_color)
        self.figure_Chooser.clicked.connect(self.get_figure)
        self.button_for_width.clicked.connect(self.set_pen_width)
        self.imagesaver.clicked.connect(self.savefunc)
        self.savefunc()
        self.image = QImage(self.h, self.w, QImage.Format_RGB32)
        self.im = Image.new("RGB", (500, 500), (255, 255, 255))
        self.im.save(f"{file_name}.{type}")
        self.path = QPainterPath()
        self.clearImage()

    def clearImage(self):
        self.path = QPainterPath()
        self.image.fill(Qt.white)
        self.update()

    def saveImage(self, fileName, fileFormat):
        self.image.save(fileName, fileFormat)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawImage(event.rect(), self.image, self.rect())

    def mousePressEvent(self, event):
        self.path.moveTo(event.pos())
        global flag_for_square
        global flag_for_triangle
        global flag_for_round
        self.path.lineTo(event.pos())
        p = QPainter(self.image)
        p.setPen(QPen(self.myPenColor,
                      self.myPenWidth, Qt.SolidLine, Qt.RoundCap,
                      Qt.RoundJoin))
        if flag_for_round:
            p.drawEllipse(event.x(), event.y(), rasmer, rasmer)
            flag_for_round = False
            p.drawPath(self.path)
            p.end()
            self.save_image_k(f"{file_name}.{type}", f"{type.upper()}")
            self.update()
        if flag_for_square:
            p.drawRect(event.x(), event.y(), rasmer, rasmer)
            flag_for_square = False
            p.drawPath(self.path)
            p.end()
            self.save_image_k(f"{file_name}.{type}", f"{type.upper()}")
            self.update()
        if flag_for_triangle:
            self.path.moveTo(event.x() - rasmer, event.y())
            self.path.lineTo(event.x(), event.y() + rasmer)
            self.path.lineTo(event.x() + rasmer, event.y())
            self.path.lineTo(event.x() - rasmer, event.y())
            p.drawPath(self.path)
            flag_for_triangle = False
            p.drawPath(self.path)
            p.end()
            self.save_image_k(f"{file_name}.{type}", f"{type.upper()}")
            self.update()

    def set_color(self):
        self.path = QPainterPath()
        self.image.fill(Qt.white)
        self.curr_image = Image.open(f'{file_name}.{type}')
        self.image = ImageQt(self.curr_image)
        self.myPenColor = QColorDialog.getColor()

    def mouseMoveEvent(self, event):
        self.path.lineTo(event.pos())
        p = QPainter(self.image)
        p.setPen(QPen(self.myPenColor,
                      penwidth, Qt.SolidLine, Qt.RoundCap,
                      Qt.RoundJoin))
        p.drawPath(self.path)
        p.end()
        self.save_image_k(f"{file_name}.{type}", f"{type.upper()}")
        self.update()

    def clearImage(self):
        self.path = QPainterPath()
        self.image.fill(Qt.white)
        self.update()

    def set_pen_width(self):
        global penwidth
        self.pen_width_getter = PenWidthClss()
        self.pen_width_getter.show()
        self.image.fill(Qt.white)
        self.curr_image = Image.open(f'{file_name}.{type}')
        self.image = ImageQt(self.curr_image)

    def save_image_k(self, fileName, fileFormat):
        self.image.save(fileName, fileFormat)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawImage(event.rect(), self.image, self.rect())

    def get_figure(self):
        self.figure_chooser = ClssFigureChooser()
        self.figure_chooser.show()

    def savefunc(self):
        self.directionclss = ClssToDirect()
        self.directionclss.show()


class ClssToDirect(QDialog):
    def __init__(self):
        super(ClssToDirect, self).__init__()
        self.image = None
        uic.loadUi('saverrr.ui', self)
        self.setWindowTitle('Choose_the_direction')
        self.pushButton123.clicked.connect(self.saving)
        self.pusherloc.clicked.connect(self.loc)
        self.lineEdit.setText(f'C:\{file_name}.{type}')

    def saving(self):
        self.pather = self.lineEdit.text()
        self.curr_image = Image.open(f'{file_name}.{type}')
        self.image = ImageQt(self.curr_image)
        self.image.save(f"{self.pather}", f"{type.upper()}")

    def loc(self):
        self.pather = \
            QFileDialog.getSaveFileName(self, 'Выберите куда',
                                        '',
                                        'Картинки (*.jpg)')[0]
        self.lineEdit.setText(self.pather)


class ClssDwnld(QDialog):
    def __init__(self):
        super(ClssDwnld, self).__init__()
        self.location = None
        self.croppingclass = None
        self.flag = 0
        uic.loadUi('dwnldproject.ui', self)
        self.setWindowTitle('Change_your_file')
        self.app = app
        self.filename = QFileDialog.getOpenFileName(self, 'Выберите картинку', '', 'Картинки (*.jpg)')[0]
        self.orig_image = Image.open(self.filename)
        self.curr_image = Image.open(self.filename)
        self.degree = 0
        self.a = ImageQt(self.curr_image)
        self.pixmap = QPixmap.fromImage(self.a)
        self.image123.setPixmap(self.pixmap)
        self.change_color.clicked.connect(self.set_channel)
        self.change_color.clicked.connect(self.rotate)
        self.buttonsave.clicked.connect(self.savve)
        self.buttoncrop.clicked.connect(self.cropping)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_R:
            self.flag = 1
        elif event.key() == Qt.Key_G:
            self.flag = 2
        elif event.key() == Qt.Key_B:
            self.flag = 3
        elif event.key() == Qt.Key_N:
            self.flag = 4
        elif event.key() == Qt.Key_P:
            self.flag = 5

    def set_channel(self):
        global EVENTLOG
        self.curr_image = self.orig_image.copy()
        pixels = self.curr_image.load()
        x, y = self.curr_image.size
        for i in range(x):
            for j in range(y):
                r, g, b = pixels[i, j]
                if self.flag == 1:
                    pixels[i, j] = r, 0, 0
                if self.flag == 2:
                    pixels[i, j] = 0, g, 0
                if self.flag == 3:
                    pixels[i, j] = 0, 0, b
                if self.flag == 4:
                    pixels[i, j] = 255 - r, 255 - g, 255 - b
                if self.flag == 5:
                    pixels[i, j] = r, g, b
        self.curr_image = self.curr_image.rotate(self.degree, expand=True)
        if f:
            self.curr_image = self.curr_image.crop(textfortcrop)
        self.a = ImageQt(self.curr_image)
        self.pixmap = QPixmap.fromImage(self.a)
        self.image123.setPixmap(self.pixmap)
        EVENTLOG += [[f'{datetime.datetime.now()}', '|произошли изменения цветовой гаммы картинки|']]

    def rotate(self):
        global EVENTLOG
        self.degree += int(self.comboBox.currentText())
        degree = 90
        self.degree %= 360
        self.curr_image = self.curr_image.rotate(degree, expand=True)
        self.a = ImageQt(self.curr_image)
        self.pixmap = QPixmap.fromImage(self.a)
        self.image123.setPixmap(self.pixmap)
        EVENTLOG += [[f'{datetime.datetime.now()}', f'градус поворота изменился на {self.degree}']]

    def except_hook(clc, exception, traseback):
        sys.__excepthook__(clc, exception, traseback)

    def savve(self):
        global EVENTLOG
        self.location = \
            QFileDialog.getSaveFileName(self, 'Выберите куда',
                                        '',
                                        'Картинки (*.jpg)')[0]

        self.curr_image.save(f"{self.location}", "JPEG")
        EVENTLOG += [[f'{datetime.datetime.now()}', f'|обьект успешно сохранен в директории {self.location}|']]
        self.close()

    def cropping(self):
        self.croppingclass = ClssCropping()
        self.croppingclass.show()
        if f:
            print(1)
            self.curr_image = self.curr_image.crop(textfortcrop)
            self.a = ImageQt(self.curr_image)
            self.pixmap = QPixmap.fromImage(self.a)
            self.image123.setPixmap(self.pixmap)


class ClssCropping(QDialog):
    def __init__(self):
        super(ClssCropping, self).__init__()
        uic.loadUi('cropper.ui', self)
        self.setWindowTitle('Crop_the_picture')
        self.btnok.clicked.connect(self.croppls)

    def croppls(self):
        global f
        global textfortcrop
        textfortcrop = tuple(map(lambda x: int(x), str(self.lineEdit.text() + ',' + self.lineEdit_2.text()).split(',')))
        f = True
        self.close()


class ClssInstruct(QDialog):
    def __init__(self):
        super(ClssInstruct, self).__init__()
        uic.loadUi('instr.ui', self)
        self.setWindowTitle('Instruction')
        self.btndwnldinstruct.clicked.connect(self.dwnld)

    def dwnld(self):
        global EVENTLOG
        self.pather = \
            QFileDialog.getSaveFileName(self, 'Выберите куда',
                                        '',
                                        'readme файл (*.txt)')[0]
        with open(f'{self.pather}', 'w+', encoding="utf8") as f:
            f.write('Дорогой пользователь прости , но я не уверен что смогу тебе помочь т.к здесь все предельно просто.\n'
                    'Соблюдай простые правила:\n'
                    '1.Когда создаешь файл, не пиши буквы в окна для высоты и ширины(это также касается изменения файла в отделе "Обрезать".\n'
                    '2.Когда прописываешь путь удостоверься , что все написано правильно.\n'
                    '3.Когда изменяешь файл кнопка N на клавиатуре "вернуть все" вернет обратно ТОЛЬКО ЦВЕТ, который был изначально. Все остальные действия будут неизменны.\n'
                    'Удачного использования!')
        EVENTLOG += [[f'{datetime.datetime.now()}', 'загружен readme.txt файл']]
        self.close()


class ClssFigureChooser(QDialog):
    def __init__(self):
        super(ClssFigureChooser, self).__init__()
        uic.loadUi('figure_chooser.ui', self)
        self.setWindowTitle('Choose_your_figure')
        self.OKman.clicked.connect(self.da)

    def da(self):
        global flag_for_square
        global flag_for_triangle
        global flag_for_round
        global EVENTLOG
        global rasmer
        global trues
        if self.figure.currentText() == 'Треугольник':
            flag_for_triangle = True
            EVENTLOG += [[f'{datetime.datetime.now()}', '|была выбрана фигура треугольник|']]
        elif self.figure.currentText() == 'Кружочек':
            flag_for_round = True
            EVENTLOG += [[f'{datetime.datetime.now()}', '|была выбрана фигура кружочек|']]
        elif self.figure.currentText() == 'Квадрат':
            flag_for_square = True
            EVENTLOG += [[f'{datetime.datetime.now()}', '|была выбрана фигура квадрат|', ]]
        trues = True
        rasmer = int(self.lineEdit.text())
        self.close()


class LogCreater(QDialog):
    def __init__(self):
        super(LogCreater, self).__init__()
        self.where = None
        uic.loadUi('location_chooser.ui', self)
        self.setWindowTitle('Choose_the_location')
        self.btn.clicked.connect(self.yescreate)
        self.way.clicked.connect(self.wayf)
        self.lineEdit.setText('C:\log.csv')

    def yescreate(self):
        print(EVENTLOG)
        new_file = open(f"{self.where}", 'w')
        new_file.close()
        with open(f"{self.where}", "w", encoding='UTF8') as csvfile:
            writer = csv.writer(csvfile, delimiter='l', quotechar='l')
            for r in EVENTLOG:
                writer.writerow(r)
        self.close()

    def wayf(self):
        self.where = QFileDialog.getSaveFileName(self, 'Выберите куда', '', 'CSV отчёт (*.csv)')[0]
        self.lineEdit.setText(self.where)


class PenWidthClss(QDialog):
    def __init__(self):
        super(PenWidthClss, self).__init__()
        uic.loadUi('choosing_the_width.ui', self)
        self.setWindowTitle('Choose_pen_width')
        self.widebtn_2.clicked.connect(self.geetwid)

    def geetwid(self):
        global penwidth
        penwidth = int(self.widthline.text())
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mp = miniPhotoshop()
    mp.show()
    sys.exit(app.exec())
