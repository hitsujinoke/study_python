#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""universalcolor.py"""

from PyQt5.QtGui import QColor

def rgb_to_hex(r, g, b):

    for i in (r, g, b):
        if isinstance(i, int):
            if all(0 <= i <= 255 for i in (r, g, b)):
                return f'#{r:02x}{g:02x}{b:02x}'

            elif any(i < 0 for i in (r, g, b)):
                raise OverflowError("can't convert negative int")
            else:
                raise OverflowError("int too big to convert")
        else:
            raise TypeError('integer argument expected')


red = rgb_to_hex(255, 75, 0)
yellow = rgb_to_hex(255, 241, 0)
green = rgb_to_hex(3, 175, 122)
blue = rgb_to_hex(0, 90, 255)
skyblue = rgb_to_hex(77, 196, 255)
pink = rgb_to_hex(255, 128, 130)
orange = rgb_to_hex(246, 170, 0)
purple = rgb_to_hex(153, 0, 153)
brown = rgb_to_hex(128, 64, 0)

light_pink = rgb_to_hex(255, 202, 191)
cream = rgb_to_hex(255, 255, 128)
light_yellow_green = rgb_to_hex(216, 242, 85)
light_skyblue = rgb_to_hex(191, 228, 255)
beige = rgb_to_hex(255, 202, 128)
light_green = rgb_to_hex(119, 217, 168)
light_purple = rgb_to_hex(201, 172, 230)

white = rgb_to_hex(255, 255, 255)
light_grey = rgb_to_hex(200, 200, 203)
grey = rgb_to_hex(132, 145, 158)
black = rgb_to_hex(0, 0, 0)


qred = QColor(255, 75, 0)
qyellow = QColor(255, 241, 0)
qgreen = QColor(3, 175, 122)
qblue = QColor(0, 90, 255)
qskyblue = QColor(77, 196, 255)
qpink = QColor(255, 128, 130)
qorange = QColor(246, 170, 0)
qpurple = QColor(153, 0, 153)
qbrown = QColor(128, 64, 0)

qlight_pink = QColor(255, 202, 191)
qcream = QColor(255, 255, 128)
qlight_yellow_green = QColor(216, 242, 85)
qlight_skyblue = QColor(191, 228, 255)
qbeige = QColor(255, 202, 128)
qlight_green = QColor(119, 217, 168)
qlight_purple = QColor(201, 172, 230)

qwhite = QColor(255, 255, 255)
qlight_grey = QColor(200, 200, 203)
qgrey = QColor(132, 145, 158)
qblack = QColor(0, 0, 0)