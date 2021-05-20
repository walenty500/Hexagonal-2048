import sys
import random
from PySide2 import QtCore, QtWidgets, QtGui
import numpy as np
import math
import xml.etree.ElementTree as et
import os
# import argparse
# import subprocess
import socket
import threading
import pickle


#
# def iterate_xml(leaf,main=object):
#     if leaf.tag == "spawn_value":
#         x = int(leaf.attrib["x"][:-1])
#         y = int(leaf.attrib["y"])
#         value = int(leaf.text[:-1])
#         spawn = main.tic_tac_toe.spawnTile(x, y, value)
#         print(spawn)
#     if leaf.tag == "move":
#         if leaf.text == "up":
#             main.movew(xml=True)
#         if leaf.text == "left_down":
#             main.movea(xml=True)
#         if leaf.text == "down":
#             main.moves(xml=True)
#         if leaf.text == "left_up":
#             main.moveq(xml=True)
#         if leaf.text == "right_up":
#             main.movee(xml=True)
#         if leaf.text == "right_down":
#             main.moved(xml=True)
#
# def read_xml(filename="przykladowy.xml",main=object):
#     tree = et.parse(filename)
#     root = tree.getroot()
#
#     size=root.attrib["board_size"]
#
#     main.change_size(size,xml=True)
#     for child in root:
#         # if child.attrib["nr"]==1:
#             for leaf in child:
#                 main.timer=QtCore.QTimer()
#                 main.timer.setInterval(500)
#                 main.timer.start()
#                 main.timer.timeout.connect(iterate_xml(leaf,main))
#
#                 main.timer.stop()
#                 # iterate_xml(leaf,main)
#
#
#
#                 # print(leaf.tag, leaf.attrib, leaf.text)
#
# # funkcja edytująca nam xml
# def create_xml(filename="przykladowy.xml",size=3,history=[]):
#     # tree = et.parse('./spam/dict.xml')
#     root = et.Element("hex2048",{"board_size":str(size)})#.getroot()
#
#     player1=et.Element("player",{"nr":"1"})
#     root.append(player1)
#
#     player2=et.Element("player",{"nr":"2"})
#     root.append(player2)
#
#     for el in history:
#         if el[0]=="Spawned":
#             tmp=et.SubElement(player1,"spawn_value",{"x":str(el[6]),"y":str(el[7])})
#             tmp.text=str(el[4])
#         if el[0]=="Move":
#             tmp=et.SubElement(player1,"move")
#             tmp.text = str(el[-1])
#         if el[0]=="Score":
#             tmp = et.SubElement(player1, "score")
#             tmp.text = str(el[-1])
#     # if filename[:-4]!=".xml":
#     #     output=filename+".xml"
#     # else:
#     output=filename
#     tree = et.ElementTree(root)
#     tree.write(output, xml_declaration=True, encoding='utf-8')
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
        self.nr_of_elem=0
        for i in range(n,2*n-1):
            self.nr_of_elem +=2*i
        self.nr_of_elem+=2*n-1
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
        self.full_board=False
        # self.nr_of_elem=0

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

    def check_if_board_full(self):
        counter=0

        for j in range(len(self.board)):
            for i in range(len(self.board[j])):
                if self.board[j][i].value!=0:
                    counter+=1
        if counter==self.nr_of_elem:
            self.full_board=True
            print("Plansza pełna")

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
                    painter.setBrush(QtGui.QColor(237, 197, 63, 200))
                if self.board[j][i].value == 2048:
                    painter.setBrush(QtGui.QColor(237, 194, 46, 200))
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

    def spawnTile(self, x_in=-1, y_in=-1, val=0):
        if x_in == -1 and y_in == -1:
            x = random.randint(0, 2 * self.size - 2)
            y = random.randint(0, len(self.board[x]) - 1)

        tile_val_int = random.randint(0, 100)
        # value = 2
        if val == 0:
            if tile_val_int < 80:
                value = 2
            else:
                value = 4
        else:
            value = val
        # if(self.board[x])
        # hex=Hexagon()
        self.check_if_board_full()
        if self.full_board==False:
            if x_in == -1 and y_in == -1:
                while (self.board[x][y].value != 0):
                    x = random.randint(0, 2 * self.size - 2)
                    y = random.randint(0, len(self.board[x]) - 1)
            else:
                x = x_in
                y = y_in

        # print("Spawned tile of value " + str(value) + ", at: " + str(x) + ", " + str(y))
            output = "Spawned tile of value " + str(value) + ", at: " + str(x) + ", " + str(y)
            self.board[x][y].value = value
            self.update()
        else:
            output = "Plansza pełna - przegrałeś grę!"
            print("Pełna tablica")

        # else:
        #     print("Wylosowałem " + str(x) + "," + str(y) + " ale jest już zajęte!")

        # self.update()

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
        if type =="&Opcje sieciowe":
            self.net()

    def net(self):
        net_name=QtWidgets.QLabel("Nazwa przeciwnika: ")
        self.net_player=QtWidgets.QLineEdit()
        self.net_player.setPlaceholderText("Web Player")
        self.net_player.textChanged.connect(self.main_window.change_web_name)
        ip=QtWidgets.QLabel("Adres IP: ")
        self.ip=QtWidgets.QLineEdit()
        self.ip.setText("127.0.0.1")
        self.ip.textChanged.connect(self.main_window.change_ip)
        port=QtWidgets.QLabel("Port połączenia: ")
        self.port=QtWidgets.QLineEdit()
        self.port.setText("8080")
        self.port.textChanged.connect(self.main_window.change_port)
        self.wyszukaj=QtWidgets.QPushButton()
        self.wyszukaj.setText("Wyszukaj gracza\nw sieci lokalnej")
        self.polacz=QtWidgets.QPushButton()
        self.polacz.setText("Połącz")



        window_layout = QtWidgets.QVBoxLayout()
        window_layout.addWidget(net_name)
        window_layout.addWidget(self.net_player)
        window_layout.addWidget(ip)
        window_layout.addWidget(self.ip)
        window_layout.addWidget(port)
        window_layout.addWidget(self.port)
        window_layout.addWidget(self.wyszukaj)
        window_layout.addWidget(self.polacz)
        self.setLayout(window_layout)
        self.setGeometry(200, 200, 400, 400)
        self.setWindowTitle("Ustawienia sieciowe")

    def game(self):
        player_name=QtWidgets.QLabel("Wybierz swoją nazwę: ")
        self.player=QtWidgets.QLineEdit()
        self.player.setPlaceholderText("Player A")
        self.player.textChanged.connect(self.main_window.change_name)
        board_size = QtWidgets.QLabel("Wybierz rozmiar planszy: ")
        self.board_size_combobox = QtWidgets.QComboBox()
        self.board_size_combobox.addItem('3')
        self.board_size_combobox.addItem('4')
        self.board_size_combobox.addItem('5')
        self.board_size_combobox.currentTextChanged.connect(self.main_window.change_size)

        window_layout = QtWidgets.QVBoxLayout()
        window_layout.addWidget(player_name)
        window_layout.addWidget(self.player)
        window_layout.addWidget(board_size)
        window_layout.addWidget(self.board_size_combobox)
        self.setLayout(window_layout)
        self.setGeometry(200, 200, 400, 400)
        self.setWindowTitle("Ustawienia gry")


# możliwe że tu w zaleznosci od systemu trzeba bedzie zczytywać odpowiednio
class SaveHistory(QtWidgets.QFileDialog):
    def __init__(self, main, type):
        super(SaveHistory, self).__init__()
        if type == "History":
            self.filename, _ = self.getSaveFileName(self, "Save game history", "history.xml", "XML File (*.xml)")
            try:
                # file = open(self.filename, 'w')
                text = main.historia.toPlainText()
                splited = text.splitlines()
                splited_words = []
                for el in splited:
                    tmp = el.split()
                    splited_words.append(tmp)
                main.create_xml(self.filename, main.size, splited_words)
                # file.write(text)
                # file.close()
            except:
                print("Nie zapisano historii gry!")
                out = MessageB(self, "History")
            # self.mode=self.setFileMode(QtWidgets.QFileDialog.AnyFile)
            # self.show(
        if type == "History Last Move":
            self.filename, _ = self.getSaveFileName(self, "Save game history", "history.xml", "XML File (*.xml)")
            try:
                # file = open(self.filename, 'w')
                text = main.historia.toPlainText()
                splited = text.splitlines()
                splited_words = []
                for el in splited:
                    tmp = el.split()
                    splited_words.append(tmp)
                splited_words_last_move = splited_words[:-3]
                main.create_xml(self.filename, main.size, splited_words_last_move)
                # file.write(text) 
                # file.close()
            except:
                print("Nie zapisano historii gry!")
                out = MessageB(self, "History")
        if type == "Config":
            self.filename, _ = self.getSaveFileName(self, "Save game configuration", "config.json",
                                                    "JSON File (*.json)")
            try:
                main.create_json()
                file = open(self.filename, 'w')
                text = main.historia.toPlainText()
                file.write(text)
                file.close()
            except:
                print("Nie zapisano konfiguracji gry!")
                out = MessageB(self, "Config")
            # self.mode=self.setFileMode(QtWidgets.QFileDialog.AnyFile)
            # self.show()
        if type == "Emulate":
            self.filename, _ = self.getOpenFileNames(self, "Select a xml file with game history to emulate", "",
                                                     "XML Files (*.xml)")
            try:
                base = os.path.basename(self.filename[0])
                baza=self.filename[0]
                main.read_xml(baza)
            except Exception as e:
                # print(e)
                print("Nie otworzono pliku xml do emulowania!")
                # print(base)
                # print(baza)
                out = MessageB(self, "Emulate")


class MessageB(QtWidgets.QMessageBox):
    def __init__(self, main, type):
        super(MessageB, self).__init__()
        if type == "Exit":
            self.setText("Czy na pewno chcesz zamknąć?")
            self.setInformativeText("Zamknięcie gry bez zapisywania spowoduje utratę progresu.")
            self.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
            self.setDefaultButton(QtWidgets.QMessageBox.Cancel)
            ret = self.exec_()

            if ret == QtWidgets.QMessageBox.Cancel:
                self.close()
            else:
                main.close()
        if type == "Nowa":
            self.setText("Czy na pewno chcesz uruchomić grę na nowo?")
            # self.setInformativeText("Zamknięcie gry bez zapisywania spowoduje utratę progresu.")
            self.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
            self.setDefaultButton(QtWidgets.QMessageBox.Cancel)
            ret = self.exec_()

            if ret == QtWidgets.QMessageBox.Cancel:
                self.close()
            else:
                # dodac resetowanie score'a
                text = main.historia.toPlainText()
                splited = text.splitlines()
                splited_words = []
                for el in splited:
                    tmp = el.split()
                    splited_words.append(tmp)
                main.create_xml(filename="last_save.xml", size=self.size, history=splited_words)
                main.tic_tac_toe.hide()
                main.gracz_sieciowy.hide()
                main.historia.clear()

                del main.tic_tac_toe
                main.tic_tac_toe = TicTacToe(int(main.size), 250, 100)

                spawn = main.tic_tac_toe.spawnTile()
                print(spawn)
                main.historia.append(spawn)

                spawn = main.tic_tac_toe.spawnTile()
                print(spawn)
                main.historia.append(spawn)

                del main.gracz_sieciowy
                main.gracz_sieciowy = TicTacToe(int(main.size), 800, 100)

                main.scene.addItem(main.tic_tac_toe)
                main.scene.addItem(main.gracz_sieciowy)
                main.scene.update()
        if type == "History":
            self.setText("NIE ZAPISANO HISTORII GRY!")
            # self.setInformativeText("Zamknięcie gry bez zapisywania spowoduje utratę progresu.")
            self.setStandardButtons(QtWidgets.QMessageBox.Ok)
            self.setDefaultButton(QtWidgets.QMessageBox.Ok)
            ret = self.exec_()

            if ret == QtWidgets.QMessageBox.Cancel:
                self.close()
        if type == "History Last Move":
            self.setText("Czy chcesz zapisac gre bez ostatniego ruchu?")
            self.setInformativeText("Przechowywanie historii z możliwością cofnięcia ostatniego ruchu")
            self.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
            self.setDefaultButton(QtWidgets.QMessageBox.Cancel)
            ret = self.exec_()

            if ret == QtWidgets.QMessageBox.Ok:
                pop = SaveHistory(main, "History Last Move")
                self.close()
            else:
                pop = SaveHistory(main, "History")
                self.close()

        if type == "Koniec Gry":
            self.setText("Koniec Gry - zacząć nową grę?")
            # self.setInformativeText("Zamknięcie gry bez zapisywania spowoduje utratę progresu.")
            self.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
            self.setDefaultButton(QtWidgets.QMessageBox.Ok)
            ret = self.exec_()

            if ret == QtWidgets.QMessageBox.Cancel:
                main.close()
            else:
                # dodac resetowanie score'a
                text = main.historia.toPlainText()
                splited = text.splitlines()
                splited_words = []
                for el in splited:
                    tmp = el.split()
                    splited_words.append(tmp)
                main.create_xml(filename="last_save.xml", size=self.size, history=splited_words)
                main.tic_tac_toe.hide()
                # main.gracz_sieciowy.hide()
                main.historia.clear()

                del main.tic_tac_toe
                main.tic_tac_toe = TicTacToe(int(main.size), 250, 100)

                spawn = main.tic_tac_toe.spawnTile()
                print(spawn)
                main.historia.append(spawn)

                spawn = main.tic_tac_toe.spawnTile()
                print(spawn)
                main.historia.append(spawn)

                del main.gracz_sieciowy
                main.gracz_sieciowy = TicTacToe(int(main.size), 800, 100)

                main.scene.addItem(main.tic_tac_toe)
                main.scene.addItem(main.gracz_sieciowy)
                main.scene.update()

        if type == "Config":
            self.setText("NIE ZAPISANO KONFIGURACJI GRY!")
            # self.setInformativeText("Zamknięcie gry bez zapisywania spowoduje utratę progresu.")
            self.setStandardButtons(QtWidgets.QMessageBox.Ok)
            self.setDefaultButton(QtWidgets.QMessageBox.Ok)
            ret = self.exec_()

            if ret == QtWidgets.QMessageBox.Cancel:
                self.close()
        if type == "Emulate":
            self.setText("NIE OTWORZONO PLIKU DO EMULOWANIA!")
            # self.setInformativeText("Zamknięcie gry bez zapisywania spowoduje utratę progresu.")
            self.setStandardButtons(QtWidgets.QMessageBox.Ok)
            self.setDefaultButton(QtWidgets.QMessageBox.Ok)
            ret = self.exec_()

            if ret == QtWidgets.QMessageBox.Cancel:
                self.close()
        if type == "Wrong File":
            self.setText("Podano zły plik!")
            # self.setInformativeText("Zamknięcie gry bez zapisywania spowoduje utratę progresu.")
            self.setStandardButtons(QtWidgets.QMessageBox.Ok)
            self.setDefaultButton(QtWidgets.QMessageBox.Ok)
            ret = self.exec_()

            if ret == QtWidgets.QMessageBox.Cancel:
                self.close()
        if type=="Wrong XML":
            self.setText("Podano niepoprawny plik xml!")
            self.setInformativeText("To nie jest historia gry.")
            self.setStandardButtons(QtWidgets.QMessageBox.Ok)
            self.setDefaultButton(QtWidgets.QMessageBox.Ok)
            ret = self.exec_()

            if ret == QtWidgets.QMessageBox.Cancel:
                self.close()

        if type == "Autoplay":
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
        self.host = '127.0.0.1'
        self.port = 8080
        self.name = "Player A"
        # self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 5)
        # self.naglowek=1024
        # self.naglowek_size=5
        # try:
        #     self.sock.connect((self.host, self.port))
        #     self.role = "Client"
        # except:
        #     self.sock.bind((self.host, self.port))
        #     self.role = "Server"
        #     self.clients = []
        #     self.sock.listen()
        # print(self.role)
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
        # if self.role == "Client":
        #     self.writeClient(spawn)
        print(spawn)
        self.historia.append(spawn)
        spawn = self.tic_tac_toe.spawnTile()
        # if self.role == "Client":
        #     self.writeClient(spawn)
        print(spawn)
        self.historia.append(spawn)
        # gracz sieciowy
        self.gracz_sieciowy = TicTacToe(n, 800, 100)

        # label z wynikiem gracza 1
        self.labelA = QtWidgets.QGraphicsSimpleTextItem()
        self.labelA.setText(self.name+" Score: ")
        self.labelA.setY(20)

        font = QtGui.QFont("Helvetica", 15, QtGui.QFont.Bold)
        self.labelA.setFont(font)
        self.scene.addItem(self.labelA)
        self.labelScore = QtWidgets.QGraphicsSimpleTextItem()
        self.labelScore.setText(str(self.tic_tac_toe.score))
        self.labelScore.setX(0)
        self.labelScore.setY(50)
        self.labelScore.setFont(font)

        # label z wynikiem gracza sieciowego
        self.labelWeb = QtWidgets.QGraphicsSimpleTextItem()
        self.labelWeb.setText("Web Player Score: ")
        self.labelWeb.setFont(font)
        self.labelWeb.setX(500)
        self.labelWeb.setY(50)
        self.scene.addItem(self.labelWeb)
        self.labelWebScore = QtWidgets.QGraphicsSimpleTextItem()
        self.labelWebScore.setText(str(self.gracz_sieciowy.score))
        self.labelWebScore.setX(710)
        self.labelWebScore.setY(20)
        self.labelWebScore.setFont(font)

        # dodawanie elementów do sceny
        self.scene.addWidget(self.historia)
        self.scene.addItem(self.labelScore)
        # self.scene.addItem(self.labelWebScore)
        self.scene.addItem(self.tic_tac_toe)
        self.scene.addItem(self.gracz_sieciowy)
        # scene.setSceneRect(0, 0, 1200, 700)
        self.setScene(self.scene)
        self.setCacheMode(QtWidgets.QGraphicsView.CacheBackground)
        # self.setWindowTitle("2048 Hexagons are TheBestagons")

        self.newGameButton = QtWidgets.QPushButton("New Game", self)
        self.newGameButton.setGeometry(750, 700, 80, 50)
        self.newGameButton.clicked.connect(self.newGame)

        self.exitGameButton = QtWidgets.QPushButton("Exit", self)
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

        self.leaf_list = []
        self.iterator = 0
        self.timer = QtCore.QTimer()
        self.timer.setInterval(500)
        # self.timer.timeout.connect(self.iterate_xml(self.leaf_list))
        # self.timer.start()

        self.timer_allow = False
        #     self.timer.start()
        # else:
        #     self.timer.stop()

        przyciski = QtWidgets.QGraphicsSimpleTextItem()
        przyciski.setText("Buttons")
        przyciski.setX(500)
        przyciski.setY(760)
        przyciski.setFont(font)
        self.scene.addItem(przyciski)

        # if self.role == "Server":
        #     self.receive_thread = threading.Thread(target=self.receiveServ,daemon=True)
        #     self.receive_thread.start()
        #
        # if self.role == "Client":
        #     self.receive_thread = threading.Thread(target=self.receiveClient,daemon=True)
        #     self.receive_thread.start()

            # self.write_thread=threading.Thread(target=self.write)
            # self.write_thread.start()

    def change_port(self,q):
        # print(type(q))
        try:
            self.port=int(q)
        except:
            print("Niepoprawny port")
    def change_ip(self,q):
        self.host=q
    def change_web_name(self,q):
        self.web_name=q
        self.labelWeb.setText(self.web_name+" Score: ")
    def change_name(self,q):
        self.name=q
        self.labelA.setText(self.name+" Score: ")
    def closeEvent(self, event):
        text = self.historia.toPlainText()
        splited = text.splitlines()
        splited_words = []
        for el in splited:
            tmp = el.split()
            splited_words.append(tmp)
        self.create_xml(filename="last_save.xml", size=self.size, history=splited_words)
        # self.receive_thread=0
        # if self.role=="Server":
        #     self.handle_thread=0
        print("Wychodze")

    def writeClient(self, mess):
        # while True:
        # tresc wiadomosci
        # a=mess
        # words=a.split()
        # struktura wiadomosci, ktora wysylamy wszystkim
        message = self.name + ' sends ' + mess
        naglowek=len(message)
        rozmiar_nagl=str(len(message))
        while len(rozmiar_nagl)!=self.naglowek_size:
            rozmiar_nagl="0"+rozmiar_nagl

        self.sock.send(rozmiar_nagl.encode('utf-8'))
        self.sock.send(message.encode('utf-8'))

    # metoda obslugujaca wiadomosci przychodzace
    def receiveClient(self):
        while True:
            try:
                # pobieranie wiadomosci z serwera
                nagl = self.sock.recv(5)
                nagl = int(nagl.decode())
                message = self.sock.recv(nagl)
                # nagl=int(nagl.decode())
                # message=self.sock.recv(nagl)
                conv=message.decode('utf-8')
                # wypisywanie jej w terminalu osoby
                print(conv)
            except:
                # gdy z jakiegos powodu nastapi blad
                print("An error occured!")
                # zamykamy polaczenie
                self.sock.close()
                break

    # wysyłanei do wszystkich uzytkowników odebranej wiadomości
    def broadcast(self, message):
        print(message.decode('utf-8'))
        self.historia.append(message.decode('utf-8'))
        rozmiar_nagl = str(len(message))
        while len(rozmiar_nagl) != self.naglowek_size:
            rozmiar_nagl = "0" + rozmiar_nagl


        for client in self.clients:
            client.send(rozmiar_nagl.encode('utf-8'))
            client.send(message)
        # obsluga wiadomosci i plikow

    def handle(self, client):
        while True:
            try:
                # odbieranie wiadomości
                nagl = client.recv(5)
                nagl=int(nagl.decode())
                message=client.recv(nagl)
                # jeżeli nie było to żadne z powyższych, to wysyłamy wiadomość do wszystkich
                self.broadcast(message)
            except:
                break

    # metoda odbierająca
    def receiveServ(self):
        while True:
            # akceptacja połaczenia
            client, address = self.sock.accept()
            print("Connection with {} established".format(str(address)))
            # dodanie nowo połączonej osoby do tablicy klientów
            self.clients.append(client)
            # Powiadomienie do wszystkich o wejsciu nowej osoby
            self.broadcast("Somebody entered the chatroom!".encode('utf-8'))
            # wiadomosc dla klienta ze sie połaczył
            # client.send('Connected!'.encode('utf-8'))

            # obsługa wątku przychodzacych wiadomosci i ich ewentualnego rozsylania
            self.handle_thread = threading.Thread(target=self.handle, args=(client,),daemon=True)
            self.handle_thread.start()

    def iterate_xml(self):
        if self.timer_allow == True:
            if self.leaf_list[self.iterator].tag == "spawn_value":
                x = int(self.leaf_list[self.iterator].attrib["x"][:-1])
                y = int(self.leaf_list[self.iterator].attrib["y"])
                value = int(self.leaf_list[self.iterator].text[:-1])
                spawn = self.tic_tac_toe.spawnTile(x, y, value)
                self.historia.append(spawn)
                print(spawn)
            if self.leaf_list[self.iterator].tag == "move":
                if self.leaf_list[self.iterator].text == "up":
                    self.movew(xml=True)
                if self.leaf_list[self.iterator].text == "left_down":
                    self.movea(xml=True)
                if self.leaf_list[self.iterator].text == "down":
                    self.moves(xml=True)
                if self.leaf_list[self.iterator].text == "left_up":
                    self.moveq(xml=True)
                if self.leaf_list[self.iterator].text == "right_up":
                    self.movee(xml=True)
                if self.leaf_list[self.iterator].text == "right_down":
                    self.moved(xml=True)
            self.iterator += 1
            if self.iterator == len(self.leaf_list):
                self.timer_allow = False
                self.timer.stop()

    def read_xml(self, filename="przykladowy.xml"):
        try:
            self.tree = et.parse(filename)
            self.root = self.tree.getroot()
            self.iterator = 0
            tag=True
            tmp=self.root.tag
            if tmp!="hex2048":
                tag=False
                # print(tmp)

            attr=False
            atributes=self.root.attrib
            if atributes=={'board_size': '3'} or atributes=={'board_size': '4'} or atributes=={'board_size': '5'}:
                attr = True

            if attr==True:
                size = self.root.attrib["board_size"]
            # print(atributes)
            # print(attr)
            # print(tmp)
            # print(tag)
            if attr==True and tag==True:
                self.leaf_list = []
                self.timer_allow = True
                self.change_size(size, xml=True)
                for child in self.root:
                    # if child.attrib["nr"]==1:
                    # self.timer.start()
                    for leaf in child:
                        self.leaf_list.append(leaf)

                # for child in self.root:
                #     # if child.attrib["nr"]==1:
                #     # self.timer.start()
                #     for leaf in child:
                #         self.iterate_xml()
                self.timer_allow = True
                self.timer.timeout.connect(self.iterate_xml)
                self.timer.start()
            else:
                self.messbox=MessageB(self,type="Wrong XML")
        except:
            self.messbox=MessageB(self,type="Wrong File")




        # self.iterate_xml(leaf)
        # self.timer.timeout.connect(self.iterate_xml(leaf))
        # self.timer = QtCore.QTimer()
        # self.timer.setInterval(500)
        # self.timer.start()
        # self.timer.timeout.connect(self.iterate_xml(leaf))

        # self.timer.stop()
        # iterate_xml(leaf,main)

        # print(leaf.tag, leaf.attrib, leaf.text)

    # funkcja edytująca nam xml
    def create_xml(self, filename="przykladowy.xml", size=3, history=[]):
        # tree = et.parse('./spam/dict.xml')
        root = et.Element("hex2048", {"board_size": str(size)})  # .getroot()

        player1 = et.Element("player", {"nr": "1"})
        root.append(player1)

        player2 = et.Element("player", {"nr": "2"})
        root.append(player2)

        for el in history:
            if el[0] == "Spawned":
                tmp = et.SubElement(player1, "spawn_value", {"x": str(el[6]), "y": str(el[7])})
                tmp.text = str(el[4])
            if el[0] == "Move":
                tmp = et.SubElement(player1, "move")
                tmp.text = str(el[-1])
            if el[0] == "Score":
                tmp = et.SubElement(player1, "score")
                tmp.text = str(el[-1])
        if filename[:-4] != ".xml":
            output = filename + ".xml"
        else:
            output = filename
        tree = et.ElementTree(root)
        tree.write(output, xml_declaration=True, encoding='utf-8')

    def create_json(self,filename="przyklad.json"):

        pass
    def change_size(self, q, xml=False):
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
        if xml == False:
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
        self.messbox = MessageB(self, "History Last Move")
        # self.dialog = SaveHistory(self,"History")

    def saveConfig(self):
        self.dialog = SaveHistory(self, "Config")

    def autoPlay(self):
        self.messbox = MessageB(self, "Autoplay")

    def emulate(self):
        self.dialog = SaveHistory(self, "Emulate")
        #     read xml
        # do moves
        pass

    def con(self, q):
        if q.text() == "&Nowa gra":
            self.newGame()
        if q.text() == "&Opcje gry" or q.text()=="&Opcje sieciowe":
            self.pop = PopupWindow(self, q.text())
            self.pop.show()
        # if q.text()=="&Opcje sieciowe":
        #     self.pop = PopupWindow(self, q.text())
        #     self.pop.show()
            # self.historia.append("POPUP")
        if q.text() == "&Zapisz historie":
            self.saveHistory()
            # self.dialog.show()
        if q.text() == "&Wyjdz":
            self.exitGame()
        if q.text() == "&Auto rozgrywka":
            self.autoPlay()
        if q.text() == "&Zapisz konfiguracje":
            self.saveConfig()
        if q.text() == "&Emuluj":
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

    def movea(self, xml=False):
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

        if xml == False:
            spawn = self.tic_tac_toe.spawnTile()
            print(spawn)
            self.historia.append(spawn)
            if spawn == "Plansza pełna - przegrałeś grę!":
                self.messbox=MessageB(self,type="Koniec Gry")


    def moveq(self, xml=False):
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

        if xml == False:
            spawn = self.tic_tac_toe.spawnTile()
            print(spawn)
            self.historia.append(spawn)
            if spawn == "Plansza pełna - przegrałeś grę!":
                self.messbox=MessageB(self,type="Koniec Gry")

    def movew(self, xml=False):
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

        if xml == False:
            spawn = self.tic_tac_toe.spawnTile()
            print(spawn)
            self.historia.append(spawn)
            if spawn == "Plansza pełna - przegrałeś grę!":
                self.messbox=MessageB(self,type="Koniec Gry")

    def movee(self, xml=False):

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

        if xml == False:
            spawn = self.tic_tac_toe.spawnTile()
            print(spawn)
            self.historia.append(spawn)
            if spawn == "Plansza pełna - przegrałeś grę!":
                self.messbox=MessageB(self,type="Koniec Gry")

    def moves(self, xml=False):
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

        if xml == False:
            spawn = self.tic_tac_toe.spawnTile()
            print(spawn)
            self.historia.append(spawn)
            if spawn == "Plansza pełna - przegrałeś grę!":
                self.messbox=MessageB(self,type="Koniec Gry")

    def moved(self, xml=False):
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

        if xml == False:
            spawn = self.tic_tac_toe.spawnTile()
            print(spawn)
            self.historia.append(spawn)
            if spawn == "Plansza pełna - przegrałeś grę!":
                self.messbox=MessageB(self,type="Koniec Gry")

    def mousePressEvent(self, event):
        if event.pos().x() < 600 and event.pos().y() < 600:
            self.m_pos_x_pr = event.pos().x()
            self.m_pos_y_pr = event.pos().y()
            self.mouse_pressed = True

    def mouseReleaseEvent(self, event):
        m_pos_x_rel = event.pos().x()
        m_pos_y_rel = event.pos().y()

        if self.mouse_pressed:
            y = m_pos_y_rel - self.m_pos_y_pr
            x = m_pos_x_rel - self.m_pos_x_pr
            angle = math.atan2(-y, x)
            if math.fabs(y) > 100 or math.fabs(x) > 100:
                if angle > 0 and angle < 1 / 3 * math.pi:
                    self.movee()
                if angle > 1 / 3 * math.pi and angle < 2 / 3 * math.pi:
                    self.movew()
                if angle > 2 / 3 * math.pi and angle < math.pi:
                    self.moveq()
                if angle < 0 and angle > -1 / 3 * math.pi:
                    self.moved()
                if angle < -1 / 3 * math.pi and angle > - 2 / 3 * math.pi:
                    self.moves()
                if angle < - 2 / 3 * math.pi and angle > - math.pi:
                    self.movea()
        self.mouse_pressed = False

    def keyPressEvent(self, event):
        key = event.key()
        # 3-2
        # 4-2
        # 5-3
        if key == QtCore.Qt.Key_1:
            spawn = self.tic_tac_toe.spawnTile()
            print(spawn)
            self.historia.append(spawn)
            if spawn == "Plansza pełna - przegrałeś grę!":
                self.messbox=MessageB(self,type="Koniec Gry")

        if key == QtCore.Qt.Key_2:
            spawn = self.gracz_sieciowy.spawnTile()
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
