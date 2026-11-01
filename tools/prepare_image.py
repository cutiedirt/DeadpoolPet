#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Cut the Deadpool image out of its white background (v2).

Fixes:
  * white EYES (the white part inside the black eye-masks) were previously
    mistaken for background and cut out -> internal holes are restored
  * the "豆包AI生成" watermark bottom-right is removed more thoroughly
"""

import os
import sys

import numpy as np
from PIL import Image, ImageFilter

# 源图路径：用环境变量 SRC_IMAGE 或第一个命令行参数传入。
# （原先硬编码本机绝对路径，会把 Windows 用户名带进公开仓库）
SRC = os.environ.get("SRC_IMAGE") or (sys.argv[1] if len(sys.argv) > 1 else "")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_SPRITE = os.path.join(ROOT, "assets", "sprite.png")
OUT_ICON = os.path.join(ROOT, "assets", "icon.png")

WHITE_T = 26
FEATHER = 2.2


def cutout():
    if not SRC:
        raise SystemExit("请指定源图：SRC_IMAGE 环境变量或第一个命令行参数")
    im = Image.open(SRC).convert("RGB")
    a = np.asarray(im, dtype=np.float32)
    dist = np.sqrt(((a - 255.0) ** 2).sum(axis=2))
    alpha = np.clip((dist - WHITE_T) / FEATHER, 0.0, 1.0) * 255.0
    alpha = alpha.astype(np.uint8)

    # --- step 2: restore internal "holes" (white eyes etc.) ---------------
    # transparent pixels that are NOT connected to the image border are
    # internal details that were wrongly cut; bring them back opaque white.
    tm = alpha < 10
    if tm.any():
        edge = np.zeros_like(tm)
        edge[0, :] = tm[0, :]
        edge[-1, :] = tm[-1, :]
        edge[:, 0] = tm[:, 0]
        edge[:, -1] = tm[:, -1]
        while True:
            n = (np.roll(edge, 1, 0) | np.roll(edge, -1, 0)
                 | np.roll(edge, 1, 1) | np.roll(edge, -1, 1)) & tm
            new = edge | n
            if new.sum() == edge.sum():
                break
            edge = new
        holes = tm & ~edge
        print("internal holes restored:", int(holes.sum()), "px")
        alpha[holes] = 255

    mask = Image.fromarray(alpha, "L").filter(ImageFilter.GaussianBlur(0.8))
    rgba = im.convert("RGBA")
    rgba.putalpha(mask)

    # --- trim empty margins -------------------------------------------------
    arr = np.asarray(rgba)
    al = arr[..., 3]
    ys, xs = np.where(al > 8)
    x0, x1 = xs.min(), xs.max()
    y0, y1 = ys.min(), ys.max()
    pad_x = int((x1 - x0) * 0.015) + 2
    pad_y = int((y1 - y0) * 0.015) + 2
    x0, x1 = max(0, x0 - pad_x), min(arr.shape[1], x1 + pad_x)
    y0, y1 = max(0, y0 - pad_y), min(arr.shape[0], y1 + pad_y)
    rgba = rgba.crop((x0, y0, x1, y1))

    # --- step 3: watermark: dark low-saturation pixels in the bottom-right -
    w, h = rgba.size
    arr = np.asarray(rgba)
    x0w, y0w = int(w * 0.55), int(h * 0.62)          # generous zone
    zone = arr[y0w:, x0w:]
    rgb = zone[..., :3].astype(int)
    mx = rgb.max(axis=2); mn = rgb.min(axis=2)
    mean = rgb.mean(axis=2)
    # text is dark and grey-ish; colored rays stay
    grey_dark = (mx - mn < 40) & (mean < 150) & (zone[..., 3] > 30)
    zone[..., 3][grey_dark] = 0
    arr[y0w:, x0w:] = zone
    rgba = Image.fromarray(arr)
    print("watermark-zone grey pixels cleared:", int(grey_dark.sum()))

    # --- step 4: user requested: just blank the whole bottom-right corner --
    # (nothing important lives there; guarantees the watermark is gone)
    arr = np.asarray(rgba)
    w, h = rgba.size
    cx, cy = int(w * 0.74), int(h * 0.80)
    arr[cy:, cx:, 3] = 0
    rgba = Image.fromarray(arr)
    print("bottom-right corner blanked:", (w - cx), "x", (h - cy), "px")
    return rgba


def main():
    sprite = cutout()
    sprite.save(OUT_SPRITE)
    print("sprite:", OUT_SPRITE, sprite.size)

    icon = sprite.copy()
    icon.thumbnail((512, 512), Image.LANCZOS)
    canvas = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
    canvas.paste(icon, ((512 - icon.width) // 2, (512 - icon.height) // 2),
                 icon)
    canvas.save(OUT_ICON)
    print("icon:", OUT_ICON)

    a = np.asarray(sprite)
    al = a[..., 3]
    print("transparent:", round(100 * (al < 10).mean(), 1), "%",
          "opaque:", round(100 * (al > 200).mean(), 1), "%")


if __name__ == "__main__":
    main()
