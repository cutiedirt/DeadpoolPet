#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Convert the pet source from PyQt5 to PySide6 (Qt6).

Qt6 uses DirectComposition for translucent windows on Windows, which is the
only mechanism this user's machine actually displays.
"""

import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ordered replacements: (regex, replacement)
REPL = [
    (r"from PyQt5\.", "from PySide6."),
    (r"import PySide6", "import PySide6"),
    # enums -> scoped enums
    (r"Qt\.FramelessWindowHint", "Qt.WindowType.FramelessWindowHint"),
    (r"Qt\.WindowStaysOnTopHint", "Qt.WindowType.WindowStaysOnTopHint"),
    (r"Qt\.X11BypassWindowManagerHint", "Qt.WindowType.X11BypassWindowManagerHint"),
    (r"Qt\.WA_TranslucentBackground", "Qt.WidgetAttribute.WA_TranslucentBackground"),
    (r"Qt\.WA_NoSystemBackground", "Qt.WidgetAttribute.WA_NoSystemBackground"),
    (r"Qt\.PointingHandCursor", "Qt.CursorShape.PointingHandCursor"),
    (r"Qt\.AlignLeft", "Qt.AlignmentFlag.AlignLeft"),
    (r"Qt\.AlignRight", "Qt.AlignmentFlag.AlignRight"),
    (r"Qt\.AlignVCenter", "Qt.AlignmentFlag.AlignVCenter"),
    (r"Qt\.AlignCenter", "Qt.AlignmentFlag.AlignCenter"),
    (r"Qt\.NoPen", "Qt.PenStyle.NoPen"),
    (r"Qt\.RoundCap", "Qt.PenCapStyle.RoundCap"),
    (r"Qt\.RoundJoin", "Qt.PenJoinStyle.RoundJoin"),
    (r"Qt\.transparent", "Qt.GlobalColor.transparent"),
    (r"Qt\.NoBrush", "Qt.BrushStyle.NoBrush"),
    (r"Qt\.NoButton", "Qt.MouseButton.NoButton"),
    (r"Qt\.LeftButton", "Qt.MouseButton.LeftButton"),
    (r"Qt\.RightButton", "Qt.MouseButton.RightButton"),
    (r"Qt\.NoModifier", "Qt.KeyboardModifier.NoModifier"),
    (r"Qt\.MouseMove", "Qt.EventType.MouseMove"),
    (r"Qt\.AA_EnableHighDpiScaling", "Qt.ApplicationAttribute.AA_EnableHighDpiScaling"),
    (r"Qt\.AA_UseHighDpiPixmaps", "Qt.ApplicationAttribute.AA_UseHighDpiPixmaps"),
    (r"\.exec_\(\)", ".exec()"),
    (r"QFontMetrics\.horizontalAdvance", "QFontMetrics.horizontalAdvance"),  # exists in Qt6
]


def convert_text(text):
    for pat, rep in REPL:
        text = re.sub(pat, rep, text)
    return text


def main():
    targets = []
    for base, dirs, files in os.walk(ROOT):
        if any(skip in base for skip in ("/build", "/dist", "/.git",
                                          "/__pycache__", "/node_modules")):
            continue
        for f in files:
            if f.endswith(".py"):
                targets.append(os.path.join(base, f))
    for path in sorted(targets):
        src = open(path, encoding="utf-8").read()
        new = convert_text(src)
        if new != src:
            open(path, "w", encoding="utf-8").write(new)
            print("converted:", os.path.relpath(path, ROOT))
    print("done,", len(targets), "py files scanned")


if __name__ == "__main__":
    main()
