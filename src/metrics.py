import numpy as np
from PIL import Image
from collections import Counter
import math

def load_pixels(path: str) -> np.ndarray:
    return np.array(Image.open(path))

def entropy(path: str) -> float:
    data = load_pixels(path).flatten()
    counts = Counter(data)
    total = len(data)
    h = 0.0
    for c in counts.values():
        p = c / total
        h -= p * math.log2(p)
    return h

def correlation(path: str, direction: str = "horizontal", samples: int = 5000) -> float:
    img = load_pixels(path)
    if img.ndim == 3:
        img = img[:, :, 0]
    h, w = img.shape
    rng = np.random.default_rng(42)
    if direction == "horizontal":
        xs = rng.integers(0, w - 1, size=samples)
        ys = rng.integers(0, h, size=samples)
        a = img[ys, xs].astype(float)
        b = img[ys, xs + 1].astype(float)
    else:
        xs = rng.integers(0, w, size=samples)
        ys = rng.integers(0, h - 1, size=samples)
        a = img[ys, xs].astype(float)
        b = img[ys + 1, xs].astype(float)
    if a.std() == 0 or b.std() == 0:
        return 0.0
    return float(np.corrcoef(a, b)[0, 1])

def npcr_uaci(path1: str, path2: str):
    a = load_pixels(path1).astype(float)
    b = load_pixels(path2).astype(float)
    if a.shape != b.shape:
        raise ValueError("Images must have the same shape")
    diff = a != b
    npcr = diff.mean() * 100
    uaci = (np.abs(a - b) / 255.0).mean() * 100
    return npcr, uaci