"""
NET3106 Assignment - Part B
Random-walk visual test: convert each bit stream into a 2D random walk
by reading bits in pairs to choose a step direction, then plot the path.

Direction mapping (2 bits -> 4 directions):
    00 -> up    (y += 1)
    01 -> down  (y -= 1)
    10 -> left  (x -= 1)
    11 -> right (x += 1)
"""

import matplotlib
matplotlib.use("Agg")  # no display needed, just save to file
import matplotlib.pyplot as plt
import numpy as np


def read_bits_from_file(path):
    """Read a file of '0'/'1' characters into a numpy uint8 array."""
    with open(path, "r") as f:
        s = f.read().strip()
    return np.array([int(c) for c in s], dtype=np.uint8)


def bits_to_walk(bits):
    """
    Convert a bit stream into a 2D random walk by reading bits in pairs.
    00 -> up, 01 -> down, 10 -> left, 11 -> right.
    Returns arrays of x and y coordinates visited (including start at 0,0).
    """
    # Make sure we have an even number of bits so pairing works cleanly
    n_pairs = len(bits) // 2
    bits = bits[: n_pairs * 2]
    pairs = bits.reshape(n_pairs, 2)

    x, y = 0, 0
    xs = np.zeros(n_pairs + 1, dtype=np.int64)
    ys = np.zeros(n_pairs + 1, dtype=np.int64)

    for i, (b0, b1) in enumerate(pairs):
        if b0 == 0 and b1 == 0:
            y += 1          # up
        elif b0 == 0 and b1 == 1:
            y -= 1          # down
        elif b0 == 1 and b1 == 0:
            x -= 1          # left
        else:  # b0 == 1 and b1 == 1
            x += 1          # right
        xs[i + 1] = x
        ys[i + 1] = y

    return xs, ys


def plot_walk(xs, ys, title, out_path):
    plt.figure(figsize=(7, 7))
    plt.plot(xs, ys, linewidth=0.5, color="#1f77b4")
    plt.scatter([xs[0]], [ys[0]], color="green", s=40, zorder=5, label="start")
    plt.scatter([xs[-1]], [ys[-1]], color="red", s=40, zorder=5, label="end")
    plt.title(title)
    plt.xlabel("x")
    plt.ylabel("y")
    plt.axis("equal")
    plt.legend()
    plt.tight_layout()
    plt.savefig(out_path, dpi=150)
    plt.close()
    print(f"Saved {out_path}")


if __name__ == "__main__":
    strong_bits = read_bits_from_file(r"strong_source.txt")
    weak_bits = read_bits_from_file(r"weak_source.txt")

    xs_strong, ys_strong = bits_to_walk(strong_bits)
    xs_weak, ys_weak = bits_to_walk(weak_bits)

    print(f"Strong walk: {len(xs_strong)-1} steps, "
          f"final position ({xs_strong[-1]}, {ys_strong[-1]}), "
          f"range x[{xs_strong.min()},{xs_strong.max()}] y[{ys_strong.min()},{ys_strong.max()}]")
    print(f"Weak walk:   {len(xs_weak)-1} steps, "
          f"final position ({xs_weak[-1]}, {ys_weak[-1]}), "
          f"range x[{xs_weak.min()},{xs_weak.max()}] y[{ys_weak.min()},{ys_weak.max()}]")

    plot_walk(xs_strong, ys_strong, "Random Walk - Strong Source (r=3.99)",
              r"walk_strong.png")
    plot_walk(xs_weak, ys_weak, "Random Walk - Weak Source (r=3.5)",
              r"walk_weak.png")