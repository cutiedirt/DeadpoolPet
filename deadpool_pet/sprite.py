# -*- coding: utf-8 -*-
"""Static Deadpool sprite rendering with a gentle breathing scale."""

import math
import os

from PySide6.QtCore import QPointF, QRectF, Qt
from PySide6.QtGui import QImage, QPainter

_ASSET_DIR = os.path.join(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))), "assets")
_sprite_cache = None


def sprite_path():
    return os.path.join(_ASSET_DIR, "sprite.png")


def load_sprite():
    global _sprite_cache
    if _sprite_cache is None:
        _sprite_cache = QImage(sprite_path())
    return _sprite_cache


def breathe_scale(t, amplitude=0.0345, period=4.0):
    """Gentle breathing: scale in [1-a, 1+a]; max/min AREA ratio stays
    within (1+a)/(1-a) squared <= 1.15 for a <= ~0.0345."""
    return 1.0 + amplitude * math.sin(2 * math.pi * t / period)


def paint(p: QPainter, rect, t: float, dy=0.0, scale=1.0):
    """Draw the sprite centered in `rect`, optionally lifted by dy (px)
    and scaled around its center."""
    img = load_sprite()
    if img.isNull():
        return
    # fit the image into the rect preserving aspect ratio
    rw, rh = rect.width(), rect.height()
    iw, ih = img.width(), img.height()
    s = min(rw / iw, rh / ih)
    dw, dh = iw * s, ih * s
    cx, cy = rect.center().x(), rect.center().y() + dy
    p.save()
    p.translate(cx, cy)
    p.scale(scale, scale)
    p.translate(-dw / 2, -dh / 2)
    p.drawImage(QRectF(0, 0, dw, dh), img)
    p.restore()
