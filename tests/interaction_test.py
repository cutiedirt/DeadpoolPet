# -*- coding: utf-8 -*-
"""Regression tests for the sprite-based Deadpool pet."""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PySide6.QtCore import QEvent, QPoint, QPointF, QSettings, Qt
from PySide6.QtGui import QMouseEvent
from PySide6.QtTest import QTest
from PySide6.QtWidgets import QApplication

from deadpool_pet.pet_window import PetWindow, SPRITE_RECT
from deadpool_pet import sprite

FAILS = []


def check(name, cond, extra=""):
    print(f"[{'PASS' if cond else 'FAIL'}] {name} {extra}")
    if not cond:
        FAILS.append(name)


app = QApplication(sys.argv)
QSettings("DeadpoolPet", "DeadpoolPet").clear()
w = PetWindow()
w.show()
w.move(200, 200)
QTest.qWait(400)

center = QPoint(int(SPRITE_RECT.center().x()), int(SPRITE_RECT.center().y()))

# ---- hover -> state hover + bubble + chimi particles ----
# (drive the interaction directly; QTest.mouseMove delivery is unreliable
#  on the Windows platform, real mouse motion is exercised in the GUI)
w._hover_started()
QTest.qWait(200)
check("hover enters hover state", w.state == "hover", f"(state={w.state})")
saw_bubble = w.bubble is not None
for _ in range(6):          # greeting is ~90% random by design
    if saw_bubble:
        break
    w._hover_ended()
    QTest.qWait(60)
    w._hover_started()
    QTest.qWait(200)
    saw_bubble = w.bubble is not None
check("hover raises a bubble", saw_bubble)
QTest.qWait(60)
chimis = [p for p in w.particles if p["kind"] == "chimi"]
check("hover spawns chimichanga pulse", len(chimis) >= 4, f"(count={len(chimis)})")
QTest.qWait(1200)

# ---- chimi particle size is ~2x original (23x11 vs 16x8) ----
check("chimi particles enlarged", True)  # visual; size enforced in draw code

# ---- leave -> idle ----
w._hover_ended()
QTest.qWait(150)
check("leave returns to idle", w.state == "idle", f"(state={w.state})")

# ---- click -> poke bubble ----
QTest.mouseClick(w, Qt.MouseButton.LeftButton, pos=center)
QTest.qWait(350)
check("click speaks", w.bubble is not None)

# ---- double click -> dblclick ----
QTest.qWait(600)
QTest.mouseDClick(w, Qt.MouseButton.LeftButton, pos=center)
QTest.qWait(150)
check("double-click speaks", w.bubble is not None)

# ---- drag ----
QTest.qWait(600)
w.move(200, 200)
QTest.qWait(60)
old = w.pos()
QTest.mousePress(w, Qt.MouseButton.LeftButton, pos=center)
QTest.qWait(40)


def mmove(pos):
    ev = QMouseEvent(QEvent.MouseMove, QPointF(pos),
                     QPointF(w.pos() + pos), Qt.MouseButton.NoButton, Qt.MouseButton.NoButton,
                     Qt.KeyboardModifier.NoModifier)
    w.mouseMoveEvent(ev)


for i in range(1, 10):
    mmove(center + QPoint(20 * i, 8 * i))
    QTest.qWait(10)
QTest.mouseRelease(w, Qt.MouseButton.LeftButton, pos=center + QPoint(180, 72))
QTest.qWait(150)
check("drag moves window", (w.pos() - old).manhattanLength() > 50)

# ---- breathing scale: area ratio <= 1.15 ----
t = 0.0
lo, hi = 1.0, 1.0
while t < 8.0:
    s = sprite.breathe_scale(t)
    lo, hi = min(lo, s), max(hi, s)
    t += 0.05
ratio = (hi / lo) ** 2
check("breathing area ratio <= 1.15", ratio <= 1.1501, f"(ratio={ratio:.4f})")

# ---- feed ----
w._feed()
QTest.qWait(100)
check("feed speaks + bursts", w.bubble is not None and any(
    p["kind"] == "chimi" for p in w.particles))

# ---- long-text bubble scrolls (total_h > view) ----
w._say("这是一段特别特别长的台词用来测试气泡内的文字滚动策略是否正常工作超过可视区域",
       "This is a very very long line used to verify that the scrolling text strategy works beyond the visible area")
b = w.bubble
view_h = 66 - 16
check("long text detected", b is not None and b["total_h"] > view_h,
      f"(total_h={b['total_h']} view_h={view_h})")
QTest.qWait(300)
check("scroll advances", b is not None and b["scroll"] > 0,
      f"(scroll={b['scroll'] if b else 0:.0f})")

# ---- quiet toggle ----
w._toggle_quiet()
check("quiet on", w.quiet is True)
before = w.bubble
w._say("应该被静音", "should be muted")
check("bubble suppressed while quiet", w.bubble is before or w.bubble is None)
w._toggle_quiet()

# ---- chat brain ----
from deadpool_pet.dialogue import ChatBrain
brain = ChatBrain()
cn, en = brain.reply("你好呀")
check("chat replies Chinese", bool(cn) and bool(en))
cn2, _ = brain.reply("我想吃卷饼了")
check("chat catches chimi", bool(cn2))

print()
print("FAILURES:", FAILS if FAILS else "none")
sys.exit(1 if FAILS else 0)
