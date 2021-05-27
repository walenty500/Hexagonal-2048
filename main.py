# Krzysztof Walentukiewicz
# 175478
# Hex 2048

# wykonane podpunkty:
# blokada ruchu dla gry 2 osobowej
# komunikaty w konsoli
# działająca gra 2osobowa

# aby odpalić grę 2osobowa nalezy odpalic skrypt bashowy
# bash run.sh

# albo w dwoch konsolach odpalic plik 175478_Walentukiewicz_Krzysztof
# wtedy czytelnosc konsoli bedzie lepsza

import sys
import random
from PySide2 import QtCore, QtWidgets, QtGui
import numpy as np
import math
import xml.etree.ElementTree as et
import os
import json
import socket
import threading
import argparse
import subprocess


# funkcja wypisująca tekst w konsoli na czerwono
def printRed(text):
    print("\033[91m {}\033[00m".format(text))


# funkcja wypisująca tekst w konsoli na zielono
def printGreen(text):
    print("\033[92m {}\033[00m".format(text))


# klasa pojedynczego pola - hexa
class Hexagon(QtWidgets.QGraphicsItem):
    def __init__(self, x=0, y=0, z=0, x_start=250, y_start=150):
        super().__init__()
        self.size = 30
        self.x_center = x_start
        self.y_center = y_start
        # indexy w 3D
        self.x = x
        self.y = y
        self.z = z
        self.value = 0

    def boundingRect(self):
        return QtCore.QRectF(0, 0, 1200, 700)

    # metoda zbierająca punkty składające się na hexagon i zwracająca je
    def paint(self, painter, option, widget, x_start, y_start):
        punkty = []
        for i in range(6):
            t = 60 * i
            x = x_start + self.size * math.cos(math.radians(t))
            y = y_start + self.size * math.sin(math.radians(t))
            punkty.append(QtCore.QPointF(x, y))
        return painter.drawPolygon(punkty)

    # metoda wypisująca wartość hexa
    def write_val(self, painter):
        if self.value != 0:
            rect = QtCore.QRectF(self.x_center - self.size, self.y_center - self.size, 2 * self.size, 2 * self.size)
            painter.setFont(QtGui.QFont('Helvetica', 18))
            if self.value > 512:
                painter.setFont(QtGui.QFont('Helvetica', 18))
            painter.drawText(rect, QtCore.Qt.AlignCenter, str(self.value))


# klasa zawierajaca całą planszę gracza
class HexBoard(QtWidgets.QGraphicsItem):
    def __init__(self, n=3, x_start=250, y_start=150):
        super(HexBoard, self).__init__()

        # tworzenie planszy
        b = []
        whole_board = np.array([])
        row = []
        # plansza to 2*n-1 rzędów, na początku rzędy rosną - mają n, n+1, n+2 elementów
        for i in range(n):
            for j in range(n + i):
                row.append(Hexagon(x=i, y=j, z=-(-i + j - n + 1)))
            row = np.array(row, dtype=object)
            whole_board = np.append(whole_board, row)
            b.append(row)
            row = []
        offset = 0
        # następnie maleją, od n-tego rzędu do 2n-1
        for i in range(1, n):
            offset += 1
            for j in range(2 * n - 1 - i):
                row.append(Hexagon(x=(n - 1 + i), y=offset + j, z=((n - 1 + i) - (j + offset) + n - 1)))
            row = np.array(row, dtype=object)
            whole_board = np.append(whole_board, row)
            b.append(row)
            row = []

        # tworzenie tablic dla indexów dla y i z
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

        self.nr_of_elem = 0
        for i in range(n, 2 * n - 1):
            self.nr_of_elem += 2 * i
        self.nr_of_elem += 2 * n - 1
        self.size = n
        self.score = 0
        self.board = b
        self.y_board = b_y
        self.z_board = b_z
        self.x_start = x_start
        self.y_start = y_start
        self.full_board = False
        self.win_condition = False

    # metoda sprawdzająca czy gra została wygrana
    def check_if_2048(self):
        for j in range(len(self.board)):
            for i in range(len(self.board[j])):
                if self.board[j][i].value == 2048:
                    self.win_condition = True

    # metoda sprawdzajaca czy gra została przegrana
    def check_if_board_full(self):
        counter = 0

        for j in range(len(self.board)):
            for i in range(len(self.board[j])):
                if self.board[j][i].value != 0:
                    counter += 1
        if counter == self.nr_of_elem:
            self.full_board = True
            print("Plansza pełna")

    # metoda rysujaca hexy na planszy
    def paint(self, painter, option, widget):
        # painter.setBrush(QtGui.QColor(204, 192, 179, 127))

        x = self.x_start
        y = self.y_start

        for j in range(len(self.board)):
            for i in range(len(self.board[j])):
                # wybieranie koloru w zaleznosci od wartosci hexa
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

                # rysowanie gornej czesci planszy
                if j / self.size < 1:
                    self.board[j][i].x_center = (
                            (x + j * 1.5 * (self.board[j][i].size)) - (i * 1.5 * (self.board[j][i].size)))
                    self.board[j][i].y_center = ((y + j * self.board[j][i].size / 2 * math.sqrt(3)) + (
                            i * self.board[j][i].size / 2 * math.sqrt(3)))

                    self.board[j][i].paint(painter, option, widget, self.board[j][i].x_center,
                                           self.board[j][i].y_center)
                    self.board[j][i].write_val(painter)

                # rysowanie dolnej czesci planszy
                else:
                    self.board[j][i].x_center = ((x + (self.size - 1) * 1.5 * (self.board[j][i].size)) - (
                            i * 1.5 * (self.board[j][i].size)))
                    self.board[j][i].y_center = (
                            (y + (j - self.size / 2 + 0.5) * self.board[j][i].size * math.sqrt(3)) + (
                            i * self.board[j][i].size / 2 * math.sqrt(3)))

                    self.board[j][i].paint(painter, option, widget, self.board[j][i].x_center,
                                           self.board[j][i].y_center)
                    self.board[j][i].write_val(painter)

    # tworzenie nowych hexów
    # jeżeli wywołujemy metodę z argumentami, oznacza to że emulujemy
    # więc nie potrzeba losować
    def spawnTile(self, x_in=-1, y_in=-1, val=0):
        if x_in == -1 and y_in == -1:
            x = random.randint(0, 2 * self.size - 2)
            y = random.randint(0, len(self.board[x]) - 1)

        # losowanie z prawdopodobienstwem 80% - 2
        # 20% - 4
        tile_val_int = random.randint(0, 100)
        if val == 0:
            if tile_val_int < 80:
                value = 2
            else:
                value = 4
        else:
            value = val

        self.check_if_board_full()
        if self.full_board == False:
            if x_in == -1 and y_in == -1:
                while (self.board[x][y].value != 0):
                    x = random.randint(0, 2 * self.size - 2)
                    y = random.randint(0, len(self.board[x]) - 1)
            else:
                x = x_in
                y = y_in

            output = "Spawned tile of value " + str(value) + ", at: " + str(x) + ", " + str(y)
            self.board[x][y].value = value
            self.update()
        else:
            output = "Plansza pełna - przegrałeś grę!"
            print("Pełna tablica")

        return output

    # logika ruchów w zależności od kierunków
    # przechodzimy po rzędach i "ściągamy" hexy od/do końca na pierwsza wolna pozycje
    def moves(self, direction):
        if direction == "left_down":
            for j in range(len(self.board) - 1, -1, -1):
                free_pos = len(self.board[j]) - 1
                for i in range(len(self.board[j]) - 1, -1, -1):
                    if self.board[j][i].value != 0:
                        self.board[j][free_pos].value = self.board[j][i].value
                        if free_pos != i:
                            self.board[j][i].value = 0
                        free_pos -= 1

        if direction == "right_up":
            for j in range(len(self.board)):
                free_pos = 0
                for i in range(len(self.board[j])):
                    if self.board[j][i].value != 0:
                        self.board[j][free_pos].value = self.board[j][i].value
                        if free_pos != i:
                            self.board[j][i].value = 0
                        free_pos += 1

        if direction == "down":
            for j in range(len(self.z_board) - 1, -1, -1):
                free_pos = len(self.z_board[j]) - 1
                for i in range(len(self.z_board[j]) - 1, -1, -1):
                    if self.z_board[j][i].value != 0:
                        self.z_board[j][free_pos].value = self.z_board[j][i].value
                        if free_pos != i:
                            self.z_board[j][i].value = 0
                        free_pos -= 1

        if direction == "up":
            for j in range(len(self.z_board)):
                free_pos = 0
                for i in range(len(self.z_board[j])):
                    if self.z_board[j][i].value != 0:
                        self.z_board[j][free_pos].value = self.z_board[j][i].value
                        if free_pos != i:
                            self.z_board[j][i].value = 0
                        free_pos += 1

        if direction == "right_down":
            for j in range(len(self.y_board) - 1, -1, -1):
                free_pos = len(self.y_board[j]) - 1
                for i in range(len(self.y_board[j]) - 1, -1, -1):
                    if self.y_board[j][i].value != 0:
                        self.y_board[j][free_pos].value = self.y_board[j][i].value
                        if free_pos != i:
                            self.y_board[j][i].value = 0
                        free_pos -= 1

        if direction == "left_up":
            for j in range(len(self.y_board)):
                free_pos = 0
                for i in range(len(self.y_board[j])):
                    if self.y_board[j][i].value != 0:
                        self.y_board[j][free_pos].value = self.y_board[j][i].value
                        if free_pos != i:
                            self.y_board[j][i].value = 0
                        free_pos += 1

        self.update()

    # łączenie hexów, jeżeli wykonano ruch w odpowiednią stronę i moga się połączyć
    def merge(self, direction):
        if direction == "left_down":
            ifmerged = False
            for j in range(len(self.board) - 1, -1, -1):
                for i in range(len(self.board[j]) - 1, 0, -1):
                    if self.board[j][i].value == self.board[j][i - 1].value and self.board[j][i].value != 0:
                        self.board[j][i].value *= 2
                        self.board[j][i - 1].value = 0
                        ifmerged = True
                        self.score += self.board[j][i].value
            return ifmerged
        if direction == "right_up":
            ifmerged = False
            for j in range(len(self.board)):
                for i in range(len(self.board[j]) - 1):
                    if self.board[j][i].value == self.board[j][i + 1].value and self.board[j][
                        i].value != 0:
                        self.board[j][i].value *= 2
                        self.board[j][i + 1].value = 0
                        ifmerged = True
                        self.score += self.board[j][i].value
            return ifmerged
        if direction == "up":
            ifmerged = False
            for j in range(len(self.z_board)):
                for i in range(len(self.z_board[j]) - 1):
                    if self.z_board[j][i].value == self.z_board[j][i + 1].value and self.z_board[j][
                        i].value != 0:
                        self.z_board[j][i].value *= 2
                        self.z_board[j][i + 1].value = 0
                        ifmerged = True
                        self.score += self.z_board[j][i].value
            return ifmerged
        if direction == "down":
            ifmerged = False
            for j in range(len(self.z_board) - 1, -1, -1):
                for i in range(len(self.z_board[j]) - 1, 0, -1):
                    if self.z_board[j][i].value == self.z_board[j][i - 1].value and self.z_board[j][
                        i].value != 0:
                        self.z_board[j][i].value *= 2
                        self.z_board[j][i - 1].value = 0
                        ifmerged = True
                        self.score += self.z_board[j][i].value
            return ifmerged
        if direction == "left_up":
            ifmerged = False
            for j in range(len(self.y_board)):
                for i in range(len(self.y_board[j]) - 1):
                    if self.y_board[j][i].value == self.y_board[j][i - 1].value and self.y_board[j][
                        i].value != 0:
                        self.y_board[j][i].value *= 2
                        self.y_board[j][i - 1].value = 0
                        ifmerged = True
                        self.score += self.y_board[j][i].value
            return ifmerged
        if direction == "right_down":
            ifmerged = False
            for j in range(len(self.y_board) - 1, -1, -1):
                for i in range(len(self.y_board[j]) - 1, 0, -1):
                    if self.y_board[j][i].value == self.y_board[j][i - 1].value and self.y_board[j][
                        i].value != 0:
                        self.y_board[j][i].value *= 2
                        self.y_board[j][i - 1].value = 0
                        ifmerged = True
                        self.score += self.y_board[j][i].value
            return ifmerged

    def boundingRect(self):
        return QtCore.QRectF(0, 0, 1200, 700)



# Okienko z opcjami gry i sieciowymi
class PopupWindow(QtWidgets.QDialog):
    def __init__(self, main, type):
        super(PopupWindow, self).__init__()
        self.main_window = main
        if type == "&Opcje gry":
            self.game()
        if type == "&Opcje sieciowe":
            self.net()

    # opcje sieciowe
    def net(self):
        net_name = QtWidgets.QLabel("Nazwa przeciwnika: ")
        self.net_player = QtWidgets.QLineEdit()
        self.net_player.setPlaceholderText(self.main_window.web_name)
        self.net_player.textChanged.connect(self.main_window.change_web_name)
        ip = QtWidgets.QLabel("Adres IP: ")
        self.ip = QtWidgets.QLineEdit()
        self.ip.setText(self.main_window.host)
        self.ip.textChanged.connect(self.main_window.change_ip)
        port = QtWidgets.QLabel("Port połączenia: ")
        self.port = QtWidgets.QLineEdit()
        self.port.setText(str(self.main_window.port))
        self.port.textChanged.connect(self.main_window.change_port)
        self.wyszukaj = QtWidgets.QPushButton()
        self.wyszukaj.setText("Wyszukaj gracza\nw sieci lokalnej")
        self.polacz = QtWidgets.QPushButton()
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

    # opcje gry
    def game(self):
        player_name = QtWidgets.QLabel("Wybierz swoją nazwę: ")
        self.player = QtWidgets.QLineEdit()
        self.player.setPlaceholderText(self.main_window.name)
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


# klasa obsługująca otwieranie/zapisywanie do pliku
class SaveHistory(QtWidgets.QFileDialog):
    def __init__(self, main, type):
        super(SaveHistory, self).__init__()
        # zapisywanie historii
        if type == "History":
            self.filename, _ = self.getSaveFileName(self, "Save game history", "history.xml", "XML File (*.xml)")
            try:
                text = main.historia.toPlainText()
                splited = text.splitlines()
                splited_words = []
                for el in splited:
                    tmp = el.split()
                    splited_words.append(tmp)
                main.create_xml(self.filename, splited_words)
            except:
                print("Nie zapisano historii gry!")
                out = MessageB(self, "History")

        # zapisywanie historii bez ostatniego ruchu
        if type == "History Last Move":
            self.filename, _ = self.getSaveFileName(self, "Save game history", "history.xml", "XML File (*.xml)")
            try:
                text = main.historia.toPlainText()
                splited = text.splitlines()
                splited_words = []
                for el in splited:
                    tmp = el.split()
                    splited_words.append(tmp)
                splited_words_last_move = splited_words[:-3]
                main.create_xml(self.filename, splited_words_last_move)
            except:
                print("Nie zapisano historii gry!")
                out = MessageB(self, "History")

        # zapisywanie konfiguracji
        if type == "Config":
            try:
                main.create_json()
            except:
                print("Nie zapisano konfiguracji gry!")
                out = MessageB(self, "Config")

        # odczytywanie historii do emulowania
        if type == "Emulate":
            self.filename, _ = self.getOpenFileNames(self, "Select a xml file with game history to emulate", "",
                                                     "XML Files (*.xml)")
            try:
                baza = self.filename[0]
                main.read_xml(baza)
            except:
                print("Nie otworzono pliku xml do emulowania!")
                out = MessageB(self, "Emulate")

# klasa z messageboxami
class MessageB(QtWidgets.QMessageBox):
    def __init__(self, main, type):
        super(MessageB, self).__init__()
        # messagebox informujący o wygranej
        if type == "Wygrana":
            self.setText("Brawo - WYGRAŁEŚ!")
            self.setInformativeText("Kliknij Ok, aby rozpocząć nową grę\nalbo Cancel aby wyjść z gry.")
            self.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
            self.setDefaultButton(QtWidgets.QMessageBox.Ok)
            ret = self.exec_()
            # jeśli cancel - koniec gry
            if ret == QtWidgets.QMessageBox.Cancel:
                main.close()
            #     jeśli ok, stworzenie nowej gry
            else:
                # resetowanie score'a
                main.labelScore.setText(str(0))
                text = main.historia.toPlainText()
                splited = text.splitlines()
                splited_words = []
                for el in splited:
                    tmp = el.split()
                    splited_words.append(tmp)
                # automatycznie zapisywanie historii ostatniej gry
                main.create_xml(filename="last_save.xml", history=splited_words)

                # schowanie, usunięcie i wyczyszczenie planszy i historii
                main.tic_tac_toe.hide()
                main.gracz_sieciowy.hide()
                main.historia.clear()

                del main.tic_tac_toe
                main.tic_tac_toe = HexBoard(int(main.size), 250, 100)

                # zespawnowanie 2 hexów na początek gry
                spawn = main.tic_tac_toe.spawnTile()
                print(spawn)
                main.historia.append(spawn)

                spawn = main.tic_tac_toe.spawnTile()
                print(spawn)
                main.historia.append(spawn)

                del main.gracz_sieciowy
                main.gracz_sieciowy = HexBoard(int(main.size), 800, 100)

                main.scene.addItem(main.tic_tac_toe)
                main.scene.addItem(main.gracz_sieciowy)
                main.scene.update()

        # messagebox informujący o wyjściu z gry
        if type == "Exit":
            self.setText("Czy na pewno chcesz zamknąć?")
            self.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
            self.setDefaultButton(QtWidgets.QMessageBox.Cancel)
            ret = self.exec_()

            if ret == QtWidgets.QMessageBox.Cancel:
                self.close()
            else:
                main.close()

        # messagebox informujący o nowej grze
        if type == "Nowa":
            self.setText("Czy na pewno chcesz uruchomić grę na nowo?")
            self.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
            self.setDefaultButton(QtWidgets.QMessageBox.Cancel)
            ret = self.exec_()

            if ret == QtWidgets.QMessageBox.Cancel:
                self.close()
            else:
                main.labelScore.setText(str(0))
                text = main.historia.toPlainText()
                splited = text.splitlines()
                splited_words = []
                for el in splited:
                    tmp = el.split()
                    splited_words.append(tmp)
                main.create_xml(filename="last_save.xml", history=splited_words)
                main.tic_tac_toe.hide()
                main.gracz_sieciowy.hide()
                main.historia.clear()

                del main.tic_tac_toe
                main.tic_tac_toe = HexBoard(int(main.size), 250, 100)

                spawn = main.tic_tac_toe.spawnTile()
                print(spawn)
                main.historia.append(spawn)

                spawn = main.tic_tac_toe.spawnTile()
                print(spawn)
                main.historia.append(spawn)

                del main.gracz_sieciowy
                main.gracz_sieciowy = HexBoard(int(main.size), 800, 100)

                main.scene.addItem(main.tic_tac_toe)
                main.scene.addItem(main.gracz_sieciowy)
                main.scene.update()

        # messagebox informujący o nie zapisaniu historii
        if type == "History":
            self.setText("NIE ZAPISANO HISTORII GRY!")
            self.setStandardButtons(QtWidgets.QMessageBox.Ok)
            self.setDefaultButton(QtWidgets.QMessageBox.Ok)
            ret = self.exec_()

            if ret == QtWidgets.QMessageBox.Cancel:
                self.close()

        # messagebox informujący o możliwosci zapisu gry bez ostatniego ruchu
        if type == "History Last Move":
            self.setText("Czy chcesz zapisac gre bez ostatniego ruchu?")
            self.setInformativeText("Ok - zapisanie bez ostatniego ruchu,\nCancel - zapisanie całej historii.")
            self.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
            self.setDefaultButton(QtWidgets.QMessageBox.Cancel)
            ret = self.exec_()

            if ret == QtWidgets.QMessageBox.Ok:
                pop = SaveHistory(main, "History Last Move")
                self.close()
            else:
                pop = SaveHistory(main, "History")
                self.close()

        # messagebox informujący o koncu gry - przegranej
        if type == "Koniec Gry":
            self.setText("Koniec Gry - zacząć nową grę?")
            self.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
            self.setDefaultButton(QtWidgets.QMessageBox.Ok)
            ret = self.exec_()

            if ret == QtWidgets.QMessageBox.Cancel:
                main.close()
            else:
                main.labelScore.setText(str(0))
                text = main.historia.toPlainText()
                main.score = 0
                splited = text.splitlines()
                splited_words = []
                for el in splited:
                    tmp = el.split()
                    splited_words.append(tmp)
                main.create_xml(filename="last_save.xml", history=splited_words)
                main.tic_tac_toe.hide()
                main.gracz_sieciowy.hide()
                main.historia.clear()

                del main.tic_tac_toe
                main.tic_tac_toe = HexBoard(int(main.size), 250, 100)

                spawn = main.tic_tac_toe.spawnTile()
                print(spawn)
                main.historia.append(spawn)

                spawn = main.tic_tac_toe.spawnTile()
                print(spawn)
                main.historia.append(spawn)

                del main.gracz_sieciowy
                main.gracz_sieciowy = HexBoard(int(main.size), 800, 100)

                main.scene.addItem(main.tic_tac_toe)
                main.scene.addItem(main.gracz_sieciowy)
                main.scene.update()

        # messagebox informujący o błędzie zapisywania konfiguracji
        if type == "Config":
            self.setText("NIE ZAPISANO KONFIGURACJI GRY!")
            self.setStandardButtons(QtWidgets.QMessageBox.Ok)
            self.setDefaultButton(QtWidgets.QMessageBox.Ok)
            ret = self.exec_()

            if ret == QtWidgets.QMessageBox.Cancel:
                self.close()

        # messagebox informujący o błędzie wczytywania historii do emulowania
        if type == "Emulate":
            self.setText("NIE OTWORZONO PLIKU DO EMULOWANIA!")
            self.setStandardButtons(QtWidgets.QMessageBox.Ok)
            self.setDefaultButton(QtWidgets.QMessageBox.Ok)
            ret = self.exec_()

            if ret == QtWidgets.QMessageBox.Cancel:
                self.close()

        # messagebox informujący o wgraniu złego pliku
        if type == "Wrong File":
            self.setText("Podano zły plik!")
            self.setStandardButtons(QtWidgets.QMessageBox.Ok)
            self.setDefaultButton(QtWidgets.QMessageBox.Ok)
            ret = self.exec_()

            if ret == QtWidgets.QMessageBox.Cancel:
                self.close()

        # messagebox informujacy o podaniu złego pliku historii
        if type == "Wrong XML":
            self.setText("Podano niepoprawny plik xml!")
            self.setInformativeText("To nie jest historia gry.")
            self.setStandardButtons(QtWidgets.QMessageBox.Ok)
            self.setDefaultButton(QtWidgets.QMessageBox.Ok)
            ret = self.exec_()

            if ret == QtWidgets.QMessageBox.Cancel:
                self.close()

        # messagebox informujący o tym ze tu bedzie automatyczna rozgrywka
        if type == "Autoplay":
            self.setText("Tutaj bedzie sie automatycznie rozgrywać gra")
            self.setStandardButtons(QtWidgets.QMessageBox.Ok)
            self.setDefaultButton(QtWidgets.QMessageBox.Ok)
            ret = self.exec_()

            if ret == QtWidgets.QMessageBox.Cancel:
                self.close()


# klasa głównego okna
class MainWindow(QtWidgets.QGraphicsView):
    def __init__(self, n=3):
        super(MainWindow, self).__init__()
        self.scene = QtWidgets.QGraphicsScene(self)
        self.host = '127.0.0.1'
        self.port = 8080
        self.name = "Player A"
        self.web_name = "Web Player"
        self.size = n
        # pole służące do kontrolowania gestami myszy
        self.mouse_pressed = False

        # listy i timery do emulowania
        self.leaf_list = []
        self.iterator = 0
        self.timer = QtCore.QTimer()
        self.timer.setInterval(500)
        self.timer_allow = False

        # plansza gracza 1
        self.tic_tac_toe = HexBoard(int(self.size), 250, 100)

        # skomentowany kod do gry sieciowej

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 5)
        self.naglowek=1024
        self.naglowek_size=5
        self.initialSpawn=[]
        try:
            self.sock.connect((self.host, self.port))
            self.role = "Client"
            self.can_move=True
        except:
            self.sock.bind((self.host, self.port))
            self.role = "Server"
            self.can_move=False
            self.clients = []
            self.sock.listen()
        print(self.role)

        # stworzenie menu bar z rozwijaną listą opcji do wyboru
        self._createActions()
        self._createMenuBar()

        # wybranie każdej opcji wysyła sygnał, który łaczy sie z metodą con
        self.option_menu.triggered[QtWidgets.QAction].connect(self.con)

        # QTextEdit z historią
        self.historia = QtWidgets.QTextEdit()
        self.historia.setReadOnly(True)
        self.historia.setGeometry(0, 600, 400, 200)

        # wylosowanie mu na początku 2 płytek
        spawn = self.tic_tac_toe.spawnTile()

        # kod do gry sieciowej

        if self.role == "Client":
            self.writeClient(spawn)
        if self.role =="Server":
            self.initialSpawn.append(spawn)
            self.broadcast(("Server sends "+spawn).encode(encoding='utf-8'))

        print(spawn)
        # wypisywanie do konsoli i przekierowywanie na kontrolkę QTextEdit
        self.historia.append(spawn)
        spawn = self.tic_tac_toe.spawnTile()

        # kod do gry sieciowej

        if self.role == "Client":
            self.writeClient(spawn)
        if self.role =="Server":
            self.initialSpawn.append(spawn)
            self.broadcast(("Server sends "+spawn).encode(encoding='utf-8'))
        print(spawn)
        self.historia.append(spawn)

        # plansza gracza sieciowego
        self.gracz_sieciowy = HexBoard(n, 800, 100)

        # label z nazwą i wynikiem gracza 1
        self.labelA = QtWidgets.QGraphicsSimpleTextItem()
        self.labelA.setText(self.name + " Score: ")
        self.labelA.setX(0)
        self.labelA.setY(20)
        font = QtGui.QFont("Helvetica", 15, QtGui.QFont.Bold)
        self.labelA.setFont(font)
        self.scene.addItem(self.labelA)
        self.labelScore = QtWidgets.QGraphicsSimpleTextItem()
        self.labelScore.setText(str(self.tic_tac_toe.score))
        self.labelScore.setX(0)
        self.labelScore.setY(50)
        self.labelScore.setFont(font)

        # label z nazwą i wynikiem gracza sieciowego
        self.labelWeb = QtWidgets.QGraphicsSimpleTextItem()
        self.labelWeb.setText(self.web_name + " Score: ")
        self.labelWeb.setFont(font)
        self.labelWeb.setX(500)
        self.labelWeb.setY(20)
        self.scene.addItem(self.labelWeb)
        self.labelWebScore = QtWidgets.QGraphicsSimpleTextItem()
        self.labelWebScore.setText(str(self.gracz_sieciowy.score))
        self.labelWebScore.setX(500)
        self.labelWebScore.setY(50)
        self.labelWebScore.setFont(font)

        # dodawanie elementów do sceny
        self.scene.addWidget(self.historia)
        self.scene.addItem(self.labelScore)
        self.scene.addItem(self.labelWebScore)
        self.scene.addItem(self.tic_tac_toe)
        self.scene.addItem(self.gracz_sieciowy)
        self.setScene(self.scene)
        self.setCacheMode(QtWidgets.QGraphicsView.CacheBackground)
        self.setWindowTitle("2048 Hexagonal Version")


        # Przyciski
        self.newGameButton = QtWidgets.QPushButton("New\nGame", self)
        self.newGameButton.setGeometry(750, 700, 100, 60)
        self.newGameButton.clicked.connect(self.newGame)

        self.exitGameButton = QtWidgets.QPushButton("Exit", self)
        self.exitGameButton.setGeometry(750, 780, 100, 60)
        self.exitGameButton.clicked.connect(self.exitGame)

        self.saveGameHistoryButton = QtWidgets.QPushButton("Save\nHistory", self)
        self.saveGameHistoryButton.setGeometry(870, 700, 100, 60)
        self.saveGameHistoryButton.clicked.connect(self.saveHistory)

        self.saveConfigButton = QtWidgets.QPushButton("Save\nConfig", self)
        self.saveConfigButton.setGeometry(990, 700, 100, 60)
        self.saveConfigButton.clicked.connect(self.saveConfig)

        self.saveConfigButton = QtWidgets.QPushButton("Load\nConfig", self)
        self.saveConfigButton.setGeometry(990, 780, 100, 60)
        self.saveConfigButton.clicked.connect(self.read_json)

        self.autoPlayButton = QtWidgets.QPushButton("Auto\nPlay", self)
        self.autoPlayButton.setGeometry(1100, 700, 100, 60)
        self.autoPlayButton.clicked.connect(self.autoPlay)

        self.emulateButton = QtWidgets.QPushButton("Emulate", self)
        self.emulateButton.setGeometry(870, 780, 100, 60)
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

        # kod gry sieciowej

        if self.role == "Server":
            self.receive_thread = threading.Thread(target=self.receiveServ,daemon=True)
            self.receive_thread.start()

        if self.role == "Client":
            self.receive_thread = threading.Thread(target=self.receiveClient,daemon=True)
            self.receive_thread.start()

        # self.write_thread=threading.Thread(target=self.write)
        # self.write_thread.start()

    # metoda zmieniająca port
    def change_port(self, q):
        try:
            self.port = int(q)
        except:
            print("Niepoprawny port")

    # metoda zmieniająca ip
    def change_ip(self, q):
        self.host = q

    # metoda zmieniająca nazwę gracza sieciowego
    def change_web_name(self, q):
        self.web_name = q
        self.labelWeb.setText(self.web_name + " Score: ")

    # metoda zmieniająca nazwę gracza
    def change_name(self, q):
        self.name = q
        self.labelA.setText(self.name + " Score: ")

    # przy zamykaniu gry tworzymy save
    def closeEvent(self, event):
        text = self.historia.toPlainText()
        splited = text.splitlines()
        splited_words = []
        for el in splited:
            tmp = el.split()
            splited_words.append(tmp)
        self.create_xml(filename="last_save.xml", history=splited_words)
        # self.receive_thread=0
        # if self.role=="Server":
        #     self.handle_thread=0

    # metody do gry sieciowej

    def writeClient(self, mess):
        # while True:
        # tresc wiadomosci
        # a=mess
        # words=a.split()
        # struktura wiadomosci, ktora wysylamy wszystkim
        self.can_move=False
        message = self.role + ' sends ' + mess
        naglowek = len(message)
        rozmiar_nagl = str(len(message))
        while len(rozmiar_nagl) != self.naglowek_size:
            rozmiar_nagl = "0" + rozmiar_nagl

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
                conv = message.decode('utf-8')
                # wypisywanie jej w terminalu osoby
                a = message
                words = a.split()
                if words[0]=="Server".encode('utf-8'):
                    self.can_move=True
                    print(conv)
                    self.historia.append(conv)
                    if words[2] == "Spawned".encode('utf-8'):
                        x = int(words[8].decode('utf-8')[:-1])
                        y = int(words[9].decode('utf-8'))
                        val = int(words[6].decode('utf-8')[:-1])
                        self.gracz_sieciowy.spawnTile(x, y, val)
                    if words[2] == "Move".encode('utf-8'):
                        if words[5] == "left_down".encode('utf-8'):
                            self.moveaweb()
                        if words[5] == "left_up".encode('utf-8'):
                            self.moveqweb()
                        if words[5] == "up".encode('utf-8'):
                            self.movewweb()
                        if words[5] == "down".encode('utf-8'):
                            self.movesweb()
                        if words[5] == "right_up".encode('utf-8'):
                            self.moveeweb()
                        if words[5] == "right_down".encode('utf-8'):
                            self.movedweb()
                # to robi pisanie u klienta tego co zrobil
                # self.historia.append(conv)
            except:
                # gdy z jakiegos powodu nastapi blad
                print("An error occured!")
                # zamykamy polaczenie
                self.sock.close()
                break

    # wysyłanei do wszystkich uzytkowników odebranej wiadomości
    def broadcast(self, message):
        a=message
        words=a.split()
        if words[0]=="Client".encode('utf-8'):
            self.can_move = True
            print(message.decode('utf-8'))
            self.historia.append(message.decode('utf-8'))
            if words[2]=="Spawned".encode('utf-8'):
                x=int(words[8].decode('utf-8')[:-1])
                y=int(words[9].decode('utf-8'))
                val=int(words[6].decode('utf-8')[:-1])
                self.gracz_sieciowy.spawnTile(x,y,val)
            if words[2]=="Move".encode('utf-8'):
                if words[5]=="left_down".encode('utf-8'):
                    self.moveaweb()
                if words[5] == "left_up".encode('utf-8'):
                    self.moveqweb()
                if words[5]=="up".encode('utf-8'):
                    self.movewweb()
                if words[5]=="down".encode('utf-8'):
                    self.movesweb()
                if words[5]=="right_up".encode('utf-8'):
                    self.moveeweb()
                if words[5]=="right_down".encode('utf-8'):
                    self.movedweb()

        if words[0] == "Server".encode('utf-8'):
            self.can_move=False
            rozmiar_nagl = str(len(message))
            while len(rozmiar_nagl) != self.naglowek_size:
                rozmiar_nagl = "0" + rozmiar_nagl

        if len(self.clients)==0:
            self.can_move=True

        for client in self.clients:
            rozmiar_nagl = str(len(message))
            while len(rozmiar_nagl) != self.naglowek_size:
                rozmiar_nagl = "0" + rozmiar_nagl
            client.send(rozmiar_nagl.encode('utf-8'))
            client.send(message)
        # obsluga wiadomosci i plikow

    def handle(self, client):
        while True:
            try:
                # odbieranie wiadomości
                nagl = client.recv(5)
                nagl = int(nagl.decode())
                message = client.recv(nagl)
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
            for el in self.initialSpawn:
                self.broadcast(("Server sends "+el).encode(encoding='utf-8'))

            # wiadomosc dla klienta ze sie połaczył
            # client.send('Connected!'.encode('utf-8'))

            # obsługa wątku przychodzacych wiadomosci i ich ewentualnego rozsylania
            self.handle_thread = threading.Thread(target=self.handle, args=(client,), daemon=True)
            self.handle_thread.start()

    # metoda służąca do emulowania
    def iterate_xml(self):
        if self.timer_allow == True:
            # przy każdym wywołaniu funkcji metoda odwołuje się do kolejnego indexu
            # listy elementów z xml, przez co występuje animacja ruchów
            if self.leaf_list[self.iterator].tag == "spawn_value":
                x = int(self.leaf_list[self.iterator].attrib["x"][:-1])
                y = int(self.leaf_list[self.iterator].attrib["y"])
                value = int(self.leaf_list[self.iterator].text[:-1])
                spawn = self.tic_tac_toe.spawnTile(x, y, value)
                self.historia.append(spawn)
                print(spawn)
            if self.leaf_list[self.iterator].tag == "move":
                if self.leaf_list[self.iterator].text == "up":
                    # atrybut xml=True pozwala na poruszanie się bez spawnowania dodatkowych hexów
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

    # metoda odczytująca zawartość xml'a
    def read_xml(self, filename="przykladowy.xml"):
        try:
            self.tree = et.parse(filename)
            self.root = self.tree.getroot()
            self.iterator = 0

            # sprawdzanie czy xml jest odpowiedni
            tag = True
            tmp = self.root.tag
            if tmp != "hex2048":
                tag = False
            attr = False
            atributes = self.root.attrib
            if atributes == {'board_size': '3'} or atributes == {'board_size': '4'} or atributes == {'board_size': '5'}:
                attr = True

            if attr == True:
                size = self.root.attrib["board_size"]

            # tworzenie listy elementów z xml'a po których później będziemy iterować
            if attr == True and tag == True:
                self.leaf_list = []
                self.timer_allow = True
                self.change_size(size, xml=True)
                for child in self.root:
                    for leaf in child:
                        self.leaf_list.append(leaf)

                # odpalenie timera, który wywołuje metodę co pół sekundy
                self.timer_allow = True
                self.timer.timeout.connect(self.iterate_xml)
                self.timer.start()
            else:
                self.messbox = MessageB(self, type="Wrong XML")
        except:
            self.messbox = MessageB(self, type="Wrong File")

    # funkcja tworząca plik xml
    def create_xml(self, filename="przykladowy.xml", history=[]):
        root = et.Element("hex2048", {"board_size": str(self.size)})  # .getroot()

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
        if filename[-4:] != ".xml":
            output = filename + ".xml"
        else:
            output = filename
        tree = et.ElementTree(root)
        tree.write(output, xml_declaration=True, encoding='utf-8')

    # odczytywanie pliku .json
    def read_json(self):
        try:
            read_config = open("config.json", "r")
            data = json.load(read_config)
            read_config.close()
            self.name = data["name"]
            self.web_name = data["web_name"]
            self.host = data["ip"]
            self.port = data["port"]
            self.labelA.setText(self.name + " Score: ")
            self.labelWeb.setText(self.web_name + " Score: ")
            print("Plik z konfiguracją wczytany")
        except:
            print("Cos poszło nie tak z czytaniem jsona")

    # tworzenie pliku json
    def create_json(self):
        try:
            read_config = open("config.json", "r")
            data = json.load(read_config)
            read_config.close()
            data["best_3"].append(self.tic_tac_toe.score)
            data["best_3"].sort()
            data["best_3"].reverse()
            data["best_3"] = data["best_3"][:3]
            data["name"] = self.name
            data["web_name"] = self.web_name
            data["ip"] = self.host
            data["port"] = self.port
            output_file = open("config.json", "w")
            json.dump(data, output_file, indent=4)
            output_file.close()
            print("Plik z konfiguracją zmodyfikowany")
        except:
            output_file = open("config.json", "w")
            config_data = {"name": self.name,
                           "web_name": self.web_name,
                           "ip": self.host,
                           "port": self.port,
                           "best_3": [self.tic_tac_toe.score]}
            json.dump(config_data, output_file, indent=4)
            output_file.close()
            print("Plik z konfiguracją stworzony")

    # metoda zmieniajaca rozmiar planszy
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

        self.labelScore.setText("0")
        self.tic_tac_toe = HexBoard(int(self.size), 250, 100)
        if xml == False:
            spawn = self.tic_tac_toe.spawnTile()
            print(spawn)
            self.historia.append(spawn)
            spawn = self.tic_tac_toe.spawnTile()
            print(spawn)
            self.historia.append(spawn)
        self.gracz_sieciowy = HexBoard(int(self.size), 800, 100)
        self.scene.addItem(self.tic_tac_toe)
        self.scene.addItem(self.gracz_sieciowy)
        self.scene.update()

    # metody wywołujące messageboxy
    def newGame(self):
        self.messbox = MessageB(self, "Nowa")

    def exitGame(self):
        self.messbox = MessageB(self, "Exit")

    def saveHistory(self):
        self.messbox = MessageB(self, "History Last Move")

    def saveConfig(self):
        self.dialog = SaveHistory(self, "Config")

    def autoPlay(self):
        self.messbox = MessageB(self, "Autoplay")

    def emulate(self):
        self.dialog = SaveHistory(self, "Emulate")

    # metoda obsługująca sygnały z opcji menubar
    def con(self, q):
        if q.text() == "&Nowa gra":
            self.newGame()
        if q.text() == "&Opcje gry" or q.text() == "&Opcje sieciowe":
            self.pop = PopupWindow(self, q.text())
            self.pop.show()
        if q.text() == "&Wczytaj konfiguracje":
            self.read_json()
        if q.text() == "&Zapisz historie":
            self.saveHistory()
        if q.text() == "&Wyjdz":
            self.exitGame()
        if q.text() == "&Auto rozgrywka":
            self.autoPlay()
        if q.text() == "&Zapisz konfiguracje":
            self.saveConfig()
        if q.text() == "&Emuluj":
            self.emulate()

    # metoda tworząca menubar i jego strukturę
    def _createMenuBar(self):
        self.menubar = QtWidgets.QMenuBar(self)
        self.option_menu = self.menubar.addMenu('&Opcje')
        self.option_menu.addAction(self.newGameAction)
        self.option_menu.addAction(self.newAction)
        self.option_menu.addAction(self.netAction)
        self.option_menu.addAction(self.saveConfigAction)
        self.option_menu.addAction(self.saveHistoryAction)
        self.option_menu.addAction(self.loadConfig)
        self.option_menu.addAction(self.loadAction)
        self.option_menu.addAction(self.autoplayAction)
        self.option_menu.addAction(self.exitAction)

    # metoda tworząca opcje menubar'a
    def _createActions(self):
        self.newAction = QtWidgets.QAction(self)
        self.newAction.setText("&Opcje gry")
        self.newGameAction = QtWidgets.QAction("&Nowa gra", self)
        self.netAction = QtWidgets.QAction("&Opcje sieciowe", self)
        self.saveHistoryAction = QtWidgets.QAction("&Zapisz historie", self)
        self.saveConfigAction = QtWidgets.QAction("&Zapisz konfiguracje", self)
        self.loadAction = QtWidgets.QAction("&Emuluj", self)
        self.loadConfig = QtWidgets.QAction("&Wczytaj konfiguracje", self)
        self.exitAction = QtWidgets.QAction("&Wyjdz", self)
        self.autoplayAction = QtWidgets.QAction("&Auto rozgrywka", self)

    # metody poszczególnych ruchów - te same metody co w HexBoard
    # służace do obsługi przycisków
    def movea(self, xml=False):
        if self.can_move==True:
            replays = self.tic_tac_toe.size - self.tic_tac_toe.size // 2

            self.tic_tac_toe.moves(direction="left_down")
            changed = self.tic_tac_toe.merge(direction="left_down")
            while replays > 0 and changed == True:
                self.tic_tac_toe.moves(direction="left_down")
                changed = self.tic_tac_toe.merge(direction="left_down")
                replays -= 1

            printRed("Moved all tiles left_down")
            self.historia.append("Move direction = left_down")
            if self.role == "Client":
                self.writeClient("Move direction = left_down")
            if self.role == "Server":
                self.broadcast("Server sends Move direction = left_down".encode(encoding='utf-8'))

            printGreen("Score = " + str(self.tic_tac_toe.score))
            self.historia.append("Score = " + str(self.tic_tac_toe.score))
            self.labelScore.setText(str(self.tic_tac_toe.score))

            self.tic_tac_toe.check_if_2048()
            if xml == False:
                spawn = self.tic_tac_toe.spawnTile()
                if self.role == "Client":
                    self.writeClient(spawn)
                if self.role == "Server":
                    self.broadcast(("Server sends "+spawn).encode(encoding='utf-8'))
                print(spawn)
                self.historia.append(spawn)
                if self.tic_tac_toe.win_condition == True:
                    self.messbox = MessageB(self, type="Wygrana")
                if spawn == "Plansza pełna - przegrałeś grę!":
                    self.messbox = MessageB(self, type="Koniec Gry")

    def moveq(self, xml=False):
        if self.can_move==True:
            replays = self.tic_tac_toe.size - self.tic_tac_toe.size // 2
            self.tic_tac_toe.moves(direction="left_up")
            changed = self.tic_tac_toe.merge(direction="left_up")
            while replays > 0 and changed == True:
                self.tic_tac_toe.moves(direction="left_up")
                changed = self.tic_tac_toe.merge(direction="left_up")
                replays -= 1

            printRed("Moved all tiles left_up")
            self.historia.append("Move direction = left_up")
            if self.role == "Client":
                self.writeClient("Move direction = left_up")
            if self.role == "Server":
                self.broadcast("Server sends Move direction = left_up".encode(encoding='utf-8'))

            printGreen("Score = " + str(self.tic_tac_toe.score))
            self.labelScore.setText(str(self.tic_tac_toe.score))
            self.historia.append("Score = " + str(self.tic_tac_toe.score))

            self.tic_tac_toe.check_if_2048()
            if xml == False:
                spawn = self.tic_tac_toe.spawnTile()
                print(spawn)
                if self.role == "Client":
                    self.writeClient(spawn)
                if self.role == "Server":
                    self.broadcast(("Server sends "+spawn).encode(encoding='utf-8'))
                self.historia.append(spawn)
                if self.tic_tac_toe.win_condition == True:
                    self.messbox = MessageB(self, type="Wygrana")
                    if spawn == "Plansza pełna - przegrałeś grę!":
                        self.messbox = MessageB(self, type="Koniec Gry")

    def movew(self, xml=False):
        if self.can_move==True:
            replays = self.tic_tac_toe.size - self.tic_tac_toe.size // 2
            self.tic_tac_toe.moves(direction="up")
            changed = self.tic_tac_toe.merge(direction="up")
            while replays > 0 and changed == True:
                self.tic_tac_toe.moves(direction="up")
                changed = self.tic_tac_toe.merge(direction="up")
                replays -= 1

            printRed("Moved all tiles up")
            self.historia.append("Move direction = up")
            if self.role == "Client":
                self.writeClient("Move direction = up")
            if self.role == "Server":
                self.broadcast("Server sends Move direction = up".encode(encoding='utf-8'))

            printGreen("Score = " + str(self.tic_tac_toe.score))
            self.labelScore.setText(str(self.tic_tac_toe.score))
            self.historia.append("Score = " + str(self.tic_tac_toe.score))

            self.tic_tac_toe.check_if_2048()
            if xml == False:
                spawn = self.tic_tac_toe.spawnTile()
                print(spawn)
                if self.role == "Client":
                    self.writeClient(spawn)
                if self.role == "Server":
                    self.broadcast(("Server sends "+spawn).encode(encoding='utf-8'))
                self.historia.append(spawn)
                if self.tic_tac_toe.win_condition == True:
                    self.messbox = MessageB(self, type="Wygrana")
                if spawn == "Plansza pełna - przegrałeś grę!":
                    self.messbox = MessageB(self, type="Koniec Gry")

    def movee(self, xml=False):
        if self.can_move==True:
            replays = self.tic_tac_toe.size - self.tic_tac_toe.size // 2
            self.tic_tac_toe.moves(direction="right_up")
            changed = self.tic_tac_toe.merge(direction="right_up")
            while replays > 0 and changed == True:
                self.tic_tac_toe.moves(direction="right_up")
                changed = self.tic_tac_toe.merge(direction="right_up")
                replays -= 1

            printRed("Moved all tiles right_up")
            self.historia.append("Move direction = right_up")
            if self.role == "Client":
                self.writeClient("Move direction = right_up")
            if self.role == "Server":
                self.broadcast("Server sends Move direction = right_up".encode(encoding='utf-8'))

            printGreen("Score = " + str(self.tic_tac_toe.score))
            self.labelScore.setText(str(self.tic_tac_toe.score))
            self.historia.append("Score = " + str(self.tic_tac_toe.score))

            self.tic_tac_toe.check_if_2048()
            if xml == False:
                spawn = self.tic_tac_toe.spawnTile()
                print(spawn)
                if self.role == "Client":
                    self.writeClient(spawn)
                if self.role == "Server":
                    self.broadcast(("Server sends "+spawn).encode(encoding='utf-8'))
                self.historia.append(spawn)
                if self.tic_tac_toe.win_condition == True:
                    self.messbox = MessageB(self, type="Wygrana")
                if spawn == "Plansza pełna - przegrałeś grę!":
                    self.messbox = MessageB(self, type="Koniec Gry")

    def moves(self, xml=False):
        if self.can_move==True:
            replays = self.tic_tac_toe.size - self.tic_tac_toe.size // 2
            self.tic_tac_toe.moves(direction="down")
            changed = self.tic_tac_toe.merge(direction="down")
            while replays > 0 and changed == True:
                self.tic_tac_toe.moves(direction="down")
                changed = self.tic_tac_toe.merge(direction="down")
                replays -= 1

            printRed("Moved all tiles down")
            self.historia.append("Move direction = down")
            if self.role == "Client":
                self.writeClient("Move direction = down")
            if self.role == "Server":
                self.broadcast("Server sends Move direction = down".encode(encoding='utf-8'))

            printGreen("Score = " + str(self.tic_tac_toe.score))
            self.labelScore.setText(str(self.tic_tac_toe.score))
            self.historia.append("Score = " + str(self.tic_tac_toe.score))

            self.tic_tac_toe.check_if_2048()
            if xml == False:
                spawn = self.tic_tac_toe.spawnTile()
                print(spawn)
                if self.role == "Client":
                    self.writeClient(spawn)
                if self.role == "Server":
                    self.broadcast(("Server sends "+spawn).encode(encoding='utf-8'))
                self.historia.append(spawn)
                if self.tic_tac_toe.win_condition == True:
                    self.messbox = MessageB(self, type="Wygrana")
                if spawn == "Plansza pełna - przegrałeś grę!":
                    self.messbox = MessageB(self, type="Koniec Gry")

    def moved(self, xml=False):
        if self.can_move==True:
            replays = self.tic_tac_toe.size - self.tic_tac_toe.size // 2
            self.tic_tac_toe.moves(direction="right_down")
            changed = self.tic_tac_toe.merge(direction="right_down")
            while replays > 0 and changed == True:
                self.tic_tac_toe.moves(direction="right_down")
                changed = self.tic_tac_toe.merge(direction="right_down")
                replays -= 1

            printRed("Moved all tiles right_down")
            self.historia.append("Move direction = right_down")
            if self.role == "Client":
                self.writeClient("Move direction = right_down")
            if self.role == "Server":
                self.broadcast("Server sends Move direction = right_down".encode(encoding='utf-8'))

            printGreen("Score = " + str(self.tic_tac_toe.score))
            self.labelScore.setText(str(self.tic_tac_toe.score))
            self.historia.append("Score = " + str(self.tic_tac_toe.score))

            self.tic_tac_toe.check_if_2048()
            if xml == False:
                spawn = self.tic_tac_toe.spawnTile()
                print(spawn)
                if self.role == "Client":
                    self.writeClient(spawn)
                if self.role == "Server":
                    self.broadcast(("Server sends "+spawn).encode(encoding='utf-8'))
                self.historia.append(spawn)
                if self.tic_tac_toe.win_condition == True:
                    self.messbox = MessageB(self, type="Wygrana")
                if spawn == "Plansza pełna - przegrałeś grę!":
                    self.messbox = MessageB(self, type="Koniec Gry")

    # wykrycie kliknięcia na obszarze planszy pierwszego gracza
    def mousePressEvent(self, event):
        if event.pos().x() < 750 and event.pos().y() < 700:
            self.mouse_position_x_press = event.pos().x()
            self.mouse_position_y_press = event.pos().y()
            self.mouse_pressed = True

    # wykrycie puszczenia przycisku myszy na planszy pierwszego gracza
    def mouseReleaseEvent(self, event):
        mouse_position_release_x = event.pos().x()
        mouse_position_release_y = event.pos().y()

        # jeżeli został kliknięty przycisk
        if self.mouse_pressed:
            # obliczamy gdzie się myszka przemieściła po puszczeniu przycisku
            y = mouse_position_release_y - self.mouse_position_y_press
            x = mouse_position_release_x - self.mouse_position_x_press
            # obliczamy kąt
            angle = math.atan2(-y, x)
            # w zależności od kąta wykonujemy ruch
            if math.fabs(y) > 100 or math.fabs(x) > 100:
                if angle > 2 / 3 * math.pi and angle < math.pi:
                    self.moveq()
                if angle > 1 / 3 * math.pi and angle < 2 / 3 * math.pi:
                    self.movew()
                if angle > 0 and angle < 1 / 3 * math.pi:
                    self.movee()
                if angle < - 2 / 3 * math.pi and angle > - math.pi:
                    self.movea()
                if angle < -1 / 3 * math.pi and angle > - 2 / 3 * math.pi:
                    self.moves()
                if angle < 0 and angle > -1 / 3 * math.pi:
                    self.moved()

        self.mouse_pressed = False




   # metody poszczególnych ruchów - te same metody co w HexBoard
    # służace do obsługi gracza sieciowego
    def moveaweb(self, xml=False):
        replays = self.gracz_sieciowy.size - self.gracz_sieciowy.size // 2

        self.gracz_sieciowy.moves(direction="left_down")
        changed = self.gracz_sieciowy.merge(direction="left_down")
        while replays > 0 and changed == True:
            self.gracz_sieciowy.moves(direction="left_down")
            changed = self.gracz_sieciowy.merge(direction="left_down")
            replays -= 1

        self.labelWebScore.setText(str(self.gracz_sieciowy.score))


    def moveqweb(self, xml=False):
        replays = self.gracz_sieciowy.size - self.gracz_sieciowy.size // 2
        self.gracz_sieciowy.moves(direction="left_up")
        changed = self.gracz_sieciowy.merge(direction="left_up")
        while replays > 0 and changed == True:
            self.gracz_sieciowy.moves(direction="left_up")
            changed = self.gracz_sieciowy.merge(direction="left_up")
            replays -= 1


        self.labelWebScore.setText(str(self.gracz_sieciowy.score))


    def movewweb(self, xml=False):
        replays = self.gracz_sieciowy.size - self.gracz_sieciowy.size // 2
        self.gracz_sieciowy.moves(direction="up")
        changed = self.gracz_sieciowy.merge(direction="up")
        while replays > 0 and changed == True:
            self.gracz_sieciowy.moves(direction="up")
            changed = self.gracz_sieciowy.merge(direction="up")
            replays -= 1

        self.labelWebScore.setText(str(self.gracz_sieciowy.score))

    def moveeweb(self, xml=False):

        replays = self.gracz_sieciowy.size - self.gracz_sieciowy.size // 2
        self.gracz_sieciowy.moves(direction="right_up")
        changed = self.gracz_sieciowy.merge(direction="right_up")
        while replays > 0 and changed == True:
            self.gracz_sieciowy.moves(direction="right_up")
            changed = self.gracz_sieciowy.merge(direction="right_up")
            replays -= 1

        self.labelWebScore.setText(str(self.gracz_sieciowy.score))

    def movesweb(self, xml=False):
        replays = self.gracz_sieciowy.size - self.gracz_sieciowy.size // 2
        self.gracz_sieciowy.moves(direction="down")
        changed = self.gracz_sieciowy.merge(direction="down")
        while replays > 0 and changed == True:
            self.gracz_sieciowy.moves(direction="down")
            changed = self.gracz_sieciowy.merge(direction="down")
            replays -= 1

        self.labelWebScore.setText(str(self.gracz_sieciowy.score))

    def movedweb(self, xml=False):
        replays = self.gracz_sieciowy.size - self.gracz_sieciowy.size // 2
        self.gracz_sieciowy.moves(direction="right_down")
        changed = self.gracz_sieciowy.merge(direction="right_down")
        while replays > 0 and changed == True:
            self.gracz_sieciowy.moves(direction="right_down")
            changed = self.gracz_sieciowy.merge(direction="right_down")
            replays -= 1

        self.labelWebScore.setText(str(self.gracz_sieciowy.score))

if __name__ == "__main__":

    app = QtWidgets.QApplication([])

    window = MainWindow()
    window.setGeometry(100, 100, 1350, 900)
    window.show()

    sys.exit(app.exec_())
