import sys
import random
from PySide2 import QtCore, QtWidgets, QtGui
import numpy as np
import math
# from termcolor import colored


def printRed(text):
    print("\033[91m {}\033[00m" .format(text))

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

    def spawnTile(self):
        x = random.randint(0, 2 * self.size - 2)
        y = random.randint(0, len(self.board[x]) - 1)
        tile_val_int = random.randint(0, 100)
        value = 2
        if tile_val_int < 80:
            value = 2
        else:
            value = 4
        # if(self.board[x])
        # hex=Hexagon()
        while (self.board[x][y].value != 0):
            x = random.randint(0, 2 * self.size - 2)
            y = random.randint(0, len(self.board[x]) - 1)

        # print("Spawned tile of value " + str(value) + ", at: " + str(x) + ", " + str(y))
        output="Spawned tile of value " + str(value) + ", at: " + str(x) + ", " + str(y)
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

    # def mousePressEvent(self, event):
    #     pos = event.pos()
    #     self.select(int(pos.x() / 100), int(pos.y() / 100))
    #     self.update()
    #     super(TicTacToe, self).mousePressEvent(event)

class PopupWindow(QtWidgets.QGraphicsView):
    def __init__(self):
        super(PopupWindow, self).__init__()
        dlg=QtWidgets.QDialog(self)
        dlg.setWindowTitle("HIII")
        dlg.exec()


# coś jest chyba nie tak ze score
class MainWindow(QtWidgets.QGraphicsView):
    def __init__(self):
        super(MainWindow, self).__init__()
        scene = QtWidgets.QGraphicsScene(self)
        self._createActions()
        self._createMenuBar()
        # self._connectActions()
        self.button=QtWidgets.QPushButton("ShowDialog")
        self.button.clicked.connect(self.newDialog())
        # self.button.
        scene.addWidget(self.button)


        # scene.addWidget()

        # rozmiar planszy
        n = 3
        # plansza gracza 1
        self.tic_tac_toe = TicTacToe(n, 250, 150)

        # QTextEdit z historią
        self.historia = QtWidgets.QTextEdit()
        self.historia.setReadOnly(True)
        self.historia.setGeometry(0, 500, 400, 200)

        # wylosowanie mu na początku 2 płytek
        spawn=self.tic_tac_toe.spawnTile()
        print(spawn)
        self.historia.append(spawn)
        spawn=self.tic_tac_toe.spawnTile()
        print(spawn)
        self.historia.append(spawn)
        # gracz sieciowy
        self.gracz_sieciowy = TicTacToe(n, 700, 150)

        # label z wynikiem gracza 1
        self.labelA = QtWidgets.QGraphicsSimpleTextItem()
        self.labelA.setText("Player A Score: ")
        self.labelA.setY(20)
        font = QtGui.QFont("Helvetica", 15, QtGui.QFont.Bold)
        self.labelA.setFont(font)
        scene.addItem(self.labelA)
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
        scene.addItem(self.labelWeb)
        self.labelWebScore = QtWidgets.QGraphicsSimpleTextItem()
        self.labelWebScore.setText(str(self.gracz_sieciowy.score))
        self.labelWebScore.setX(710)
        self.labelWebScore.setY(20)
        self.labelWebScore.setFont(font)

        # dodawanie elementów do sceny
        scene.addWidget(self.historia)
        scene.addItem(self.labelScore)
        scene.addItem(self.labelWebScore)
        scene.addItem(self.tic_tac_toe)
        scene.addItem(self.gracz_sieciowy)
        # scene.setSceneRect(0, 0, 1200, 700)
        self.setScene(scene)
        self.setCacheMode(QtWidgets.QGraphicsView.CacheBackground)
        # self.setWindowTitle("2048 Hexagons are TheBestagons")
    def _createMenuBar(self):
        menubar = QtWidgets.QMenuBar(self)
        option_menu = menubar.addMenu('&Opcje')
        option_menu.addAction(self.newAction)
        # Using a QMenu object
        fileMenu = QtWidgets.QMenu("&File", self)
        menubar.addMenu(fileMenu)
        # Using a title
        editMenu = menubar.addMenu("&Edit")
    def _createActions(self):
        # Creating action using the first constructor
        self.newAction = QtWidgets.QAction(self)
        self.newAction.setText("&New")
        # Creating actions using the second constructor
        self.openAction = QtWidgets.QAction("&Open...", self)
        self.saveAction = QtWidgets.QAction("&Save", self)
        self.exitAction = QtWidgets.QAction("&Exit", self)
        self.copyAction = QtWidgets.QAction("&Copy", self)
        self.pasteAction = QtWidgets.QAction("&Paste", self)
        self.cutAction = QtWidgets.QAction("C&ut", self)
        self.helpContentAction = QtWidgets.QAction("&Help Content", self)
        self.aboutAction = QtWidgets.QAction("&About", self)
    def newDialog(self):
        self.opcjeDialog=QtWidgets.QDialog()
        self.opcjeDialog.show()
    def _connectActions(self):
        self.newAction.connect(self.newDialog())

    def keyPressEvent(self, event):
        key = event.key()
        # 3-2
        # 4-2
        # 5-3
        replays = self.tic_tac_toe.size - self.tic_tac_toe.size // 2
        if key == QtCore.Qt.Key_R:
            self.tic_tac_toe.reset()
        if key == QtCore.Qt.Key_1:
            spawn=self.tic_tac_toe.spawnTile()
            print(spawn)
        if key == QtCore.Qt.Key_2:
            spawn=self.gracz_sieciowy.spawnTile()
            print(spawn)
        if key == QtCore.Qt.Key_A:
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

            spawn=self.tic_tac_toe.spawnTile()
            print(spawn)
            self.historia.append(spawn)

        if key == QtCore.Qt.Key_E:
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

            spawn=self.tic_tac_toe.spawnTile()
            print(spawn)
            self.historia.append(spawn)

        if key == QtCore.Qt.Key_S:
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

            spawn=self.tic_tac_toe.spawnTile()
            print(spawn)
            self.historia.append(spawn)

        if key == QtCore.Qt.Key_W:
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

            spawn=self.tic_tac_toe.spawnTile()
            print(spawn)
            self.historia.append(spawn)

        if key == QtCore.Qt.Key_Q:
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
            self.historia.append(str(self.tic_tac_toe.score))

            spawn=self.tic_tac_toe.spawnTile()
            print(spawn)
            self.historia.append(spawn)

        if key == QtCore.Qt.Key_D:
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
            self.historia.append(str(self.tic_tac_toe.score))

            spawn=self.tic_tac_toe.spawnTile()
            print(spawn)
            self.historia.append(spawn)

        super(MainWindow, self).keyPressEvent(event)


# class Window(QtWidgets.QMainWindow):
#     def __init__(self, parent=None):
#         super().__init__(parent)
#         self.resize(1500, 700)
#         self.setWindowTitle("HALO")
#
#         self._createMenuBar()
#         # self.set
#         self.view=QtWidgets.QGraphicsView()
#         scene = QtWidgets.QGraphicsScene(self)
#         scene.setSceneRect(0,0,1500,700)
#         # rozmiar planszy
#         n = 3
#         # plansza gracza 1
#         self.tic_tac_toe = TicTacToe(n, 250, 150)
#         # wylosowanie mu na początku 2 płytek
#         self.tic_tac_toe.spawnTile()
#         self.tic_tac_toe.spawnTile()
#         # gracz sieciowy
#         self.gracz_sieciowy = TicTacToe(n, 700, 150)
#
#         # label z wynikiem gracza 1
#         self.labelA = QtWidgets.QGraphicsSimpleTextItem()
#         self.labelA.setText("Player A Score: ")
#         font = QtGui.QFont("Helvetica", 15, QtGui.QFont.Bold)
#         self.labelA.setFont(font)
#         scene.addItem(self.labelA)
#         self.labelScore = QtWidgets.QGraphicsSimpleTextItem()
#         self.labelScore.setText(str(self.tic_tac_toe.score))
#         self.labelScore.setX(180)
#         self.labelScore.setFont(font)
#
#         # label z wynikiem gracza sieciowego
#         self.labelWeb = QtWidgets.QGraphicsSimpleTextItem()
#         self.labelWeb.setText("Web Player Score: ")
#         self.labelWeb.setFont(font)
#         self.labelWeb.setX(500)
#         scene.addItem(self.labelWeb)
#         self.labelWebScore = QtWidgets.QGraphicsSimpleTextItem()
#         self.labelWebScore.setText(str(self.gracz_sieciowy.score))
#         self.labelWebScore.setX(710)
#         self.labelWebScore.setFont(font)
#
#         # QTextEdit z historią
#         self.historia=QtWidgets.QTextEdit()
#         self.historia.setReadOnly(True)
#         self.historia.setGeometry(0,500,400,200)
#
#         # dodawanie elementów do sceny
#         scene.addWidget(self.historia)
#         scene.addItem(self.labelScore)
#         scene.addItem(self.labelWebScore)
#         scene.addItem(self.tic_tac_toe)
#         scene.addItem(self.gracz_sieciowy)
#         # scene.setSceneRect(0, 0, 1200, 700)
#         self.view.setScene(scene)
#         self.view.show()
#         # self.view.setCacheMode(QtWidgets.QGraphicsView.CacheBackground)
#         # scene = QtWidgets.QGraphicsScene(self)
#         # scene.addItem(self.view.labelA)
#         # scene.addWidget(self.view.historia)
#         # scene.addItem(self.view.labelScore)
#         # scene.addItem(self.view.labelWebScore)
#         # scene.addItem(self.view.tic_tac_toe)
#         # scene.addItem(self.view.gracz_sieciowy)
#
#         # self.view.show()
#
#     def _createMenuBar(self):
#         menuBar=QtWidgets.QMenuBar(self)
#
#         fileMenu=QtWidgets.QMenu("&File",self)
#         menuBar.addMenu(fileMenu)
#
#         editMenu = menuBar.addMenu("&Edit")
#         helpMenu = menuBar.addMenu("&Help")
#
#         self.setMenuBar(menuBar)
#     def keyPressEvent(self, event):
#         key = event.key()
#         # 3-2
#         # 4-2
#         # 5-3
#         replays=self.tic_tac_toe.size-self.tic_tac_toe.size//2
#         if key == QtCore.Qt.Key_R:
#             self.tic_tac_toe.reset()
#         if key == QtCore.Qt.Key_1:
#             self.tic_tac_toe.spawnTile()
#         if key == QtCore.Qt.Key_2:
#             self.gracz_sieciowy.spawnTile()
#         if key == QtCore.Qt.Key_A:
#             self.tic_tac_toe.moves(direction="left_down")
#             changed=self.tic_tac_toe.merge(direction="left_down")
#             while replays > 0 and changed==True:
#                 self.tic_tac_toe.moves(direction="left_down")
#                 changed=self.tic_tac_toe.merge(direction="left_down")
#                 replays-=1
#             print("Moved all tiles left_down")
#             self.historia.append("Score = "+str(self.tic_tac_toe.score))
#             print("Score = "+str(self.tic_tac_toe.score))
#             self.labelScore.setText(str(self.tic_tac_toe.score))
#             self.tic_tac_toe.spawnTile()
#         if key == QtCore.Qt.Key_E:
#             self.tic_tac_toe.moves(direction="right_up")
#             changed=self.tic_tac_toe.merge(direction="right_up")
#             while replays > 0 and changed == True:
#                 self.tic_tac_toe.moves(direction="right_up")
#                 changed = self.tic_tac_toe.merge(direction="right_up")
#                 replays -= 1
#             print("Moved all tiles right_up")
#             print("Score = " + str(self.tic_tac_toe.score))
#             self.labelScore.setText(str(self.tic_tac_toe.score))
#             self.tic_tac_toe.spawnTile()
#         if key == QtCore.Qt.Key_S:
#             self.tic_tac_toe.moves(direction="down")
#             changed=self.tic_tac_toe.merge(direction="down")
#             while replays > 0 and changed == True:
#                 self.tic_tac_toe.moves(direction="down")
#                 changed = self.tic_tac_toe.merge(direction="down")
#                 replays -= 1
#             print("Moved all tiles down")
#             print("Score = " + str(self.tic_tac_toe.score))
#             self.labelScore.setText(str(self.tic_tac_toe.score))
#             self.tic_tac_toe.spawnTile()
#         if key == QtCore.Qt.Key_W:
#             self.tic_tac_toe.moves(direction="up")
#             changed=self.tic_tac_toe.merge(direction="up")
#             while replays > 0 and changed == True:
#                 self.tic_tac_toe.moves(direction="up")
#                 changed = self.tic_tac_toe.merge(direction="up")
#                 replays -= 1
#             print("Moved all tiles up")
#             print("Score = " + str(self.tic_tac_toe.score))
#             self.labelScore.setText(str(self.tic_tac_toe.score))
#             self.tic_tac_toe.spawnTile()
#         if key == QtCore.Qt.Key_Q:
#             self.tic_tac_toe.moves(direction="left_up")
#             changed=self.tic_tac_toe.merge(direction="left_up")
#             while replays > 0 and changed == True:
#                 self.tic_tac_toe.moves(direction="left_up")
#                 changed = self.tic_tac_toe.merge(direction="left_up")
#                 replays -= 1
#             print("Moved all tiles left_up")
#             print("Score = " + str(self.tic_tac_toe.score))
#             self.labelScore.setText(str(self.tic_tac_toe.score))
#             self.tic_tac_toe.spawnTile()
#         if key == QtCore.Qt.Key_D:
#             self.tic_tac_toe.moves(direction="right_down")
#             changed=self.tic_tac_toe.merge(direction="right_down")
#             while replays > 0 and changed == True:
#                 self.tic_tac_toe.moves(direction="right_down")
#                 changed = self.tic_tac_toe.merge(direction="right_down")
#                 replays -= 1
#             print("Moved all tiles right_down")
#             print("Score = " + str(self.tic_tac_toe.score))
#             self.labelScore.setText(str(self.tic_tac_toe.score))
#             self.tic_tac_toe.spawnTile()
#         super(Window, self).keyPressEvent(event)
if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    window = MainWindow()
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