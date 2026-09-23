# -*- coding: utf-8 -*-
"""A tiny chat hotline to Deadpool."""

from html import escape
import sys

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (QDialog, QHBoxLayout, QLineEdit, QPushButton,
                             QTextBrowser, QVBoxLayout, QWidget, QLabel)

from . import dialogue

TITLE_BG = "#C8102E"
BODY_BG = "#FFFDF5"


class ChatDialog(QDialog):
    def __init__(self, pet):
        super().__init__(pet)
        self.pet = pet
        self.brain = dialogue.ChatBrain()
        self._font = pet.cn_font_family
        FONT = self._font
        flags = Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint
        if sys.platform.startswith("linux"):
            flags |= Qt.WindowType.X11BypassWindowManagerHint
        self.setWindowFlags(flags)
        self.setFixedSize(430, 500)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, False)
        self.setStyleSheet(f"background:{BODY_BG}; border:1px solid #333;"
                           f" border-radius:10px;")

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        bar = QWidget()
        bar.setStyleSheet(f"background:{TITLE_BG};"
                          "border-top-left-radius:10px;"
                          "border-top-right-radius:10px;")
        bl = QHBoxLayout(bar)
        bl.setContentsMargins(12, 8, 8, 8)
        title = QLabel("💬 Deadpool Hotline — 死侍热线")
        title.setStyleSheet("color:#fff; font-weight:bold; background:transparent;")
        title.setFont(QFont(FONT, 11))
        bl.addWidget(title)
        bl.addStretch(1)
        close = QPushButton("✕")
        close.setFixedSize(26, 26)
        close.setStyleSheet("background:transparent; color:#fff; font-weight:bold;"
                            " border:none; font-size:15px;")
        close.clicked.connect(self.close)
        bl.addWidget(close)
        root.addWidget(bar)

        self.view = QTextBrowser()
        self.view.setStyleSheet(f"border:none; background:{BODY_BG};"
                                " padding:8px; font-size:13px;")
        self.view.setFont(QFont(FONT, 10))
        root.addWidget(self.view, 1)

        qrow = QHBoxLayout()
        qrow.setContentsMargins(8, 6, 8, 0)
        for label, fn in (("🌯 投喂", self.pet._feed),):
            b = QPushButton(label)
            b.setStyleSheet("background:#F3E3C3; border:1px solid #d9b96a;"
                            " border-radius:8px; padding:4px 10px;")
            b.setFont(QFont(FONT, 9))
            b.clicked.connect(fn)
            qrow.addWidget(b)
        root.addLayout(qrow)

        irow = QHBoxLayout()
        irow.setContentsMargins(8, 8, 8, 10)
        self.input = QLineEdit()
        self.input.setPlaceholderText("跟死侍说点什么… (Enter 发送)")
        self.input.setStyleSheet("border:1px solid #bbb; border-radius:10px;"
                                 " padding:6px 10px; background:#fff;")
        self.input.setFont(QFont(FONT, 10))
        self.input.returnPressed.connect(self._send)
        irow.addWidget(self.input, 1)
        send = QPushButton("发送 ➤")
        send.setStyleSheet(f"background:{TITLE_BG}; color:#fff; border:none;"
                           " border-radius:10px; padding:6px 14px;")
        send.setFont(QFont(FONT, 10))
        send.clicked.connect(self._send)
        irow.addWidget(send)
        root.addLayout(irow)

        self._append_dp("哇，终于有人类肯跟我说话了！", "Wow, a human finally talks to me!")
        self.input.setFocus()

    def _append_user(self, text):
        self.view.append(f'<p align="right" style="color:#666;">'
                         f'<b>你：</b>{escape(text)}</p>')

    def _append_dp(self, cn, en=""):
        extra = (f'<br><span style="color:#999; font-size:10px; font-style:italic;">'
                 f'{escape(en)}</span>' if en else "")
        self.view.append(f'<p style="color:#C8102E; margin-top:6px;">'
                         f'<b>死侍：</b>{escape(cn)}{extra}</p>')

    def _send(self):
        text = self.input.text().strip()
        if not text:
            return
        self.input.clear()
        self._append_user(text)
        cn, en = self.brain.reply(text)
        self._append_dp(cn, en)
        self.view.verticalScrollBar().setValue(
            self.view.verticalScrollBar().maximum())
        self.pet._chimi_burst(4, 40)
