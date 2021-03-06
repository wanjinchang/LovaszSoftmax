"""
Python utils
Maxim Berman 2018 ESAT-PSI KU Leuven (MIT License)
"""

from __future__ import print_function, division
from itertools import  ifilterfalse
import numpy as np
from PIL import Image, ImageDraw


def mean(l, ignore_nan=False, empty=0):
    """
    nanmean compatible with generators.
    """
    l = iter(l)
    if ignore_nan:
        l = ifilterfalse(np.isnan, l)
    try:
        n = 1
        acc = next(l)
    except StopIteration:
        if empty == 'raise':
            raise ValueError('Empty mean')
        return empty
    for n, v in enumerate(l, 2):
        acc += v
    if n == 1:
        return acc
    return acc / n


def paletteVOC(N=256, normalized=False, PIL=False):
    """
    Pascal VOC color map
    """
    def bitget(byteval, idx):
        return ((byteval & (1 << idx)) != 0)

    dtype = 'float32' if normalized else 'uint8'
    cmap = np.zeros((N, 3), dtype=dtype)
    for i in range(N):
        r = g = b = 0
        c = i
        for j in range(8):
            r = r | (bitget(c, 0) << 7-j)
            g = g | (bitget(c, 1) << 7-j)
            b = b | (bitget(c, 2) << 7-j)
            c = c >> 3

        cmap[i] = np.array([r, g, b])

    cmap = cmap/255 if normalized else cmap
    if PIL:
        cmap = [k for l in cmap for k in l]
    return cmap


def pil_grid(images, max_horiz=np.iinfo(int).max, margin=0, background='white'):
    """
    Grid of images in PIL
    """
    n_images = len(images)
    n_horiz = min(n_images, max_horiz)
    h_sizes, v_sizes = [0] * n_horiz, [0] * (n_images // n_horiz)
    for i, im in enumerate(images):
        h, v = i % n_horiz, i // n_horiz
        h_sizes[h] = max(h_sizes[h], im.size[0]) + margin
        v_sizes[v] = max(v_sizes[v], im.size[1]) + margin
    h_sizes, v_sizes = np.cumsum([0] + h_sizes), np.cumsum([0] + v_sizes)
    im_grid = Image.new('RGB', (h_sizes[-1], v_sizes[-1]), color=background)
    for i, im in enumerate(images):
        im_grid.paste(im, (h_sizes[i % n_horiz], v_sizes[i // n_horiz]))
    return im_grid


def dummy_triangles(w, categories=[0, 255, 1]):
    """
    Generate random images with desired categories and random triangles
    """
    im = Image.new('P', (w, w), color=categories[0])
    im.putpalette(paletteVOC(PIL=True))
    draw = ImageDraw.Draw(im)
    for c in categories[1:]:
        draw.polygon(map(tuple, np.random.randint(w, size=(3, 2))), fill=c, outline=None)
    return im