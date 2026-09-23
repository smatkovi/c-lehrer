# -*- coding: utf-8 -*-
"""Draws what the learner's program printed.

QtQuick 1.1 has no Canvas -- that arrived with QtQuick 2 -- so the picture is
painted here with QPainter and handed to QML as a PNG.

The picture is the actual teacher in the numerics chapters: an explicit
Euler step visibly gains energy, a time step past the stability limit visibly
explodes. Reading that in a sentence convinces nobody; watching the curve
leave the screen does. So the axes always autoscale to the data, including
when the data is absurd.
"""
import os

import config

WIDTH, HEIGHT = 620, 400
MARGIN_L, MARGIN_R, MARGIN_T, MARGIN_B = 62, 14, 14, 40

COLOURS = ["#5aa9ff", "#ffb14e", "#7ee787", "#ff6b6b", "#c792ea"]
BACKGROUND = "#101014"
AXIS = "#8a8a95"
GRID = "#26262e"
TEXT = "#d8d8e0"


def _nice_step(span, target):
    """A grid spacing a person would have chosen."""
    if span <= 0:
        return 1.0
    import math
    rough = span / float(target)
    power = math.floor(math.log10(rough))
    base = 10.0 ** power
    for factor in (1.0, 2.0, 2.5, 5.0, 10.0):
        if base * factor >= rough:
            return base * factor
    return base * 10.0


def draw(series, path=None, title=""):
    """series: [(name, [(x, y), ...]), ...]. Returns the file written."""
    from PySide.QtGui import (QImage, QPainter, QColor, QPen, QFont,
                              QPainterPath)
    from PySide.QtCore import Qt, QPointF

    if path is None:
        if not os.path.isdir(config.CACHE):
            os.makedirs(config.CACHE, 0755)
        path = os.path.join(config.CACHE, "plot.png")

    image = QImage(WIDTH, HEIGHT, QImage.Format_ARGB32)
    image.fill(QColor(BACKGROUND))
    painter = QPainter(image)
    painter.setRenderHint(QPainter.Antialiasing, True)

    points = []
    for _, data in series:
        points.extend(data)
    if not points:
        painter.setPen(QColor(TEXT))
        painter.drawText(20, 30, "Nichts zu zeichnen")
        painter.end()
        image.save(path, "PNG")
        return path

    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    # A diverging run produces inf/nan; keep the plot drawable and let the
    # scale show how far things went.
    ys = [y for y in ys if y == y and abs(y) < 1e30] or [0.0]
    x0, x1 = min(xs), max(xs)
    y0, y1 = min(ys), max(ys)
    if x1 - x0 < 1e-12:
        x0, x1 = x0 - 1.0, x1 + 1.0
    if y1 - y0 < 1e-12:
        y0, y1 = y0 - 1.0, y1 + 1.0
    pad = (y1 - y0) * 0.08
    y0, y1 = y0 - pad, y1 + pad

    plot_w = WIDTH - MARGIN_L - MARGIN_R
    plot_h = HEIGHT - MARGIN_T - MARGIN_B

    def sx(x):
        return MARGIN_L + (x - x0) / (x1 - x0) * plot_w

    def sy(y):
        if y != y:
            y = y1
        y = max(min(y, y1), y0)
        return MARGIN_T + plot_h - (y - y0) / (y1 - y0) * plot_h

    font = QFont("Nokia Pure Text", 11)
    painter.setFont(font)

    # grid and labels
    painter.setPen(QPen(QColor(GRID), 1))
    step_y = _nice_step(y1 - y0, 5)
    import math
    tick = math.ceil(y0 / step_y) * step_y
    while tick <= y1:
        painter.setPen(QPen(QColor(GRID), 1))
        painter.drawLine(MARGIN_L, sy(tick), WIDTH - MARGIN_R, sy(tick))
        painter.setPen(QColor(TEXT))
        label = ("%g" % tick)
        painter.drawText(4, sy(tick) + 4, MARGIN_L - 10, 14,
                         Qt.AlignRight | Qt.AlignVCenter, label)
        tick += step_y

    step_x = _nice_step(x1 - x0, 5)
    tick = math.ceil(x0 / step_x) * step_x
    while tick <= x1:
        painter.setPen(QPen(QColor(GRID), 1))
        painter.drawLine(sx(tick), MARGIN_T, sx(tick), MARGIN_T + plot_h)
        painter.setPen(QColor(TEXT))
        painter.drawText(sx(tick) - 40, HEIGHT - MARGIN_B + 4, 80, 16,
                         Qt.AlignHCenter | Qt.AlignTop, "%g" % tick)
        tick += step_x

    painter.setPen(QPen(QColor(AXIS), 1))
    painter.drawLine(MARGIN_L, MARGIN_T, MARGIN_L, MARGIN_T + plot_h)
    painter.drawLine(MARGIN_L, MARGIN_T + plot_h, WIDTH - MARGIN_R, MARGIN_T + plot_h)

    for index in range(len(series)):
        name, data = series[index]
        colour = QColor(COLOURS[index % len(COLOURS)])
        painter.setPen(QPen(colour, 2))
        route = QPainterPath()
        started = False
        for x, y in data:
            if y != y or abs(y) > 1e30:
                started = False          # a gap rather than a wild jump
                continue
            if not started:
                route.moveTo(QPointF(sx(x), sy(y)))
                started = True
            else:
                route.lineTo(QPointF(sx(x), sy(y)))
        painter.drawPath(route)
        if name:
            painter.setPen(colour)
            painter.drawText(MARGIN_L + 10, MARGIN_T + 16 + index * 16, name)

    if title:
        painter.setPen(QColor(TEXT))
        painter.drawText(MARGIN_L, MARGIN_T + plot_h + 28, title)

    painter.end()
    image.save(path, "PNG")
    return path
