import sys
import random
from PySide2 import QtCore, QtWidgets, QtGui
import numpy as np
import math
import xml.etree.ElementTree as et
import os

def read_xml(filename="przykladowy.xml",main=object):
    tree = et.parse(filename)
    root = tree.getroot()

    size=root.attrib["board_size"]

    main.change_size(size,xml=True)

    for child in root:
        # if child.attrib["nr"]==1:
            for leaf in child:
                if leaf.tag=="spawn_value":
                    x=int(leaf.attrib["x"][:-1])
                    y=int(leaf.attrib["y"])
                    value=int(leaf.text[:-1])
                    spawn = main.tic_tac_toe.spawnTile(x,y,value)
                    print(spawn)
                # print(leaf.tag, leaf.attrib, leaf.text)

# funkcja edytująca nam xml
def create_xml(filename="przykladowy.xml",size=3,history=[]):
    # tree = et.parse('./spam/dict.xml')
    root = et.Element("hex2048",{"board_size":str(size)})#.getroot()

    player1=et.Element("player",{"nr":"1"})
    root.append(player1)

    player2=et.Element("player",{"nr":"2"})
    root.append(player2)

    for el in history:
        if el[0]=="Spawned":
            tmp=et.SubElement(player1,"spawn_value",{"x":str(el[6]),"y":str(el[7])})
            tmp.text=str(el[4])
        if el[0]=="Move":
            tmp=et.SubElement(player1,"move")
            tmp.text = str(el[-1])
        if el[0]=="Score":
            tmp = et.SubElement(player1, "score")
            tmp.text = str(el[-1])
    # if filename[:-4]!=".xml":
    #     output=filename+".xml"
    # else:
    output=filename
    tree = et.ElementTree(root)
    tree.write(output, xml_declaration=True, encoding='utf-8')
    # # wpisujemy wszystkie prawdopodobienstwa ham, do elementów drzewa
    # for el in ham_probab:
    #     data = et.Element("word", {"type": "ham", "probability": str(round(ham_probab[el],4))})
    #     data.text = str(el)
    #     root.append(data)
    #  # wpisujemy wszystkie prawdopodobienstwa spam, do elementów drzewa
    # for el in spam_probab:
    #     data = et.Element("word", {"type": "spam", "probability": str(round(spam_probab[el],4))})
    #     data.text = str(el)
    #     root.append(data)
    # #     zappisujemy plik
    # tree.write('output.xml', xml_declaration=True, encoding='utf-8')

def printRed(text):
    print("\033[91m {}\033[00m".format(text))


def printGreen(text):
    print("\033[92m {}\033[00m".format(text))


class Hexagon(QtWidgets.QGraphicsItem):
    def __init__(self, x=0, y=0, z=0, x_start=250, y_start=150):
        super().__init__()
        self.size = 30
        self.x_center = x_start
        self.y_center = y_start
        self.x = x
        self.y = y
        self.z = z
        self.value = 0

    def boundingRect(self):
        return QtCore.QRectF(0, 0, 1200, 700)

    def paint(self, painter, option, widget, x_start, y_start):
        punkty = []
        for i in range(6):
            t = 60 * i
            x = x_start + self.size * math.cos(math.radians(t))
            y = y_start + self.size * math.sin(math.radians(t))
            punkty.append(QtCore.QPointF(x, y))
        # hexagon=QtGui.QPolygon(punkty)
        return painter.drawPolygon(punkty)

    def write_val(self, painter, option, widget):
        if self.value != 0:
            rect = QtCore.QRectF(self.x_center - self.size, self.y_center - self.size, 2 * self.size, 2 * self.size)
            painter.setFont(QtGui.QFont('Arial', 16))
            painter.drawText(rect, QtCore.Qt.AlignCenter, str(self.value))


# czy przez przypadek każdy element planszy nie ma być osobną instancją klasy?
class TicTacToe(QtWidgets.QGraphicsItem):
    def __init__(self, n=3, x_start=250, y_start=150):
        super(TicTacToe, self).__init__()
        b = []
        whole_board = np.array([])
        row = []
        for i in range(n):
            for j in range(n + i):
                row.append(Hexagon(x=i, y=j, z=-(-i + j - n + 1)))
            row = np.array(row, dtype=object)
            whole_board = np.append(whole_board, row)
            b.append(row)
            row = []
        offset = 0
        for i in range(1, n):
            offset += 1
            for j in range(2 * n - 1 - i):
                row.append(Hexagon(x=(n - 1 + i), y=offset + j, z=((n - 1 + i) - (j + offset) + n - 1)))
            row = np.array(row, dtype=object)
            whole_board = np.append(whole_board, row)
            b.append(row)
            row = []

        #     tworzenie arraya dla y i z
        b_y = []
        ctr = 0
        b_z = []
        row_y = []
        row_z = []
        for j in range(2 * n - 1):
            for i in range(len(whole_board)):
                if whole_board[i].y == ctr:
                    row_y.append(whole_board[i])
                if whole_board[i].z == ctr:
                    row_z.append(whole_board[i])
            row_y = np.array(row_y, dtype=object)
            b_y.append(row_y)
            row_z = np.array(row_z, dtype=object)
            b_z.append(row_z)
            row_y = []
            row_z = []
            ctr += 1

        # ctr=0
        # for i in range(len(whole_board)):
        #     if whole_board[i].z==0:
        #         row.append(whole_board[i])
        #         row=np.array(row,dtype=object)
        #         b_z.append(row)
        #         row=[]
        #         ctr+=1

        # for i in range(n):
        #     b.append(np.zeros(n + i, dtype=object))
        # for i in range(1, n):
        #     b.append(np.zeros(2 * n - 1 - i, dtype=object))
        self.size = n
        self.board = b
        self.y_board = b_y
        self.z_board = b_z
        self.x_start = x_start
        self.y_start = y_start
        self.score = 0
        self.O = 0
        self.X = 1
        self.turn = self.O
        self.coords = 0

    # def reset(self):
    #     for y in range(self.size):
    #         for x in range(self.size):
    #             self.board[y][x] = -1
    #             self.turn = self.O
    #             self.update()
    #
    # def select(self, x, y):
    #     if x < 0 or y < 0 or x >= 3 or y >= 3:
    #         return
    #     if self.board[y][x] == -1:
    #         self.board[y][x] = self.turn
    #         self.turn = 1 - self.turn

    def paint(self, painter, option, widget):
        # # painter.setPen(QtCore.Qt.black)
        # brush=QtGui.QBrush
        # col=QtGui.QColor(QtGui.qRgb(204, 192, 179))
        # brush.setColor(col)
        # #         painter.setBrush(brush)

        painter.setBrush(QtGui.QColor(204, 192, 179, 127))
        # hex = Hexagon()

        x = self.x_start
        y = self.y_start
        # coords_list = []
        # for i in range(self.size):
        #     coords_list.append(np.zeros(self.size + i, dtype=object))
        # for i in range(1, self.size):
        #     coords_list.append(np.zeros(2 * self.size - 1 - i, dtype=object))

        for j in range(len(self.board)):
            for i in range(len(self.board[j])):
                if self.board[j][i].value == 0:
                    painter.setBrush(QtGui.QColor(204, 192, 179, 200))
                if self.board[j][i].value == 2:
                    painter.setBrush(QtGui.QColor(238, 228, 218, 200))
                if self.board[j][i].value == 4:
                    painter.setBrush(QtGui.QColor(238, 225, 201, 200))
                if self.board[j][i].value == 8:
                    painter.setBrush(QtGui.QColor(243, 178, 122, 200))
                if self.board[j][i].value == 16:
                    painter.setBrush(QtGui.QColor(246, 150, 100, 200))
                if self.board[j][i].value == 32:
                    painter.setBrush(QtGui.QColor(247, 124, 95, 200))
                if self.board[j][i].value == 64:
                    painter.setBrush(QtGui.QColor(247, 95, 59, 200))
                if self.board[j][i].value == 128:
                    painter.setBrush(QtGui.QColor(237, 208, 115, 200))
                if self.board[j][i].value == 256:
                    painter.setBrush(QtGui.QColor(237, 204, 98, 200))
                if self.board[j][i].value == 512:
                    painter.setBrush(QtGui.QColor(237, 201, 80, 200))
                if self.board[j][i].value == 1024:
                    painter.setBrush(QtGui.QColor(237, 197,  63, 200))
                if self.board[j][i].value == 2048:
                    painter.setBrush(QtGui.QColor(237, 194,  46, 200))
                if j / self.size < 1:
                    self.board[j][i].x_center = (
                            (x + j * 1.5 * (self.board[j][i].size)) - (i * 1.5 * (self.board[j][i].size)))
                    self.board[j][i].y_center = ((y + j * self.board[j][i].size / 2 * math.sqrt(3)) + (
                            i * self.board[j][i].size / 2 * math.sqrt(3)))

                    self.board[j][i].paint(painter, option, widget, self.board[j][i].x_center,
                                           self.board[j][i].y_center)
                    self.board[j][i].write_val(painter, option, widget)

                    # hex.paint(painter, option, widget, (x + j * 1.5 * (hex.size)) - (i * 1.5 * (hex.size)),
                    #           (y + j * hex.size / 2 * math.sqrt(3)) + (i * hex.size / 2 * math.sqrt(3)))
                    # coords_list[j][i] = (((x + j * 1.5 * (hex.size)) - (i * 1.5 * (hex.size)))
                    #                      , ((y + j * hex.size / 2 * math.sqrt(3)) + (i * hex.size / 2 * math.sqrt(3))))

                else:
                    self.board[j][i].x_center = ((x + (self.size - 1) * 1.5 * (self.board[j][i].size)) - (
                            i * 1.5 * (self.board[j][i].size)))
                    self.board[j][i].y_center = (
                            (y + (j - self.size / 2 + 0.5) * self.board[j][i].size * math.sqrt(3)) + (
                            i * self.board[j][i].size / 2 * math.sqrt(3)))

                    self.board[j][i].paint(painter, option, widget, self.board[j][i].x_center,
                                           self.board[j][i].y_center)
                    self.board[j][i].write_val(painter, option, widget)
                    # hex.paint(painter, option, widget,
                    #           (x + (self.size - 1) * 1.5 * (hex.size)) - (i * 1.5 * (hex.size)),
                    #           (y + (j - self.size / 2 + 0.5) * hex.size * math.sqrt(3)) + (
                    #                       i * hex.size / 2 * math.sqrt(3)))
                    # coords_list[j][i] = (((x + j * 1.5 * (hex.size)) - (i * 1.5 * (hex.size)))
                    #                      , ((y + j * hex.size / 2 * math.sqrt(3)) + (i * hex.size / 2 * math.sqrt(3))))
        # print("Siema")

    # def drawTile(self, painter, option, widget,coord_x,coord_y,hex):
    #     painter.setBrush(QtGui.QColor((237, 224, 200,200)))
    #     hex.paint(painter, option, widget,coord_x,coord_y)

    def spawnTile(self,x_in=-1,y_in=-1,val=0):
        if x_in==-1 and y_in==-1:
            x = random.randint(0, 2 * self.size - 2)
            y = random.randint(0, len(self.board[x]) - 1)

        tile_val_int = random.randint(0, 100)
        # value = 2
        if val==0:
            if tile_val_int < 80:
                value = 2
            else:
                value = 4
        else:
            value=val
        # if(self.board[x])
        # hex=Hexagon()
        if x_in==-1 and y_in==-1:
            while (self.board[x][y].value != 0):
                x = random.randint(0, 2 * self.size - 2)
                y = random.randint(0, len(self.board[x]) - 1)
        else:
            x=x_in
            y=y_in

        # print("Spawned tile of value " + str(value) + ", at: " + str(x) + ", " + str(y))
        output = "Spawned tile of value " + str(value) + ", at: " + str(x) + ", " + str(y)
        self.board[x][y].value = value

        # else:
        #     print("Wylosowałem " + str(x) + "," + str(y) + " ale jest już zajęte!")

        self.update()

        return output

    def moves(self, direction):
        if direction == "left_down":
            for j in range(len(self.board) - 1, -1, -1):
                free_pos = len(self.board[j]) - 1
                for i in range(len(self.board[j]) - 1, -1, -1):
                    if self.board[j][i].value != 0:
                        # if self.board[j][i].y<len(self.board[j])-1:
                        self.board[j][free_pos].value = self.board[j][i].value
                        if free_pos != i:
                            self.board[j][i].value = 0
                        free_pos -= 1

                        # print(
                        #     "Przesunąłem klocek " + str(self.board[j][i].x) + " " + str(self.board[j][i].y) + " " + str(
                        #         self.board[j][i].z))
        if direction == "right_up":
            for j in range(len(self.board)):
                free_pos = 0
                for i in range(len(self.board[j])):
                    if self.board[j][i].value != 0:
                        # if self.board[j][i].y<len(self.board[j])-1:
                        self.board[j][free_pos].value = self.board[j][i].value
                        if free_pos != i:
                            self.board[j][i].value = 0
                        free_pos += 1
                        # print(
                        #     "Przesunąłem klocek " + str(self.board[j][i].x) + " " + str(self.board[j][i].y) + " " + str(
                        #         self.board[j][i].z))
        if direction == "down":
            for j in range(len(self.z_board) - 1, -1, -1):
                free_pos = len(self.z_board[j]) - 1
                for i in range(len(self.z_board[j]) - 1, -1, -1):
                    if self.z_board[j][i].value != 0:
                        # if self.board[j][i].y<len(self.board[j])-1:
                        self.z_board[j][free_pos].value = self.z_board[j][i].value
                        if free_pos != i:
                            self.z_board[j][i].value = 0
                        free_pos -= 1
                        # print(
                        #     "Przesunąłem klocek " + str(self.z_board[j][i].x) + " " + str(
                        #         self.z_board[j][i].y) + " " + str(
                        #         self.z_board[j][i].z))
        if direction == "up":
            for j in range(len(self.z_board)):
                free_pos = 0
                for i in range(len(self.z_board[j])):
                    if self.z_board[j][i].value != 0:
                        # if self.board[j][i].y<len(self.board[j])-1:
                        self.z_board[j][free_pos].value = self.z_board[j][i].value
                        if free_pos != i:
                            self.z_board[j][i].value = 0
                        free_pos += 1
                        # print(
                        #     "Przesunąłem klocek " + str(self.z_board[j][i].x) + " " + str(
                        #         self.z_board[j][i].y) + " " + str(
                        #         self.z_board[j][i].z))
        if direction == "right_down":
            for j in range(len(self.y_board) - 1, -1, -1):
                free_pos = len(self.y_board[j]) - 1
                for i in range(len(self.y_board[j]) - 1, -1, -1):
                    if self.y_board[j][i].value != 0:
                        # if self.board[j][i].y<len(self.board[j])-1:
                        self.y_board[j][free_pos].value = self.y_board[j][i].value
                        if free_pos != i:
                            self.y_board[j][i].value = 0
                        free_pos -= 1
                        # print(
                        #     "Przesunąłem klocek " + str(self.y_board[j][i].x) + " " + str(
                        #         self.y_board[j][i].y) + " " + str(
                        #         self.y_board[j][i].z))
        if direction == "left_up":
            for j in range(len(self.y_board)):
                free_pos = 0
                for i in range(len(self.y_board[j])):
                    if self.y_board[j][i].value != 0:
                        # if self.board[j][i].y<len(self.board[j])-1:
                        self.y_board[j][free_pos].value = self.y_board[j][i].value
                        if free_pos != i:
                            self.y_board[j][i].value = 0
                        free_pos += 1
                        # print(
                        #     "Przesunąłem klocek " + str(self.y_board[j][i].x) + " " + str(
                        #         self.y_board[j][i].y) + " " + str(
                        #         self.y_board[j][i].z))
        # print(self.score)
        self.update()

    def merge(self, direction):
        if direction == "left_down":
            ifmerged = False
            for j in range(len(self.board) - 1, -1, -1):
                for i in range(len(self.board[j]) - 1, 0, -1):
                    if self.board[j][i].value == self.board[j][i - 1].value and self.board[j][i].value != 0:
                        # if self.board[j][i].y<len(self.board[j])-1:
                        self.board[j][i].value *= 2
                        self.board[j][i - 1].value = 0
                        ifmerged = True
                        self.score += self.board[j][i].value
                        # print(self.score)
            return ifmerged
        if direction == "right_up":
            ifmerged = False
            for j in range(len(self.board)):
                for i in range(len(self.board[j]) - 1):
                    if self.board[j][i].value == self.board[j][i + 1].value and self.board[j][
                        i].value != 0:
                        # if self.board[j][i].y<len(self.board[j])-1:
                        self.board[j][i].value *= 2
                        self.board[j][i + 1].value = 0
                        ifmerged = True
                        self.score += self.board[j][i].value
                        # print(self.score)
            return ifmerged
        if direction == "up":
            ifmerged = False
            for j in range(len(self.z_board)):
                for i in range(len(self.z_board[j]) - 1):
                    if self.z_board[j][i].value == self.z_board[j][i + 1].value and self.z_board[j][
                        i].value != 0:
                        # if self.board[j][i].y<len(self.board[j])-1:
                        self.z_board[j][i].value *= 2
                        self.z_board[j][i + 1].value = 0
                        ifmerged = True
                        self.score += self.z_board[j][i].value
                        # print(self.score)
            return ifmerged
        if direction == "down":
            ifmerged = False
            for j in range(len(self.z_board) - 1, -1, -1):
                for i in range(len(self.z_board[j]) - 1, 0, -1):
                    if self.z_board[j][i].value == self.z_board[j][i - 1].value and self.z_board[j][
                        i].value != 0:
                        # if self.board[j][i].y<len(self.board[j])-1:
                        self.z_board[j][i].value *= 2
                        self.z_board[j][i - 1].value = 0
                        ifmerged = True
                        self.score += self.z_board[j][i].value
                        # print(self.score)
            return ifmerged
        if direction == "left_up":
            ifmerged = False
            for j in range(len(self.y_board)):
                for i in range(len(self.y_board[j]) - 1):
                    if self.y_board[j][i].value == self.y_board[j][i - 1].value and self.y_board[j][
                        i].value != 0:
                        # if self.board[j][i].y<len(self.board[j])-1:
                        self.y_board[j][i].value *= 2
                        self.y_board[j][i - 1].value = 0
                        ifmerged = True
                        self.score += self.y_board[j][i].value
                        # print(self.score)
            return ifmerged
        if direction == "right_down":
            ifmerged = False
            for j in range(len(self.y_board) - 1, -1, -1):
                for i in range(len(self.y_board[j]) - 1, 0, -1):
                    if self.y_board[j][i].value == self.y_board[j][i - 1].value and self.y_board[j][
                        i].value != 0:
                        # if self.board[j][i].y<len(self.board[j])-1:
                        self.y_board[j][i].value *= 2
                        self.y_board[j][i - 1].value = 0
                        ifmerged = True
                        self.score += self.y_board[j][i].value
                        # print(self.score)
            return ifmerged
            # print(
            #     "Przesunąłem klocek " + str(self.board[j][i].x) + " " + str(self.board[j][i].y) + " " + str(
            #         self.board[j][i].z))

    def boundingRect(self):
        return QtCore.QRectF(0, 0, 1200, 700)

    def __del__(self):
        print("Destructor called")
    # def mousePressEvent(self, event):
    #     pos = event.pos()
    #     self.select(int(pos.x() / 100), int(pos.y() / 100))
    #     self.update()
    #     super(TicTacToe, self).mousePressEvent(event)


class PopupWindow(QtWidgets.QDialog):
    def __init__(self, main, type):
        super(PopupWindow, self).__init__()
        self.main_window = main
        if type == "&Opcje gry":
            self.game()

    def net(self):
        pass

    def game(self):
        board_size = QtWidgets.QLabel("Wybierz rozmiar planszy: ")
        self.board_size_combobox = QtWidgets.QComboBox()
        self.board_size_combobox.addItem('3')
        self.board_size_combobox.addItem('4')
        self.board_size_combobox.addItem('5')
        self.board_size_combobox.currentTextChanged.connect(self.main_window.change_size)

        window_layout = QtWidgets.QVBoxLayout()
        window_layout.addWidget(board_size)
        window_layout.addWidget(self.board_size_combobox)
        self.setLayout(window_layout)
        self.setGeometry(200, 200, 400, 400)
        self.setWindowTitle("Ustawienia gry")


# możliwe że tu w zaleznosci od systemu trzeba bedzie zczytywać odpowiednio
class SaveHistory(QtWidgets.QFileDialog):
    def __init__(self, main,type):
        super(SaveHistory, self).__init__()
        if type=="History":
            self.filename, _ = self.getSaveFileName(self, "Save game history", "history.xml", "XML File (*.xml)")
            try:
                # file = open(self.filename, 'w')
                text = main.historia.toPlainText()
                splited=text.splitlines()
                splited_words=[]
                for el in splited:
                    tmp=el.split()
                    splited_words.append(tmp)
                create_xml(self.filename,main.size,splited_words)
                # file.write(text)
                # file.close()
            except:
                print("Nie zapisano historii gry!")
                out=MessageB(self,"History")
            # self.mode=self.setFileMode(QtWidgets.QFileDialog.AnyFile)
            # self.show()
        if type=="Config":
            self.filename, _ = self.getSaveFileName(self, "Save game configuration", "config.json", "JSON File (*.json)")
            try:
                file = open(self.filename, 'w')
                text = main.historia.toPlainText()
                file.write(text)
                file.close()
            except:
                print("Nie zapisano konfiguracji gry!")
                out=MessageB(self,"Config")
            # self.mode=self.setFileMode(QtWidgets.QFileDialog.AnyFile)
            # self.show()
        if type=="Emulate":
            self.filename, _ = self.getOpenFileNames(self, "Select a xml file with game history to emulate", "","XML Files (*.xml)")
            try:
                base=os.path.basename(self.filename[0])
                read_xml(base,main)
            except:
                print("Nie otworzono pliku xml do emulowania!")
                out=MessageB(self,"Emulate")
class MessageB(QtWidgets.QMessageBox):
    def __init__(self,main,type):
        super(MessageB, self).__init__()
        if type=="Exit":
            self.setText("Czy na pewno chcesz zamknąć?")
            self.setInformativeText("Zamknięcie gry bez zapisywania spowoduje utratę progresu.")
            self.setStandardButtons(QtWidgets.QMessageBox.Ok|QtWidgets.QMessageBox.Cancel)
            self.setDefaultButton(QtWidgets.QMessageBox.Cancel)
            ret= self.exec_()

            if ret == QtWidgets.QMessageBox.Cancel:
                self.close()
            else:
                main.close()
        if type=="Nowa":
            self.setText("Czy na pewno chcesz uruchomić grę na nowo?")
            # self.setInformativeText("Zamknięcie gry bez zapisywania spowoduje utratę progresu.")
            self.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
            self.setDefaultButton(QtWidgets.QMessageBox.Cancel)
            ret = self.exec_()

            if ret == QtWidgets.QMessageBox.Cancel:
                self.close()
            else:
                # dodac resetowanie score'a
                main.tic_tac_toe.hide()
                main.gracz_sieciowy.hide()
                main.historia.clear()

                del main.tic_tac_toe
                main.tic_tac_toe=TicTacToe(int(main.size), 250, 100)

                spawn = main.tic_tac_toe.spawnTile()
                print(spawn)
                main.historia.append(spawn)

                spawn = main.tic_tac_toe.spawnTile()
                print(spawn)
                main.historia.append(spawn)

                del main.gracz_sieciowy
                main.gracz_sieciowy=TicTacToe(int(main.size), 800, 100)

                main.scene.addItem(main.tic_tac_toe)
                main.scene.addItem(main.gracz_sieciowy)
                main.scene.update()
        if type=="History":
            self.setText("NIE ZAPISANO HISTORII GRY!")
            # self.setInformativeText("Zamknięcie gry bez zapisywania spowoduje utratę progresu.")
            self.setStandardButtons(QtWidgets.QMessageBox.Ok)
            self.setDefaultButton(QtWidgets.QMessageBox.Ok)
            ret = self.exec_()

            if ret == QtWidgets.QMessageBox.Cancel:
                self.close()

        if type=="Config":
            self.setText("NIE ZAPISANO KONFIGURACJI GRY!")
            # self.setInformativeText("Zamknięcie gry bez zapisywania spowoduje utratę progresu.")
            self.setStandardButtons(QtWidgets.QMessageBox.Ok)
            self.setDefaultButton(QtWidgets.QMessageBox.Ok)
            ret = self.exec_()

            if ret == QtWidgets.QMessageBox.Cancel:
                self.close()
        if type=="Emulate":
            self.setText("NIE OTWORZONO PLIKU DO EMULOWANIA!")
            # self.setInformativeText("Zamknięcie gry bez zapisywania spowoduje utratę progresu.")
            self.setStandardButtons(QtWidgets.QMessageBox.Ok)
            self.setDefaultButton(QtWidgets.QMessageBox.Ok)
            ret = self.exec_()

            if ret == QtWidgets.QMessageBox.Cancel:
                self.close()

        if type=="Autoplay":
            self.setText("Tutaj bedzie sie automatycznie rozgrywać gra")
            # self.setInformativeText("Zamknięcie gry bez zapisywania spowoduje utratę progresu.")
            self.setStandardButtons(QtWidgets.QMessageBox.Ok)
            self.setDefaultButton(QtWidgets.QMessageBox.Ok)
            ret = self.exec_()

            if ret == QtWidgets.QMessageBox.Cancel:
                self.close()


# coś jest chyba nie tak ze score
class MainWindow(QtWidgets.QGraphicsView):
    def __init__(self, n=3):
        super(MainWindow, self).__init__()
        self.scene = QtWidgets.QGraphicsScene(self)
        self._createActions()
        self._createMenuBar()
        # self._connectActions()
        self.option_menu.triggered[QtWidgets.QAction].connect(self.con)
        # self.menubar.triggered[QtWidgets.QAction].connect(self.menucon)

        self.size = n

        # rozmiar planszy
        # plansza gracza 1
        self.tic_tac_toe = TicTacToe(int(self.size), 250, 100)

        # QTextEdit z historią
        self.historia = QtWidgets.QTextEdit()
        self.historia.setReadOnly(True)
        self.historia.setGeometry(0, 600, 400, 200)

        # wylosowanie mu na początku 2 płytek
        spawn = self.tic_tac_toe.spawnTile()
        print(spawn)
        self.historia.append(spawn)
        spawn = self.tic_tac_toe.spawnTile()
        print(spawn)
        self.historia.append(spawn)
        # gracz sieciowy
        self.gracz_sieciowy = TicTacToe(n, 800, 100)

        # label z wynikiem gracza 1
        self.labelA = QtWidgets.QGraphicsSimpleTextItem()
        self.labelA.setText("Player A Score: ")
        self.labelA.setY(20)
        font = QtGui.QFont("Helvetica", 15, QtGui.QFont.Bold)
        self.labelA.setFont(font)
        self.scene.addItem(self.labelA)
        self.labelScore = QtWidgets.QGraphicsSimpleTextItem()
        self.labelScore.setText(str(self.tic_tac_toe.score))
        self.labelScore.setX(180)
        self.labelScore.setY(20)
        self.labelScore.setFont(font)

        # label z wynikiem gracza sieciowego
        self.labelWeb = QtWidgets.QGraphicsSimpleTextItem()
        self.labelWeb.setText("Web Player Score: ")
        self.labelWeb.setFont(font)
        self.labelWeb.setX(500)
        self.labelWeb.setY(20)
        self.scene.addItem(self.labelWeb)
        self.labelWebScore = QtWidgets.QGraphicsSimpleTextItem()
        self.labelWebScore.setText(str(self.gracz_sieciowy.score))
        self.labelWebScore.setX(710)
        self.labelWebScore.setY(20)
        self.labelWebScore.setFont(font)

        # dodawanie elementów do sceny
        self.scene.addWidget(self.historia)
        self.scene.addItem(self.labelScore)
        self.scene.addItem(self.labelWebScore)
        self.scene.addItem(self.tic_tac_toe)
        self.scene.addItem(self.gracz_sieciowy)
        # scene.setSceneRect(0, 0, 1200, 700)
        self.setScene(self.scene)
        self.setCacheMode(QtWidgets.QGraphicsView.CacheBackground)
        # self.setWindowTitle("2048 Hexagons are TheBestagons")

        self.newGameButton=QtWidgets.QPushButton("New Game", self)
        self.newGameButton.setGeometry(750, 700, 80, 50)
        self.newGameButton.clicked.connect(self.newGame)

        self.exitGameButton=QtWidgets.QPushButton("Exit", self)
        self.exitGameButton.setGeometry(750, 750, 80, 50)
        self.exitGameButton.clicked.connect(self.exitGame)

        self.saveGameHistoryButton = QtWidgets.QPushButton("Save History", self)
        self.saveGameHistoryButton.setGeometry(850, 700, 80, 50)
        self.saveGameHistoryButton.clicked.connect(self.saveHistory)

        self.saveConfigButton = QtWidgets.QPushButton("Save \n Configuration", self)
        self.saveConfigButton.setGeometry(850, 750, 80, 50)
        self.saveConfigButton.clicked.connect(self.saveConfig)

        self.autoPlayButton = QtWidgets.QPushButton("Auto Play", self)
        self.autoPlayButton.setGeometry(950, 700, 80, 50)
        self.autoPlayButton.clicked.connect(self.autoPlay)

        self.emulateButton = QtWidgets.QPushButton("Emulate", self)
        self.emulateButton.setGeometry(950, 750, 80, 50)
        self.emulateButton.clicked.connect(self.emulate)

        self.Q = QtWidgets.QPushButton("&Q", self)
        self.Q.setShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Q))
        self.Q.setGeometry(550, 670, 30, 30)
        self.Q.clicked.connect(self.moveq)

        self.A = QtWidgets.QPushButton("&A", self)
        self.A.setGeometry(550, 720, 30, 30)
        self.A.setShortcut(QtGui.QKeySequence(QtCore.Qt.Key_A))
        self.A.clicked.connect(self.movea)

        self.W = QtWidgets.QPushButton("&W", self)
        self.W.setGeometry(600, 650, 30, 30)
        self.W.setShortcut(QtGui.QKeySequence(QtCore.Qt.Key_W))
        self.W.clicked.connect(self.movew)

        self.E = QtWidgets.QPushButton("&E", self)
        self.E.setGeometry(650, 670, 30, 30)
        self.E.setShortcut(QtGui.QKeySequence(QtCore.Qt.Key_E))
        self.E.clicked.connect(self.movee)

        self.D = QtWidgets.QPushButton("&D", self)
        self.D.setGeometry(650, 720, 30, 30)
        self.D.setShortcut(QtGui.QKeySequence(QtCore.Qt.Key_D))
        self.D.clicked.connect(self.moved)

        self.S = QtWidgets.QPushButton("&S", self)
        self.S.setGeometry(600, 750, 30, 30)
        self.S.setShortcut(QtGui.QKeySequence(QtCore.Qt.Key_S))
        self.S.clicked.connect(self.moves)

        przyciski = QtWidgets.QGraphicsSimpleTextItem()
        przyciski.setText("Buttons")
        przyciski.setX(500)
        przyciski.setY(760)
        przyciski.setFont(font)
        self.scene.addItem(przyciski)



    def change_size(self, q,xml=False):
        if q == "4":
            self.size = 4
        if q == "3":
            self.size = 3
        if q == "5":
            self.size = 5
        self.tic_tac_toe.hide()
        self.gracz_sieciowy.hide()
        self.historia.clear()
        del self.tic_tac_toe
        del self.gracz_sieciowy
        printRed("Zmieniono rozmiar planszy na: " + str(self.size))

        # dodac resetowanie score'a
        self.tic_tac_toe = TicTacToe(int(self.size), 250, 100)
        if xml==False:
            spawn = self.tic_tac_toe.spawnTile()
            print(spawn)
            self.historia.append(spawn)
            spawn = self.tic_tac_toe.spawnTile()
            print(spawn)
            self.historia.append(spawn)
        self.gracz_sieciowy = TicTacToe(int(self.size), 800, 100)
        self.scene.addItem(self.tic_tac_toe)
        self.scene.addItem(self.gracz_sieciowy)
        self.scene.update()

    def newGame(self):
        self.messbox = MessageB(self, "Nowa")
        # self.koniec.show()
        print("Nowa Gra")
    def exitGame(self):
        self.messbox = MessageB(self, "Exit")
        # self.koniec.show()
        print("Koniec")

    def saveHistory(self):
        self.dialog = SaveHistory(self,"History")
    def saveConfig(self):
        self.dialog = SaveHistory(self,"Config")

    def autoPlay(self):
        self.messbox=MessageB(self,"Autoplay")
    def emulate(self):
        self.dialog=SaveHistory(self,"Emulate")
    #     read xml
    # do moves
        pass
    def con(self, q):
        if q.text()=="&Nowa gra":
            self.newGame()
        if q.text() == "&Opcje gry":
            self.pop = PopupWindow(self, q.text())
            self.pop.show()
            # self.historia.append("POPUP")
        if q.text() == "&Zapisz historie":
            self.saveHistory()
            # self.dialog.show()
        if q.text() == "&Wyjdz":
            self.exitGame()
        if q.text() =="&Auto rozgrywka":
            self.autoPlay()
        if q.text() == "&Zapisz konfiguracje":
            self.saveConfig()
        if q.text() =="&Emuluj":
            self.emulate()

    def _createMenuBar(self):
        self.menubar = QtWidgets.QMenuBar(self)
        self.option_menu = self.menubar.addMenu('&Opcje')
        self.option_menu.addAction(self.newGameAction)
        self.option_menu.addAction(self.newAction)
        self.option_menu.addAction(self.netAction)
        self.option_menu.addAction(self.saveConfigAction)
        self.option_menu.addAction(self.saveHistoryAction)
        self.option_menu.addAction(self.loadAction)
        self.option_menu.addAction(self.autoplayAction)
        self.option_menu.addAction(self.exitAction)
        # Using a QMenu object
        # fileMenu = QtWidgets.QMenu("&Exit", self)
        # self.menubar.addMenu(fileMenu)
        # self.menubar.addAction(self.cutAction)
        # Using a title
        editMenu = self.menubar.addMenu("&Edit")

    def _createActions(self):
        # Creating action using the first constructor
        self.newAction = QtWidgets.QAction(self)
        self.newAction.setText("&Opcje gry")
        # Creating actions using the second constructor
        self.newGameAction = QtWidgets.QAction("&Nowa gra", self)
        self.netAction = QtWidgets.QAction("&Opcje sieciowe", self)
        self.saveHistoryAction = QtWidgets.QAction("&Zapisz historie", self)
        self.saveConfigAction = QtWidgets.QAction("&Zapisz konfiguracje", self)
        self.loadAction = QtWidgets.QAction("&Emuluj", self)
        self.exitAction = QtWidgets.QAction("&Wyjdz", self)
        self.autoplayAction = QtWidgets.QAction("&Auto rozgrywka", self)
        self.pasteAction = QtWidgets.QAction("&Paste", self)
        self.cutAction = QtWidgets.QAction("&Cut", self)
        self.helpContentAction = QtWidgets.QAction("&Help Content", self)
        self.aboutAction = QtWidgets.QAction("&About", self)

    def movea(self):
        replays = self.tic_tac_toe.size - self.tic_tac_toe.size // 2

        self.tic_tac_toe.moves(direction="left_down")
        changed = self.tic_tac_toe.merge(direction="left_down")
        while replays > 0 and changed == True:
            self.tic_tac_toe.moves(direction="left_down")
            changed = self.tic_tac_toe.merge(direction="left_down")
            replays -= 1

        printRed("Moved all tiles left_down")
        self.historia.append("Move direction = left_down")

        printGreen("Score = " + str(self.tic_tac_toe.score))
        self.historia.append("Score = " + str(self.tic_tac_toe.score))
        self.labelScore.setText(str(self.tic_tac_toe.score))

        spawn = self.tic_tac_toe.spawnTile()
        print(spawn)
        self.historia.append(spawn)

    def moveq(self):
        replays = self.tic_tac_toe.size - self.tic_tac_toe.size // 2
        self.tic_tac_toe.moves(direction="left_up")
        changed = self.tic_tac_toe.merge(direction="left_up")
        while replays > 0 and changed == True:
            self.tic_tac_toe.moves(direction="left_up")
            changed = self.tic_tac_toe.merge(direction="left_up")
            replays -= 1

        printRed("Moved all tiles left_up")
        self.historia.append("Move direction = left_up")

        printGreen("Score = " + str(self.tic_tac_toe.score))
        self.labelScore.setText(str(self.tic_tac_toe.score))
        self.historia.append("Score = " + str(self.tic_tac_toe.score))

        spawn = self.tic_tac_toe.spawnTile()
        print(spawn)
        self.historia.append(spawn)

    def movew(self):
        replays = self.tic_tac_toe.size - self.tic_tac_toe.size // 2
        self.tic_tac_toe.moves(direction="up")
        changed = self.tic_tac_toe.merge(direction="up")
        while replays > 0 and changed == True:
            self.tic_tac_toe.moves(direction="up")
            changed = self.tic_tac_toe.merge(direction="up")
            replays -= 1

        printRed("Moved all tiles up")
        self.historia.append("Move direction = up")

        printGreen("Score = " + str(self.tic_tac_toe.score))
        self.labelScore.setText(str(self.tic_tac_toe.score))
        self.historia.append("Score = " + str(self.tic_tac_toe.score))

        spawn = self.tic_tac_toe.spawnTile()
        print(spawn)
        self.historia.append(spawn)

    def movee(self):

        replays = self.tic_tac_toe.size - self.tic_tac_toe.size // 2
        self.tic_tac_toe.moves(direction="right_up")
        changed = self.tic_tac_toe.merge(direction="right_up")
        while replays > 0 and changed == True:
            self.tic_tac_toe.moves(direction="right_up")
            changed = self.tic_tac_toe.merge(direction="right_up")
            replays -= 1

        printRed("Moved all tiles right_up")
        self.historia.append("Move direction = right_up")

        printGreen("Score = " + str(self.tic_tac_toe.score))
        self.labelScore.setText(str(self.tic_tac_toe.score))
        self.historia.append("Score = " + str(self.tic_tac_toe.score))

        spawn = self.tic_tac_toe.spawnTile()
        print(spawn)
        self.historia.append(spawn)

    def moves(self):
        replays = self.tic_tac_toe.size - self.tic_tac_toe.size // 2
        self.tic_tac_toe.moves(direction="down")
        changed = self.tic_tac_toe.merge(direction="down")
        while replays > 0 and changed == True:
            self.tic_tac_toe.moves(direction="down")
            changed = self.tic_tac_toe.merge(direction="down")
            replays -= 1

        printRed("Moved all tiles down")
        self.historia.append("Move direction = down")

        printGreen("Score = " + str(self.tic_tac_toe.score))
        self.labelScore.setText(str(self.tic_tac_toe.score))
        self.historia.append("Score = " + str(self.tic_tac_toe.score))

        spawn = self.tic_tac_toe.spawnTile()
        print(spawn)
        self.historia.append(spawn)

    def moved(self):
        replays = self.tic_tac_toe.size - self.tic_tac_toe.size // 2
        self.tic_tac_toe.moves(direction="right_down")
        changed = self.tic_tac_toe.merge(direction="right_down")
        while replays > 0 and changed == True:
            self.tic_tac_toe.moves(direction="right_down")
            changed = self.tic_tac_toe.merge(direction="right_down")
            replays -= 1

        printRed("Moved all tiles right_down")
        self.historia.append("Move direction = right_down")

        printGreen("Score = " + str(self.tic_tac_toe.score))
        self.labelScore.setText(str(self.tic_tac_toe.score))
        self.historia.append("Score = " + str(self.tic_tac_toe.score))

        spawn = self.tic_tac_toe.spawnTile()
        print(spawn)
        self.historia.append(spawn)

    def keyPressEvent(self, event):
        key = event.key()
        # 3-2
        # 4-2
        # 5-3
        if key == QtCore.Qt.Key_1:
            spawn=self.tic_tac_toe.spawnTile()
            print(spawn)
            self.historia.append(spawn)
        if key == QtCore.Qt.Key_2:
            spawn=self.gracz_sieciowy.spawnTile()
            print(spawn)
            self.historia.append(spawn)
        super(MainWindow, self).keyPressEvent(event)
    #     # if key == QtCore.Qt.Key_A:
    #     #     # self.movea("A")
    #
    #     if key == QtCore.Qt.Key_E:
    #         self.tic_tac_toe.moves(direction="right_up")
    #         changed = self.tic_tac_toe.merge(direction="right_up")
    #         while replays > 0 and changed == True:
    #             self.tic_tac_toe.moves(direction="right_up")
    #             changed = self.tic_tac_toe.merge(direction="right_up")
    #             replays -= 1
    #
    #
    #         printRed("Moved all tiles right_up")
    #         self.historia.append("Move direction = right_up")
    #
    #         printGreen("Score = " + str(self.tic_tac_toe.score))
    #         self.labelScore.setText(str(self.tic_tac_toe.score))
    #         self.historia.append("Score = " + str(self.tic_tac_toe.score))
    #
    #         spawn=self.tic_tac_toe.spawnTile()
    #         print(spawn)
    #         self.historia.append(spawn)
    #
    #     if key == QtCore.Qt.Key_S:
    #         self.tic_tac_toe.moves(direction="down")
    #         changed = self.tic_tac_toe.merge(direction="down")
    #         while replays > 0 and changed == True:
    #             self.tic_tac_toe.moves(direction="down")
    #             changed = self.tic_tac_toe.merge(direction="down")
    #             replays -= 1
    #
    #
    #         printRed("Moved all tiles down")
    #         self.historia.append("Move direction = down")
    #
    #         printGreen("Score = " + str(self.tic_tac_toe.score))
    #         self.labelScore.setText(str(self.tic_tac_toe.score))
    #         self.historia.append("Score = " + str(self.tic_tac_toe.score))
    #
    #         spawn=self.tic_tac_toe.spawnTile()
    #         print(spawn)
    #         self.historia.append(spawn)
    #
    #     if key == QtCore.Qt.Key_W:
    #         self.tic_tac_toe.moves(direction="up")
    #         changed = self.tic_tac_toe.merge(direction="up")
    #         while replays > 0 and changed == True:
    #             self.tic_tac_toe.moves(direction="up")
    #             changed = self.tic_tac_toe.merge(direction="up")
    #             replays -= 1
    #
    #
    #         printRed("Moved all tiles up")
    #         self.historia.append("Move direction = up")
    #
    #         printGreen("Score = " + str(self.tic_tac_toe.score))
    #         self.labelScore.setText(str(self.tic_tac_toe.score))
    #         self.historia.append("Score = " + str(self.tic_tac_toe.score))
    #
    #         spawn=self.tic_tac_toe.spawnTile()
    #         print(spawn)
    #         self.historia.append(spawn)
    #
    #     if key == QtCore.Qt.Key_Q:
    #         self.tic_tac_toe.moves(direction="left_up")
    #         changed = self.tic_tac_toe.merge(direction="left_up")
    #         while replays > 0 and changed == True:
    #             self.tic_tac_toe.moves(direction="left_up")
    #             changed = self.tic_tac_toe.merge(direction="left_up")
    #             replays -= 1
    #
    #
    #         printRed("Moved all tiles left_up")
    #         self.historia.append("Move direction = left_up")
    #
    #         printGreen("Score = " + str(self.tic_tac_toe.score))
    #         self.labelScore.setText(str(self.tic_tac_toe.score))
    #         self.historia.append(str(self.tic_tac_toe.score))
    #
    #         spawn=self.tic_tac_toe.spawnTile()
    #         print(spawn)
    #         self.historia.append(spawn)
    #
    #     if key == QtCore.Qt.Key_D:
    #         self.tic_tac_toe.moves(direction="right_down")
    #         changed = self.tic_tac_toe.merge(direction="right_down")
    #         while replays > 0 and changed == True:
    #             self.tic_tac_toe.moves(direction="right_down")
    #             changed = self.tic_tac_toe.merge(direction="right_down")
    #             replays -= 1
    #
    #         printRed("Moved all tiles right_down")
    #         self.historia.append("Move direction = right_down")
    #
    #         printGreen("Score = " + str(self.tic_tac_toe.score))
    #         self.labelScore.setText(str(self.tic_tac_toe.score))
    #         self.historia.append(str(self.tic_tac_toe.score))
    #
    #         spawn=self.tic_tac_toe.spawnTile()
    #         print(spawn)
    #         self.historia.append(spawn)
    #
    #     super(MainWindow, self).keyPressEvent(event)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    window = MainWindow()
    window.setGeometry(100, 100, 1350, 900)
    window.show()
    # window.show()
    # mainWindow = MainWindow()
    #
    # # mainWindow.ensureVisible(mainWindow.tic_tac_toe)
    # mainWindow.show()

    # polygon=Grid(3)
    # widget = GameWindow()
    # widget.addItem(polygon)
    #
    # view=QtWidgets.QGraphicsView(widget)
    # view.resize(800,600)
    # # widget.resize(800, 600)
    # view.show()

    sys.exit(app.exec_())
