"""
NET3106 Assignment - Part C
Random-bitmap visual test: convert each bit stream into a 256x256
black-and-white image, one pixel per bit.

A strong source should look like structureless static.
A weak source should show stripes, tiles, solid regions, or diagonals.
"""

import numpy as np
from PIL import Image


def read_bits_from_file(path):
    with open(path, "r") as f:
        s = f.read().strip()
    return np.array([int(c) for c in s], dtype=np.uint8)


def bits_to_bitmap(bits, size=256):
    """
    Take the first size*size bits and arrange them into a size x size
    black-and-white image. bit=1 -> white pixel (255), bit=0 -> black (0).
    """
    n_needed = size * size
    if len(bits) < n_needed:
        raise ValueError(f"Need {n_needed} bits, only got {len(bits)}")

    grid = bits[:n_needed].reshape(size, size)
    # Scale 0/1 -> 0/255 so it renders as proper black/white, not near-black
    img_array = (grid * 255).astype(np.uint8)
    return Image.fromarray(img_array, mode="L")  # 'L' = 8-bit grayscale


if __name__ == "__main__":
    strong_bits = read_bits_from_file(r"strong_source.txt")
    weak_bits = read_bits_from_file(r"weak_source.txt")

    strong_img = bits_to_bitmap(strong_bits, size=256)
    weak_img = bits_to_bitmap(weak_bits, size=256)

    strong_img.save("bitmap_strong.png")
    weak_img.save("bitmap_weak.png")

    print("Saved bitmap_strong.png and bitmap_weak.png (256x256 each)")

    # Quick numeric sanity check: fraction of white pixels in each
    strong_white_pct = 100 * (np.array(strong_img) == 255).mean()
    weak_white_pct = 100 * (np.array(weak_img) == 255).mean()
    print(f"Strong source: {strong_white_pct:.2f}% white pixels")
    print(f"Weak source:   {weak_white_pct:.2f}% white pixels")