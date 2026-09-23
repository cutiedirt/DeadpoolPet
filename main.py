#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Deadpool desktop pet entry point."""

import os
import sys

from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFontDatabase, QIcon
from PySide6.QtWidgets import QApplication

from deadpool_pet.pet_window import PetWindow


def _bundle_dir():
    if getattr(sys, "frozen", False):
        return sys._MEIPASS
    return os.path.dirname(os.path.abspath(__file__))


def _register_fonts():
    ttf = os.path.join(_bundle_dir(), "assets", "fonts", "DroidSansFallbackFull.ttf")
    if os.path.exists(ttf):
        fid = QFontDatabase.addApplicationFont(ttf)
        families = QFontDatabase.applicationFontFamilies(fid)
        return families[0] if families else None
    return None


def main():
    QApplication.setAttribute(Qt.ApplicationAttribute.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps, True)
    app = QApplication(sys.argv)
    app.setApplicationName("DeadpoolPet")
    app.setOrganizationName("DeadpoolPet")

    cn_font = _register_fonts()
    icon_path = os.path.join(_bundle_dir(), "assets", "icon.png")
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))

    w = PetWindow(font_family=cn_font)
    w.show()

    # debug hook: DEADPOOL_SHOT=/path.png or --shot=path -> screenshot & quit
    shot = os.environ.get("DEADPOOL_SHOT")
    if not shot and len(sys.argv) > 1 and sys.argv[1].startswith("--shot="):
        shot = sys.argv[1][len("--shot="):]
    if shot:
        def _shot():
            w.grab().save(shot)
            print("screenshot saved:", shot)
            print("window geo: pos=(%d,%d) size=(%dx%d)"
                  % (w.x(), w.y(), w.width(), w.height()))
            app.quit()
        QTimer.singleShot(3500, _shot)

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
