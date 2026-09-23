# -*- coding: utf-8 -*-
"""Deadpool desktop pet window: breathing sprite, scrolling speech bubble,
chimichanga pulse, drag/menu/chat. Port of the original pet's logic onto a
provided sprite image."""

import math
import os
import random
import sys

from PySide6.QtCore import (QPointF, QRectF, QSettings, Qt, QTimer)
from PySide6.QtGui import (QColor, QCursor, QFont, QFontMetrics, QImage,
                           QPainter, QPainterPath, QPen)
from PySide6.QtWidgets import QApplication, QMenu, QWidget

from . import dialogue, sprite

# sprite area: 40% of the original 340x340, then shrunk to 80% of that
WINDOW_W, WINDOW_H = 340, 300
SPRITE_W = 192
SPRITE_RECT = QRectF((WINDOW_W - SPRITE_W) / 2, 78, SPRITE_W, SPRITE_W)
BUBBLE_RECT = QRectF(10, 4, WINDOW_W - 20, 66)
FPS = 30


def clamp(v, lo, hi):
    return max(lo, min(hi, v))


class PetWindow(QWidget):
    def __init__(self, font_family=None):
        super().__init__(None)
        flags = Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint
        if sys.platform.startswith("linux"):
            flags |= Qt.WindowType.X11BypassWindowManagerHint
        self.setWindowFlags(flags)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setMouseTracking(True)
        self.setFixedSize(WINDOW_W, WINDOW_H)
        self.setWindowTitle("Deadpool — Desktop Pet")
        self.cn_font_family = font_family or "Droid Sans Fallback"

        self.settings = QSettings("DeadpoolPet", "DeadpoolPet")
        self.quiet = self.settings.value("quiet", False, type=bool)
        self.movable = True
        self.ontop = True

        # ----- state machine (minimal: idle/hover/poke/drag/talk) -----
        self.state = "idle"
        self.state_t = 0.0
        self.T = 0.0
        self.hovering = False
        self.dragging = False
        self.press_pos = None
        self.press_off = None
        self.drag_moved = False
        self.double_clicked = False
        self.exiting = False
        self.idle_until = random.uniform(16, 30)

        # ----- speech bubble (scrolling text) -----
        self.bubble = None       # dict(cn, en, lines_cn, lines_en, scroll, t0)
        self.scroll_speed = 34.0
        self.bubble_font_cn = QFont(self.cn_font_family, 13)
        self.bubble_font_cn.setBold(True)
        self.bubble_font_en = QFont("DejaVu Sans", 9)
        self.bubble_font_en.setItalic(True)

        # ----- particles -----
        self.particles = []
        self._chimi_cache = None

        # ----- chat -----
        self.chat = None

        self.click_timer = QTimer(self)
        self.click_timer.setSingleShot(True)
        self.click_timer.timeout.connect(self._poke)
        self.frame = QTimer(self)
        self.frame.timeout.connect(self._tick)
        self.frame.start(1000 // FPS)

        self._restore_pos()

    # ------------------------------------------------------------- position
    def _restore_pos(self):
        p = self.settings.value("pos")
        if p is not None:
            self.move(p)
        else:
            scr = QApplication.primaryScreen().availableGeometry()
            self.move(scr.right() - self.width() - 40,
                      scr.bottom() - self.height() - 40)
        self._clamp_to_screen()

    def _clamp_to_screen(self):
        scr = QApplication.primaryScreen().availableGeometry()
        x = clamp(self.x(), scr.left() - self.width() + 40, scr.right() - 40)
        y = clamp(self.y(), scr.top(), scr.bottom() - 30)
        self.move(x, y)

    # ------------------------------------------------------------- main loop
    def _tick(self):
        dt = 1.0 / FPS
        self.T += dt
        self.state_t += dt

        if self.state == "idle" and not self.dragging and self.T >= self.idle_until:
            self.idle_until = self.T + random.uniform(18, 34)
            if not self.quiet and random.random() < 0.75:
                self._say(*dialogue.pick("idle_talk"))

        self._update_bubble(dt)
        self._update_particles(dt)
        self.update()

    # ------------------------------------------------------------- speech
    def _say(self, cn, en=None):
        if cn is None:
            self.bubble = None
            return
        if self.quiet:
            return
        fm_cn = QFontMetrics(self.bubble_font_cn)
        fm_en = QFontMetrics(self.bubble_font_en)
        max_w = int(BUBBLE_RECT.width()) - 28
        lines_cn = self._wrap(cn, fm_cn, max_w)
        lines_en = self._wrap(en or "", fm_en, max_w - 8) if en else []
        self.bubble = {"cn": cn, "en": en or "",
                       "lines_cn": lines_cn, "lines_en": lines_en,
                       "scroll": 0.0, "t0": self.T,
                       "total_h": len(lines_cn) * 21 + len(lines_en) * 15,
                       "done_scroll": False}

    @staticmethod
    def _wrap(text, fm, max_w):
        lines, cur = [], ""
        for ch in text:
            if fm.horizontalAdvance(cur + ch) > max_w and cur:
                lines.append(cur)
                cur = ch
            else:
                cur += ch
        if cur:
            lines.append(cur)
        return lines

    def _update_bubble(self, dt):
        if not self.bubble:
            return
        b = self.bubble
        view_h = BUBBLE_RECT.height() - 16
        if b["total_h"] > view_h:
            if not b["done_scroll"]:
                b["scroll"] += self.scroll_speed * dt
                if b["scroll"] >= b["total_h"] - view_h:
                    b["scroll"] = b["total_h"] - view_h
                    b["done_scroll"] = True
                    b["t0"] = self.T          # hold at the end
        # lifetime: scrolling phase + 3s hold; short text: 4.5s
        if b["done_scroll"] or b["total_h"] <= view_h:
            if self.T - b["t0"] > (3.0 if b["done_scroll"] else 4.5):
                self.bubble = None

    # ------------------------------------------------------------- particles
    def _spawn(self, x, y, vx, vy, ttl, kind, **extra):
        pt = {"x": x, "y": y, "vx": vx, "vy": vy,
              "ttl": ttl, "age": 0.0, "kind": kind}
        pt.update(extra)
        self.particles.append(pt)

    def _chimi_burst(self, n, speed):
        """Chimichanga pulse: n mini-burritos spawn on a RING around the
        sprite's outline (not from its center) and fly radially outward."""
        c = SPRITE_RECT.center()
        r = SPRITE_RECT.width() * 0.46          # emission ring radius
        for i in range(n):
            ang = 2 * math.pi * i / n + random.uniform(-0.16, 0.16)
            sp = speed * random.uniform(0.75, 1.2)
            rr = r + random.uniform(-5, 5)
            self._spawn(c.x() + math.cos(ang) * rr,
                        c.y() + math.sin(ang) * rr,
                        math.cos(ang) * sp, math.sin(ang) * sp,
                        random.uniform(0.7, 1.15), "chimi",
                        rot=random.uniform(0, 360),
                        rot_spd=random.uniform(-420, 420))

    def _spawn_heart(self):
        cx, cy = SPRITE_RECT.center().x(), SPRITE_RECT.top() + 20
        self._spawn(cx + random.uniform(-60, 60), cy,
                    random.uniform(-12, 12), random.uniform(-70, -50),
                    random.uniform(1.4, 2.2), "heart")

    def _spawn_exclaim(self):
        cx, cy = SPRITE_RECT.center().x(), SPRITE_RECT.top() - 4
        self._spawn(cx, cy, 0, -24, 0.5, "exclaim")

    def _update_particles(self, dt):
        keep = []
        for pt in self.particles:
            pt["age"] += dt
            if pt["age"] >= pt["ttl"]:
                continue
            pt["x"] += pt["vx"] * dt
            pt["y"] += pt["vy"] * dt
            pt["vy"] *= (1 - 0.4 * dt)
            if "rot" in pt:
                pt["rot"] = (pt["rot"] + pt["rot_spd"] * dt) % 360
            keep.append(pt)
        self.particles = keep

    # ------------------------------------------------------------- interactions
    def _hover_started(self):
        if self.dragging:
            return
        self.hovering = True
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.state_t = 0.0
        if self.state != "hover":
            self.state = "hover"
            if not self.quiet and random.random() < 0.9:
                self._say(*dialogue.pick("greet"))
            self._spawn_exclaim()
            self._chimi_burst(8, 62)      # chimichanga pulse!
        # occasional small pulse while hovering
        if random.random() < 0.05:
            self._chimi_burst(4, 40)

    def _hover_ended(self):
        self.hovering = False
        self.unsetCursor()
        if self.state == "hover":
            self.state = "idle"

    def _poke(self):
        if self.exiting:
            return
        self._say(*dialogue.pick("poke"))

    def _double_click(self):
        if self.exiting:
            return
        self._say(*dialogue.pick("dblclick"))
        self._chimi_burst(6, 55)

    def _feed(self):
        if self.exiting:
            return
        self._say(*dialogue.pick("feed"))
        self._chimi_burst(10, 60)
        for _ in range(4):
            self._spawn_heart()

    # ------------------------------------------------------------- painting
    def paintEvent(self, _ev):
        if getattr(self, "_painting", False):
            return
        self._painting = True
        try:
            self._paint()
        finally:
            self._painting = False

    def _paint(self):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing, True)

        # gentle breathing scale (area ratio max/min <= 1.2)
        scale = sprite.breathe_scale(self.T)
        dy = 0.0
        if self.state == "hover" and self.state_t < 0.45:
            u = self.state_t / 0.45
            dy = -math.sin(math.pi * u) * 26      # startled hop
        elif self.state == "hover":
            dy = math.sin(self.T * 6) * 3

        sprite.paint(p, SPRITE_RECT, self.T, dy=dy, scale=scale)
        self._paint_particles(p)
        if self.bubble:
            self._paint_bubble(p)

    def _paint_bubble(self, p):
        b = self.bubble
        r = BUBBLE_RECT
        # white rounded bubble with tail
        path = QPainterPath()
        path.addRoundedRect(r, 12, 12)
        tx, ty = r.center().x(), r.bottom()
        path.moveTo(tx - 9, ty)
        path.lineTo(tx, ty + 13)
        path.lineTo(tx + 9, ty)
        path.closeSubpath()
        p.setPen(QPen(QColor("#2B2B2B"), 2))
        p.setBrush(QColor(255, 255, 255, 246))
        p.drawPath(path)

        # scrolling text inside the bubble
        view = QRectF(r.x() + 10, r.y() + 8, r.width() - 20, r.height() - 16)
        p.save()
        p.setClipRect(view)
        p.translate(0, -b["scroll"])
        p.setFont(self.bubble_font_cn)
        p.setPen(QColor("#222222"))
        y = view.y() + 2
        for ln in b["lines_cn"]:
            p.drawText(QRectF(view.x(), y, view.width(), 21),
                       Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, ln)
            y += 21
        if b["lines_en"]:
            p.setFont(self.bubble_font_en)
            p.setPen(QColor("#888888"))
            for ln in b["lines_en"]:
                p.drawText(QRectF(view.x() + 2, y, view.width() - 4, 15),
                           Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, ln)
                y += 15
        p.restore()

    def _paint_particles(self, p):
        for pt in self.particles:
            a = 1.0 - pt["age"] / pt["ttl"]
            k = pt["kind"]
            if k == "exclaim":
                p.setPen(QPen(QColor(255, 60, 60, int(255 * a)), 0))
                f = QFont("DejaVu Sans", 24)
                f.setBold(True)
                p.setFont(f)
                p.drawText(QPointF(pt["x"] - 8, pt["y"]), "!")
            elif k == "heart":
                self._draw_heart(p, pt["x"], pt["y"], 6 * a, a)
            elif k == "chimi":
                self._draw_mini_chimi(p, pt["x"], pt["y"],
                                      pt.get("rot", 0.0), a)

    def _chimi_image(self):
        """🌯 rendered off-screen once (colored emoji does not survive the
        DirectComposition path of a translucent window, so we blit a
        pre-rendered image instead of drawing the glyph live)."""
        if self._chimi_cache is None:
            S = 96
            img = QImage(S, S, QImage.Format_ARGB32)
            img.fill(Qt.GlobalColor.transparent)
            qp = QPainter(img)
            qp.setRenderHint(QPainter.RenderHint.Antialiasing, True)
            qp.setFont(QFont("Segoe UI Emoji", 62))
            qp.setPen(QColor(0, 0, 0))
            qp.drawText(QPointF(6, 74), "🌯")
            qp.end()
            self._chimi_cache = img
        return self._chimi_cache

    def _draw_mini_chimi(self, p, x, y, rot, alpha):
        """Spinning burrito particle drawn as the 🌯 emoji (~2x area of the
        original vector version, rendered off-screen then blitted)."""
        img = self._chimi_image()
        p.save()
        p.translate(x, y)
        p.rotate(rot)
        p.setOpacity(alpha)
        p.drawImage(QRectF(-13, -13, 26, 26), img)
        p.setOpacity(1.0)
        p.restore()

    def _draw_heart(self, p, x, y, s, alpha):
        p.save()
        p.translate(x, y)
        p.scale(s, s)
        p.setPen(Qt.PenStyle.NoPen)
        p.setBrush(QColor(255, 90, 120, int(255 * alpha)))
        path = QPainterPath()
        path.moveTo(0, 4)
        path.cubicTo(-9, -3, -6, -11, 0, -5)
        path.cubicTo(6, -11, 9, -3, 0, 4)
        p.drawPath(path)
        p.restore()

    # ------------------------------------------------------------- events
    def leaveEvent(self, _ev):
        if not self.dragging:
            self._hover_ended()

    def mouseMoveEvent(self, ev):
        if self.dragging:
            self.move(ev.globalPos() - self.press_off)
            if not self.drag_moved \
                    and (ev.pos() - self.press_pos).manhattanLength() > 6:
                self.drag_moved = True
                self._say(*dialogue.pick("drag_start"))
            return
        if SPRITE_RECT.contains(ev.pos().x(), ev.pos().y()):
            self._hover_started()
        elif self.hovering:
            self._hover_ended()

    def mousePressEvent(self, ev):
        if ev.button() == Qt.MouseButton.RightButton:
            self._show_menu(ev.globalPos())
            return
        if ev.button() == Qt.MouseButton.LeftButton:
            if not self.movable:
                self.click_timer.start(0)
                return
            self.press_pos = ev.pos()
            self.press_off = ev.globalPos() - self.frameGeometry().topLeft()
            self.dragging = True
            self.drag_moved = False

    def mouseReleaseEvent(self, ev):
        if ev.button() != Qt.MouseButton.LeftButton or not self.dragging:
            return
        self.dragging = False
        if self.drag_moved:
            self._clamp_to_screen()
            self.settings.setValue("pos", self.pos())
            self._say(*dialogue.pick("drag_drop"))
        else:
            if not self.double_clicked:
                self.click_timer.start(260)
        self.double_clicked = False

    def mouseDoubleClickEvent(self, ev):
        if ev.button() == Qt.MouseButton.LeftButton:
            self.double_clicked = True
            self.click_timer.stop()
            self._double_click()

    # ------------------------------------------------------------- menu
    def _show_menu(self, gpos):
        m = QMenu(self)
        m.setStyleSheet("QMenu { background:#2b2b2b; color:#eee;"
                        " border:1px solid #555; border-radius:6px; padding:4px; }"
                        "QMenu::item { padding:6px 22px; border-radius:4px; }"
                        "QMenu::item:selected { background:#C8102E; }")
        m.addAction("🌯 喂我 Chimichanga", self._feed)
        m.addAction("💬 跟我聊聊", self._open_chat)
        m.addSeparator()
        m.addAction("🔇 静音" if not self.quiet else "🔊 恢复讲话",
                    self._toggle_quiet)
        m.addAction("📌 锁定位置" if self.movable else "📍 解除锁定",
                    self._toggle_movable)
        m.addSeparator()
        m.addAction("🚪 退出（我要去找 Chimichanga 了）", self._quit_pet)
        m.exec_(gpos)

    def _toggle_quiet(self):
        if self.quiet:
            self.quiet = False
            self.settings.setValue("quiet", False)
            self._say(*dialogue.pick("quiet_off"))
        else:
            self._say(*dialogue.pick("quiet_on"))
            self.quiet = True
            self.settings.setValue("quiet", True)

    def _toggle_movable(self):
        self.movable = not self.movable
        if not self.movable:
            self._say("Fine. I'll stay put. Like a very sassy statue.",
                      "行吧，我原地待着，像尊非常毒舌的雕像。")

    def _open_chat(self):
        if self.chat is None:
            from .chat_window import ChatDialog
            self.chat = ChatDialog(self)
        scr = QApplication.primaryScreen().availableGeometry()
        x = self.x() + self.width() + 14
        if x + self.chat.width() > scr.right():
            x = self.x() - self.chat.width() - 14
        y = clamp(self.y(), scr.top(), scr.bottom() - self.chat.height())
        self.chat.move(x, y)
        self.chat.show()
        self.chat.raise_()
        self.chat.input.setFocus()
        self._say(*dialogue.pick("chat_open"))

    def _quit_pet(self):
        if self.exiting:
            return
        self.exiting = True
        self._say(*dialogue.pick("exit"))
        QTimer.singleShot(2000, QApplication.instance().quit)
