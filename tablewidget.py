
import configparser
import sys
import traceback

import pandas as pd
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QHBoxLayout, QPushButton,
                             QTableWidget, QTableWidgetItem, QVBoxLayout,
                             QWidget)

import universalcolor as uc


class Config(object):

    def __init__(self, fname=None):
        if fname is not None:
            self.read(fname)

    def read(self, fname):
        cfg = configparser.ConfigParser()
        cfg.read(fname)
        self._read_dtype_section(cfg['MMAP'])
        self.setting = cfg['SETTING']

    def _read_dtype_section(self, dtype_section):
        self.nbytes, self.dtypes, self.names = dict(), dict(), dict()

        for k, i in dtype_section.items():
            key = (int(k[:3], 16), int(k[3], 16))
            items = i.split(',')
            try:
                self.nbytes[key] = int(items[0])
            except ValueError:
                self.nbytes[key] = pd.np.nan
            self.dtypes[key] = items[1].strip()
            self.names[key] = items[2].strip()


class MemoryMapTableWidget(QWidget):
    def __init__(self, config=None, parent=None):
        super().__init__(parent)
        fname = './config.ini'
        if config is None:
            self.config = Config(fname)
        elif isinstance(config, Config):
            self.config = config
        else:
            raise TypeError('config must be an instance of Config.')

        self.max_column = int(self.config.setting['max_column'])
        self.max_row = int(self.config.setting['max_row'])

        self.tablewidget = QTableWidget(self.max_row, self.max_column)

        horizontalHeaderLabels = (f'   _{i:X}  ' for i in range(self.max_column))
        self.tablewidget.setHorizontalHeaderLabels(horizontalHeaderLabels)
        verticalHeaderLabels = (f'{i:02X}0' for i in range(self.max_row))
        self.tablewidget.setVerticalHeaderLabels(verticalHeaderLabels)

        self.tablewidget.resizeColumnsToContents()
        self.tablewidget.resizeRowsToContents()
        self.tablewidget.cellChanged.connect(self.cell_changed)

        for(i, j), n in self.config.nbytes.items():
            if isinstance(n, int):
                if n > 1:
                    self.tablewidget.setSpan(i, j, 1, n)
                elif n == 1:
                    pass
                else:
                    raise ValueError
            else:
                continue

        layout = QHBoxLayout()
        layout.addWidget(self.tablewidget)
        self.setLayout(layout)
        self.setWindowTitle('MemoryMap')

    def set_data(self, data):
        for i, n in enumerate(data):
            for j, m in enumerate(n):
                item = QTableWidgetItem(str(m))
                item.setTextAlignment(Qt.AlignCenter)
                try:
                    item.setToolTip(self.config.names[(i, j)])
                except KeyError:
                    pass
                self.tablewidget.setItem(i, j, item)

    def cell_changed(self, i, j):
        item =  self.tablewidget.item(i, j)

        try:
            dtype = self.config.dtypes[(i, j)]
        except KeyError:
            return

        nbytes = self.config.nbytes[(i, j)]

        if dtype == 'signed int':
            if nbytes == 1:
                item.setBackground(uc.qlight_skyblue)
            else:
                item.setBackground(uc.qskyblue)
            try:
                n = int(item.text())
                n = n.to_bytes(nbytes, 'big', signed=True)
                n = int.from_bytes(n, 'big', signed=False)
                s = format(n, f'0{nbytes*2}X')
                assert len(s) == nbytes * 2
            except Exception:
                traceback.print_exc()
                item.setForeground(uc.qred)
            else:
                item.setForeground(uc.qblack)
        elif dtype == 'unsigned int':
            if nbytes == 1:
                item.setBackground(uc.qcream)
            else:
                item.setBackground(uc.qlight_purple)
            try:
                n = int(item.text())
                s = format(n, f'0{nbytes*2}X')
                assert len(s) == nbytes * 2
                assert n >= 0
            except Exception:
                traceback.print_exc()
                item.setForeground(uc.qred)
            else:
                item.setForeground(uc.qblack)
        elif dtype == 'ascii':
            item.setBackground(uc.qpink)
            try:
                s = item.text()
                n = ord(s)
                assert 0 <= n <= 255
            except Exception:
                item.setForeground(uc.qred)
            else:
                item.setForeground(uc.qblack)
        elif dtype == 'bool':
            item.setBackground(uc.qbeige)
        elif dtype == 'bcd':
            item.setBackground(uc.qlight_green)
            try:
                s = item.text()
                assert len(s) <= nbytes * 2
                s = format(int(s), f'0{nbytes*2}')
                assert item.text().isnumeric()
                assert len(s) == nbytes * 2
            except (AssertionError, ValueError):
                item.setForeground(uc.qred)
            else:
                item.setForeground(uc.qblack)

class MemoMapWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        fname = './config.ini'
        self.config = Config(fname)
        self.initUI()

    def initUI(self):
        self.readBtn = QPushButton('READ')
        self.writeBtn = QPushButton('WRITE')
        self.saveBtn = QPushButton('SAVE')
        self.clearBtn = QPushButton('CLEAR')
        self.readBtn.clicked.connect(self.read)
        self.writeBtn.clicked.connect(self.write)
        self.saveBtn.clicked.connect(self.save)
        self.clearBtn.clicked.connect(self.clear)

        self.memomaptable = MemoryMapTableWidget(self.config)

        btnLayout = QVBoxLayout()
        btnLayout.addWidget(self.readBtn)
        btnLayout.addWidget(self.writeBtn)
        btnLayout.addWidget(self.saveBtn)
        btnLayout.addWidget(self.clearBtn)
        btnLayout.addStretch(1)

        layout = QHBoxLayout()
        layout.addLayout(btnLayout)
        layout.addWidget(self.memomaptable)

        self.setLayout(layout)
        self.setWindowTitle('MemoryMap')

    def read(self):
        data = [[f'FF' for j in range(self.memomaptable.max_column)]
                for i in range(self.memomaptable.max_row)]

        for (i, j), dtype in self.config.dtypes.items():
            n = self.config.nbytes[(i, j)]
            if isinstance(n, int):
                if n >= 1:
                    s = str()
                    for k in range(n):
                        s += data[i][j+k]

                    if dtype == 'unsigned int':
                        data[i][j] = int(s, 16)
                    elif dtype == 'signed int':
                        s = int(s, 16)
                        b = s.to_bytes(n, 'big', signed=False)
                        s = int.from_bytes(b, 'big', signed=True)
                        data[i][j] = s
                    elif dtype == 'ascii':
                        c = chr(int(s, 16))
                        data[i][j] = c
                    elif dtype in ['hex', 'bcd', 'bool']:
                        data[i][j] = s
                else:
                    raise ValueError
            else:
                continue

        self.memomaptable.set_data(data)
        # self.memomaptable.update()

    def write(self):
        """"""
        # self.memomaptable.tablewidget.

    def save(self):
        for i in range(self.memomaptable.max_row):
            text = f'{i:02X} :'
            for j in range(self.memomaptable.max_column):
                text += f', {int(self.memomaptable.tablewidget.item(i, j).text(), 16):02X}'
            print(text)

    def clear(self):
        pass


def main():

    app = QApplication(sys.argv)
    widget = MemoMapWindow()
    # widget.memomaptable.set_data(data)
    widget.setMinimumWidth(750)
    widget.setMinimumHeight(500)
    widget.show()
    widget.raise_()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
